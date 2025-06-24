from dataclasses import dataclass


@dataclass
class MatchTemplate:
    title: str
    coordinate: tuple[int, int]
    center: tuple[int, int]
    width: int
    height: int