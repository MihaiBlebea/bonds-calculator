from __future__ import annotations
from typing import List, Callable
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

        keys = [ attr for attr in dir(self[0]) if attr[0] != "_" ]
        columns = [ attr.replace("_", " ").title() for attr in keys ]
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
        return self._only_this(lambda b: b.country == "UK")

    def only_public_companies(self)-> Bonds:
        return self._only_this(lambda b: b.ownership == "Public")

    def only_private_companies(self)-> Bonds:
        return self._only_this(lambda b: b.ownership == "Private")

    def only_fixed_coupon(self)-> Bonds:
        return self._only_this(lambda b: b.coupon_type == "Fixed")

    def only_coupon_gt(self, value: float)-> Bonds:
        return self._only_this(lambda b: b.coupon > value)

    def only_available(self)-> Bonds:
        return self._only_this(lambda b: b.available > 0)
