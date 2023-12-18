import typing as t


class Project(t.NamedTuple):
    hash: str  # noqa: A003: it is a nice name and does not hurt anyone
    title: str
    total_rooms: int
    total_floors: int
