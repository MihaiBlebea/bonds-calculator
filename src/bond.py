from typing import Dict
from dataclasses import dataclass
from datetime import datetime
import pycountry


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

    def __post_init__(self)-> None:
        self.maturity = datetime.strptime(self.maturity, "%d-%m-%Y")
        self.next_payment = datetime.strptime(self.next_payment, "%d-%m-%Y")
        self.coupon = self._prep_coupon(self.coupon)
        self.current_yield = round(float(self.current_yield) / 100, 5)
        self.ytm_ytc = round(float(self.ytm_ytc) / 100, 5)
        self.price = round(float(self.price), 4)
        self.available = round(float(self.available), 4)
        self.country = self.__prep_country(self.country)

    def _prep_coupon(self, value)-> float:
        coupon = value.replace("%", "")
        if "+" in coupon:
            coupon = coupon.split("+")[1]

        return float(coupon) / 100

    def __prep_country(self, value: str)-> str:
        if value == "UK":
            return "GB"

        if value == "USA":
            return "US"

        return COUNTRIES[value] if value in COUNTRIES else value

