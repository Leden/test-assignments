import io

from aiohttp import ClientSession, web

from p5d_scraper.scraper import get_gallery_project_links
from p5d_scraper.utils import arange
from p5d_scraper.worker import run_workers


def run_server() -> None:
    """
    Interactive mode: hosts a web server allowing the user to select
    which projects to scrape and download the resulting CSV.
    """
    app = web.Application()
    app.add_routes(
        [
            web.get("/", index_view),
            web.post("/process", process_view),
        ],
    )
    web.run_app(app)


async def index_view(_request: web.Request) -> web.Response:
    """
    Loads and displays the project links from the first 3 pages of the gallery.
    Allows the user to select which projects to scrape with an HTML form.
    """
    urls = []
    async with ClientSession() as session:
        # load first 3 pages to have 3*16=48 > 25 options to choose from
        # although 2 would suffice, but just barely.
        async for page in arange(3):
            urls += await get_gallery_project_links(page + 1, session)

    # for a more complex UI might use Jinja or some other template engine
    html = f"""
        <!DOCTYPE html>
        <html>
          <head></head>
          <body>
            <form action="/process" method="POST">
              <ul>{''.join(
                f'''<li>
                  <label>{url}
                    <input type="checkbox" id="{url}" name="{url}" />
                  <label/>
                </li>''' for url in urls)
              }</ul>
              <input type="submit" value="Submit"/>
            </form>
          </body>
        </html>
    """
    return web.Response(text=html, content_type="text/html")


async def process_view(request: web.Request) -> web.FileResponse:
    """
    Takes the selected links from POST request and scrapes them,
    then returns the resulting CSV as a downloadable file.
    """
    data = await request.post()
    input_file = io.StringIO("\n".join(data))
    output_file = io.StringIO()
    await run_workers([input_file], output_file)
    output_file.seek(0)
    return web.Response(
        body=output_file,
        headers={
            "Content-Disposition": 'attachment; filename="gallery.csv"',
            "Content-Type": "text/csv",
        },
    )
