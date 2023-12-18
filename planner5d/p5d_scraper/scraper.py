import re

from aiohttp import ClientSession

from p5d_scraper.models import Project

BASE_URL = "https://planner5d.com/"
GALLERY_URL = f"{BASE_URL}gallery/floorplans/"
API_PROJECT_URL = f"{BASE_URL}api/project/"
HASH_LINK_RE = re.compile(BASE_URL + r"v\?key=([0-9a-f]{32})&viewMode=3d")
PROJECT_LINK_RE = re.compile(GALLERY_URL + r"[^/]+/[^\"]+")


class ScrapingError(Exception):
    pass


async def get_gallery_project_links(
    page: int, session: ClientSession
) -> list[str]:
    """
    Interactive mode helper function.
    Fetches the given page number from the gallery and extracts all unique
    links to projects.
    """
    async with session.get(
        f"{GALLERY_URL}?page={page}",
    ) as resp:
        html = await resp.text()
        matches = PROJECT_LINK_RE.finditer(html)
        # make urls unique but preserve the order
        urls = {m.group(0): None for m in matches if m}
        return list(urls)


async def scrape_project(url: str, session: ClientSession) -> Project:
    """
    Gets a project page url and scrapes the required data
    using the given HTTP client session.
    Returns Project instance.
    """
    async with session.get(url) as project_page_resp:
        hash_ = _parse_hash(await project_page_resp.text())

    async with session.get(
        f"{API_PROJECT_URL}{hash_}",
    ) as project_api_resp:
        project_json = await project_api_resp.json()

    title = _parse_name(project_json)
    total_rooms, total_floors = _count_rooms_and_floors(project_json)

    return Project(hash_, title, total_rooms, total_floors)


def _parse_hash(project_page: str) -> str:
    """
    A scraping helper function to extract project hash from the html page.
    For a simple task like this regex is fine. More complex data extraction
    may require a proper DOM parser.

    Gets the page html as str and returns the found project has as str,
    or raises ScrapingError.
    """
    match = HASH_LINK_RE.search(project_page)
    if not match:
        msg = "Project hash not found"
        raise ScrapingError(msg)

    return match.group(1)


def _parse_name(project_json: dict) -> str:
    """
    A scraping helper function to extract project name/title from api data.

    Gets project api data and returns the project name as str,
    or raises ScrapingError.
    """
    try:
        return project_json["items"][0]["name"]
    except (KeyError, IndexError) as err:
        msg = "Project name not found"
        raise ScrapingError(msg) from err


def _count_rooms_and_floors(project_json: dict) -> tuple[int, int]:
    """
    A scraping helper function to count the number of rooms and floors.

    Gets project api data and returns the 2-tuple with #rooms and #floors.
    Raises ScrapingError in case of unexpected structure of the data.
    """
    rooms = floors = 0
    try:
        data = project_json["items"][0]["data"]

        for item in data["items"]:
            if item["className"] == "Floor":
                floors += 1
                for floor_item in item["items"]:
                    if floor_item["className"] == "Room":
                        rooms += 1
    except (KeyError, IndexError) as err:
        msg = "Floor(s) and Room(s) not found"
        raise ScrapingError(msg) from err

    return rooms, floors
