import asyncio
import csv
import io

import pytest
from aiohttp import ClientSession

from p5d_scraper.models import Project
from p5d_scraper.worker import _make_csv_writer, run_workers, worker

pytestmark = pytest.mark.asyncio


async def test_run_workers(monkeypatch: pytest.MonkeyPatch) -> None:
    url = "https://example.com/"

    async def worker_mock(
        id_: int,
        tasks: asyncio.Queue[str],
        writer: csv.DictWriter,
        _session: ClientSession,
    ) -> None:
        try:
            task = await tasks.get()
            assert task == url

            assert id_ == 0

            writer.writerow(
                {
                    "hash": "foo",
                    "title": "foo",
                    "total_rooms": 42,
                    "total_floors": 64,
                }
            )
        finally:
            tasks.task_done()

    monkeypatch.setattr("p5d_scraper.worker.worker", worker_mock)

    input_file = io.StringIO(url)
    output_file = io.StringIO()

    await run_workers([input_file], output_file, 1)

    output_file.seek(0)
    assert "foo,foo,42,64\r\n" in list(output_file.readlines())


async def test_worker(url: str, project: Project) -> None:
    q: asyncio.Queue[str] = asyncio.Queue(1)
    q.put_nowait(url)

    out = io.StringIO()
    writer = _make_csv_writer(out)

    async with ClientSession() as session:
        w = asyncio.create_task(worker(1, q, writer, session))
        await q.join()
        w.cancel()

    out.seek(0)
    assert list(out.readlines()) == [
        "hash,title,total_rooms,total_floors\r\n",
        f"{project.hash},{project.title},{project.total_rooms},{project.total_floors}\r\n",
    ]
