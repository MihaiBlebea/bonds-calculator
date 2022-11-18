from typing import Dict
from dataclasses import dataclass, field
from datetime import datetime
from math import floor
import pycountry
from src.rating import Rating


def all_countries()-> Dict[str, str]:
    countries = {}
    for country in pycountry.countries:
        countries[country.name] = country.alpha_2

    return countries

COUNTRIES = all_countries()

@dataclass
class Bond:
    """
        Bond is a single bond model.

        Yields presented are estimated returns calculations. Pre-tax and fees. Prices can go up or down.
    """

    company: str

    industry: str

    ticker: str

    type: str

    market: str

    seniority: str
    """Investment grade bonds can either be secured or unsecured on the company's assets."""

    isin: str

    currency: str

    state: str

    moodys_rate: str

    snp_rate: str

    fitch_rate: str

    country: str

    ownership: str

    maturity: datetime

    next_payment: datetime

    coupon_type: str

    coupon_frequency: str

    coupon: float

    current_yield: float
    """Coupon divided by the price."""

    ytm_ytc: float
    """Yield to date or Yield to call."""

    price: float

    available: float

    _rating: Rating = field(default=None, init=False)

    def __post_init__(self)-> None:
        self.maturity = datetime.strptime(self.maturity, "%d-%m-%Y")
        self.next_payment = datetime.strptime(self.next_payment, "%d-%m-%Y")
        self.coupon = self._prep_coupon(self.coupon)
        self.current_yield = round(float(self.current_yield) / 100, 5)
        self.ytm_ytc = round(float(self.ytm_ytc) / 100, 5)
        self.price = round(float(self.price), 4)
        self.available = round(float(self.available), 4)
        self.country = self._prep_country(self.country)

        self._rating = Rating(self.snp_rate)

    def _prep_coupon(self, value)-> float:
        coupon = value.replace("%", "")
        if "+" in coupon:
            coupon = coupon.split("+")[1]

        return float(coupon) / 100

    def _prep_country(self, value: str)-> str:
        if value == "UK":
            return "GB"

        if value == "USA":
            return "US"

        return COUNTRIES[value] if value in COUNTRIES else value

    def get_properties(self):   
        return [i for i in self.__dict__.keys() if i[:1] != "_"]

    def get_maturity_months(self)-> int:
        # diff = self.maturity - datetime.now()

        return floor((self.maturity - datetime.now()).days / 30)

    def get_maturity_years(self)-> int:
        # diff = self.maturity - datetime.now()

        return floor((self.maturity - datetime.now()).days / 365)

    def is_rate(self, rate: str)-> bool:
        return self._rating == Rating(rate)

    def is_a_rate(self)-> bool:
        return self._rating.is_a_rate()

    def is_b_rate(self)-> bool:
        return self._rating.is_b_rate()

    def is_c_rate(self)-> bool:
        return self._rating.is_c_rate()
    
    def is_investment_grade(self)-> bool:
        return self._rating.is_investment_grade()

    def is_high_yield_grade(self)-> bool:
        return self._rating.is_high_yield_grade()

    def is_premium(self)-> bool:
        return self.price > 100

    def is_discount(self)-> bool:
        return self.price < 100

    def is_available(self)-> bool:
        return self.available > 0
