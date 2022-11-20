from __future__ import annotations
from dataclasses import dataclass
from enum import Enum


class RatingSystem(Enum):
    SANDP = "S&P"
    MOODY = "Moody"
    FITCH = "Fitch"


S_P_RATE_MAP: dict = {
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
    "BBB-": 10, # Investment grade limit
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

MOODY_RATE_MAP: dict = {
    "WR": 0,
    "Aaa": 1,
    "Aa1": 2,
    "Aa2": 3,
    "Aa3": 4,
    "A1": 5,
    "A2": 6,
    "A3": 7,
    "Baa1": 8,
    "Baa2": 9,
    "Baa3": 10, # Investment grade limit
    "Ba1": 11,
    "Ba2": 12,
    "Ba3": 13,
    "B1": 14,
    "B2": 15,
    "B3": 16,
    "Caa1": 17,
    "Caa2": 18,
    "Caa3": 19,
    "Ca": 20,
    "C": 21,
}

RATE_MAP: dict = {
    RatingSystem.SANDP: S_P_RATE_MAP,
    RatingSystem.MOODY: MOODY_RATE_MAP,
    RatingSystem.FITCH: S_P_RATE_MAP,
}


@dataclass
class Rating:

    snp_rate: str

    moodys_rate: str = None

    fitch_rate: str = None

    use_rating: str = RatingSystem.SANDP

    def __post_init__(self):
        if self.snp_rate == "" or self.snp_rate is None:
            self.snp_rate = "NR"
            self.use_rating = RatingSystem.MOODY

        if self.moodys_rate == "" or self.moodys_rate is None:
            self.moodys_rate = "WR"
            self.use_rating = RatingSystem.FITCH

        if self.fitch_rate == "" or self.fitch_rate is None:
            self.fitch_rate = "WD"
            self.use_rating = RatingSystem.SANDP

    def __eq__(self, ob: Rating)-> bool:
        return self.get_score() == ob.get_score()

    def __lt__(self, ob: Rating)-> bool:
        return self.get_score() > ob.get_score()

    def __gt__(self, ob: Rating)-> bool:
        return self.get_score() < ob.get_score()

    def get_score(self)-> int:
        return RATE_MAP[self.use_rating][self.get_rate()]

    def get_rate(self)-> str:
        match self.use_rating:
            case RatingSystem.SANDP:
                return self.snp_rate
            case RatingSystem.MOODY:
                return self.moodys_rate
            case RatingSystem.FITCH:
                return self.fitch_rate
    
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

