from __future__ import annotations
from typing import List, Callable
from datetime import datetime
from dateutil.relativedelta import relativedelta
from pandas import DataFrame
from src.bond import Bond


def bonds(*bonds: List[Bond])-> Bonds:
    """Bonds class factory function."""

    b = Bonds()
    if len(bonds) == 0:
        return b

    if isinstance(bonds[0], list):
        bonds = bonds[0]

    for b in bonds:
        assert isinstance(b, Bond), "Not instance of Bond class"
        bonds.append(b)

    return b

class Bonds(list):
    """Bonds is a collection of Bond models."""
    
    def __init__(self, *data: List[Bond]):
        super(Bonds, self).__init__(data)

    def __add__(self, bonds: Bonds)-> Bonds:
        res = Bonds()
        for b in self:
            res.append(b)

        for b in bonds:
            res.append(b)

        return res
    
    def _only_this(self, cb: Callable[[Bond], bool])-> Bonds:
        res = bonds()
        for b in self:
            if cb(b):
                res.append(b)

        return res

    def to_df(self)-> DataFrame | None:
        if len(self) == 0:
            return None

        keys = self[0].get_properties()
        columns = [ attr.title() for attr in keys ]
        data = []
        for b in self:
            data.append([ getattr(b, k) for k in keys ])

        return DataFrame(data, columns=columns)

    def to_tickers(self)-> List[str]:
        return [ b.ticker for b in self ]
    
    def to_company_names(self)-> List[str]:
        return [ b.company for b in self ]

    def only_secured_seniority(self)-> Bonds:
        return self._only_this(lambda b: "Secured" in b.seniority)

    def only_bond_type(self)-> Bonds:
        return self._only_this(lambda b: b.type == "Bond")

    def only_gbp_currency(self)-> Bonds:
        return self._only_this(lambda b: b.currency == "GBP")

    def only_uk_based(self)-> Bonds:
        return self._only_this(lambda b: b.country == "GB")

    def only_country(self, value: str)-> Bonds:
        return self._only_this(lambda b: b.country == value)

    def only_public_companies(self)-> Bonds:
        return self._only_this(lambda b: b.ownership == "Public")

    def only_private_companies(self)-> Bonds:
        return self._only_this(lambda b: b.ownership == "Private")

    def only_fixed_coupon(self)-> Bonds:
        return self._only_this(lambda b: b.coupon_type == "Fixed")

    def only_coupon_gt(self, value: float)-> Bonds:
        return self._only_this(lambda b: b.coupon > value)

    def only_current_yield_gt(self, value: float)-> Bonds:
        return self._only_this(lambda b: b.current_yield > value)

    def only_available(self)-> Bonds:
        return self._only_this(lambda b: b.available > 0)
    
    def only_max_maturity_months(self, months: int)-> Bonds:
        return self._only_this(lambda b: b.get_maturity_months() < months)

    def only_max_maturity_years(self, years: int)-> Bonds:
        return self._only_this(lambda b: b.get_maturity_years() < years)

    def only_investment_grade(self)-> Bonds:
        return self._only_this(lambda b: b.is_investment_grade())

    def only_high_yield_grade(self)-> Bonds:
        return self._only_this(lambda b: b.is_high_yield_grade())

    def only_premium_price(self)-> Bonds:
        return self._only_this(lambda b: b.is_premium())

    def only_discount_price(self)-> Bonds:
        return self._only_this(lambda b: b.is_discount())

    def only_available(self)-> Bonds:
        return self._only_this(lambda b: b.is_available())

    def sort_by_maturity(self, direction = "desc")-> None:
        self.sort(key=lambda x: x.maturity, reverse=True if direction == "desc" else False)

    def sort_by_length(self, direction = "desc")-> None:
        self.sort(key=lambda x: x.get_maturity_months(), reverse=True if direction == "desc" else False)

    def sort_by_rating_score(self, direction = "desc")-> None:
        self.sort(key=lambda x: x.get_rating_score(), reverse=True if direction == "desc" else False)

    def sort_by_total_yield(self, direction = "desc")-> None:
        self.sort(key=lambda x: x.get_total_yield(), reverse=True if direction == "desc" else False)

    def sort_by_risk_score(self, direction = "desc")-> None:
        self.sort(key=lambda x: x.get_risk_score(), reverse=True if direction == "desc" else False)

    def first(self, count: int = 1)-> Bonds:
        b = bonds()
        [ b.append(bond) for bond in self[0:count] ]

        return b

    def find_by_ticker(self, ticker: str)-> Bond | None:
        for b in self:
            if b.ticker == ticker:
                return b

        return None

    def find_by_isin(self, isin: str)-> Bond | None:
        for b in self:
            if b.isin == isin:
                return b

        return None