from dataclasses import dataclass
from pandas import DataFrame
from src.bonds import Bonds


@dataclass
class Report:
    
    bonds: Bonds

    def _fmt_percentage(self, val)-> str:
        return f"{round(val * 100, 2)}%"

    def _fmt_money(self, val)-> str:
        return f"{round(val, 2):,}"

    def generate_report(self)-> DataFrame:
        b = self.bonds.only_discount_price()\
            .only_bond_type()\
            .only_available()

        b.sort_by_length()

        data = []
        for bond in b:
            data.append([
                bond.company, 
                self._fmt_money(bond.price), 
                self._fmt_money(bond.get_total_yield()), 
                self._fmt_percentage(bond.get_maturity_growth()), 
                bond.get_maturity_months(),
                bond.is_investment_grade(),
                bond.get_rating_score()
            ])

        columns=["Company", "Lose", "Win", "Rate", "Maturity (months)", "Investable", "Rating score"]

        return DataFrame(data, columns=columns)
