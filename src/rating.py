from __future__ import annotations
from dataclasses import dataclass

RATE_MAP: dict = {
    "NR": 0,
    "AAA": 1,
    "AA+": 2,
    "AA": 3,
    "AA-": 4,
    "A+": 5,
    "A": 6,
    "A-": 7,
    "BBB+": 8,
    "BBB": 9,
    "BBB-": 10,
    "BB+": 11,
    "BB": 12,
    "BB-": 13,
    "B+": 14,
    "B": 15,
    "B-": 16,
    "CCC+": 17,
    "CCC": 18,
    "CCC-": 19,
    "CC+": 20,
    "CC": 21,
    "CC-": 22,
    "C+": 23,
    "C": 24,
    "C-": 25,
}

@dataclass
class Rating:

    snp_rate: str

    moodys_rate: str = None

    fitch_rate: str = None

    def __post_init__(self):
        if self.snp_rate == "" or self.snp_rate is None:
            self.snp_rate = "NR"

    def __eq__(self, ob: Rating)-> bool:
        return RATE_MAP[self.snp_rate] == RATE_MAP[ob.snp_rate]

    def __lt__(self, ob: Rating)-> bool:
        return RATE_MAP[self.snp_rate] > RATE_MAP[ob.snp_rate]

    def __gt__(self, ob: Rating)-> bool:
        return RATE_MAP[self.snp_rate] < RATE_MAP[ob.snp_rate]

    def get_score(self)-> int:
        return RATE_MAP[self.snp_rate]

    def is_a_rate(self)-> bool:
        return 1 < self.get_score() <= 7

    def is_b_rate(self)-> bool:
        return 7 < self.get_score() <= 16

    def is_c_rate(self)-> bool:
        return 16 < self.get_score() <= 19

    def is_investment_grade(self)-> bool:
        return 0 < self.get_score() <= 10

    def is_high_yield_grade(self)-> bool:
        return self.get_score() > 10

