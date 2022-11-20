from typing import Dict, List
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

    id: str = field(default="", init=False)

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
        self.id = self._generate_id(self.company, self.coupon, self.maturity)

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

    def _generate_id(self, company: str, coupon: float, maturity: datetime)-> str:
        company_name = company.replace(" ", "_").replace(",", "").replace(".", "").lower().strip()
        rate = str(round(coupon * 100, 2)).replace(".", "_")
        maturity_date = maturity.strftime("%d_%m_%Y")
        return f"{company_name}-{rate}-{maturity_date}"

    def _calc_percentage_diff(self, initial: float, current: float)-> float:
        return abs(initial - current) / current

    def get_properties(self)-> List[str]:   
        return [i for i in self.__dict__.keys() if i[:1] != "_"]

    def get_maturity_months(self)-> int:
        return floor((self.maturity - datetime.now()).days / 30)

    def get_maturity_years(self)-> int:
        return floor((self.maturity - datetime.now()).days / 365)

    def get_total_yield(self)-> float:
        """Get the total amount of money returned at maturity, including intermediate coupons and final principal return."""
        yield_per_month = (self.price * self.current_yield) / 12
        return (yield_per_month * self.get_maturity_months()) + 100

    def get_maturity_growth(self)-> float:
        """Get the growth % between the initial price of a bond and the total money returned at maturity."""
        return self._calc_percentage_diff(self.price, self.get_total_yield())

    def get_rating_score(self)-> str:
        return self._rating.get_score()

    def get_risk_score(self)-> float:
        risk = 0
        if self.get_maturity_years() > 0:
            risk += round(self.get_maturity_years() / 3, 0)

        if self.is_public_company() is False:
            risk += 2

        if self.is_secured() is False:
            risk += 10

        if self.is_b_rate():
            risk += 5

        if self.is_c_rate():
            risk += 20

        return risk

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

    def is_public_company(self)-> bool:
        return self.ownership == "Public"

    def is_secured(self)-> bool:
        return "Secured" in self.seniority
