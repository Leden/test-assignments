import asyncio
import logging
import typing as t

import click

from p5d_scraper.server import run_server
from p5d_scraper.worker import run_workers

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


@click.command()
@click.argument("input_files", type=click.File("r"), nargs=-1, required=False)
@click.argument("output_file", type=click.File("w"), required=False)
@click.option(
    "--interactive",
    "-i",
    is_flag=True,
    help="Interactive mode (start web server)",
)
def main(
    input_files: t.Iterable[t.IO[str]],
    output_file: t.IO[str],
    interactive: bool,  # noqa: FBT001: cli interface, it is ok
) -> None:
    """
    Planner 5D Gallery Scraper.

    INPUT_FILES: one or more files with links to scrape, or `-` (stdin).
    OUTPUT_FILE: a CSV file for the scraping results, or `-` (stdout).
    """
    if interactive:
        run_server()
    elif input_files and output_file:
        asyncio.run(run_workers(input_files, output_file))
    else:
        logger.error(
            "Either --interactive, or input_files and "
            "output_file must be specified."
        )


if __name__ == "__main__":
    main()
