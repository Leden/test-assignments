import asyncio
import csv
import logging
import typing as t

from aiohttp import ClientSession

from p5d_scraper.models import Project
from p5d_scraper.scraper import ScrapingError, scrape_project

logger = logging.getLogger(__name__)

POOL_SIZE = 3


async def run_workers(
    input_files: t.Iterable[t.IO[str]],
    output_file: t.IO[str],
    pool_size: int = POOL_SIZE,
) -> None:
    """
    Scrape all URLs from the input files and write the scraped data as CSV
    into the output file.
    """
    tasks = _make_tasks_queue(input_files)
    writer = _make_csv_writer(output_file)

    async with ClientSession() as session:
        workers = [
            asyncio.create_task(worker(i, tasks, writer, session))
            for i in range(pool_size)
        ]

        await tasks.join()

        for w in workers:
            w.cancel()


async def worker(
    id_: int,
    tasks: asyncio.Queue[str],
    writer: csv.DictWriter,
    session: ClientSession,
) -> None:
    """
    Scraper Worker implementation.
    Gets an ID to use in logs, incoming tasks queue providing URLs to scrape,
    a csv writer to receive scraped data,
    and HTTP client session to make requests with.

    Skips URLs which could not be successfully scraped.

    While writing to the same file from several workers,
    we are still in a single thread running concurrently,
    so no special tricks to avoid races are needed.
    """
    logger.debug("Worker id=%s boots up", id_)
    while True:
        url = await tasks.get()
        try:
            project = await scrape_project(url, session)
        except ScrapingError:
            logger.exception("Error while scraping URL [%s]", url)
        else:
            # would be nice to have an async file api someday...
            writer.writerow(project._asdict())
        tasks.task_done()


def _make_tasks_queue(
    input_files: t.Iterable[t.IO[str]],
) -> asyncio.Queue[str]:
    """
    Helper function creating reading all lines from the given input streams
    and inserting them into the queue for scraping.
    Returns a new queue.
    """
    # Surely 100 capacity is plenty for everyone...
    # However might be a good idea to make producer a full coroutine
    # by itself and use blocking Queue.put to handle arbitrary large inputs
    tasks: asyncio.Queue[str] = asyncio.Queue(100)

    for f in input_files:
        for url in f.readlines():
            tasks.put_nowait(url.strip())

    return tasks


def _make_csv_writer(output_file: t.IO[str]) -> csv.DictWriter:
    """
    Helper function wrapping an output stream into a CSV DictWriter.
    """
    fieldnames = Project._fields
    writer = csv.DictWriter(output_file, fieldnames)
    writer.writeheader()
    return writer
