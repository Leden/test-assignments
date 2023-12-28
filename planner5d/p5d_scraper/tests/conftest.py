import pytest
from aioresponses import aioresponses
from faker import Faker

from p5d_scraper.models import Project
from p5d_scraper.scraper import API_PROJECT_URL, BASE_URL


@pytest.fixture()
def mock_aioresponse() -> aioresponses:
    with aioresponses() as m:
        yield m


@pytest.fixture()
def url() -> str:
    return "https://example.com"


@pytest.fixture(params=[[], [1] * 3, [5, 4, 3, 2, 1]])
def rooms_by_floor(request: pytest.FixtureRequest) -> list[int]:
    return request.param


@pytest.fixture()
def project(
    url: str,
    rooms_by_floor: list[int],
    mock_aioresponse: aioresponses,
    faker: Faker,
) -> Project:
    hash_ = faker.uuid4(cast_to=None).hex
    name = faker.pystr()
    prj = Project(
        hash=hash_,
        title=name,
        total_rooms=sum(rooms_by_floor, 0),
        total_floors=len(rooms_by_floor),
    )
    mock_aioresponse.get(
        url,
        body=f"""
        ... {BASE_URL}v?key={hash_}&viewMode=3d ...
        """,
    )
    mock_aioresponse.get(
        f"{API_PROJECT_URL}{hash_}",
        payload={
            "items": [
                {
                    "name": name,
                    "data": {
                        "items": [
                            {
                                "className": "Floor",
                                "items": [
                                    {"className": "Room"} for _ in range(rooms)
                                ],
                            }
                            for rooms in rooms_by_floor
                        ],
                    },
                },
            ],
        },
    )
    return prj
