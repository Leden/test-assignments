import pytest
from aiohttp import ClientSession
from aioresponses import aioresponses

from p5d_scraper.models import Project
from p5d_scraper.scraper import (
    GALLERY_URL,
    get_gallery_project_links,
    scrape_project,
)

pytestmark = pytest.mark.asyncio


# TODO: cover negative cases
async def test_get_gallery_project_links(
    mock_aioresponse: aioresponses,
) -> None:
    url = f"{GALLERY_URL}ABC123/floorplans-bar-baz-3d"
    mock_aioresponse.get(
        f"{GALLERY_URL}?page=1",
        body=f"""
        ... "{url}" ...
        """,
    )

    async with ClientSession() as session:
        urls = await get_gallery_project_links(1, session)

    assert urls == [url]


# TODO: cover negative cases
async def test_scrape_project(url: str, project: Project) -> None:
    async with ClientSession() as session:
        parsed = await scrape_project(url, session)

    assert parsed == project
