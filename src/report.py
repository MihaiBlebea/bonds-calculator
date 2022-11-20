from dataclasses import dataclass
from pandas import DataFrame
from src.bond import Bond
from src.bonds import Bonds


@dataclass
class Report:
    
    bonds: Bonds

    def _fmt_percentage(self, val)-> str:
        return f"{round(val * 100, 2)}%"

    def _fmt_money(self, val)-> str:
        return f"{round(val, 2):,}"

    def generate_report(self, sort = None, direction = "desc")-> DataFrame:
        b = self.bonds.only_discount_price()\
            .only_bond_type()\
            .only_available()

        if sort is not None:
            match sort:
                case "length":
                    b.sort_by_length(direction)
                case "maturity":
                    b.sort_by_maturity(direction)
                case "score":
                    b.sort_by_rating_score(direction)
                case "yield":
                    b.sort_by_total_yield(direction)
                case "risk":
                    b.sort_by_risk_score(direction)

        data = []
        for bond in b:
            data.append([
                bond.ticker,
                bond.company, 
                self._fmt_money(bond.price), 
                self._fmt_money(bond.get_total_yield()), 
                self._fmt_percentage(bond.get_maturity_growth()), 
                f"{bond.get_maturity_months()} months",
                bond.is_investment_grade(),
                bond.get_rating_score(),
                bond.get_risk_score()
            ])

        columns=["Ticker", "Company", "Lose", "Win", "Rate", "Maturity", "Investable", "Rating score", "Risk"]

        return DataFrame(data, columns=columns)
