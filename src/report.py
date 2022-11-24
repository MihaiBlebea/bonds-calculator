from dataclasses import dataclass
from pandas import DataFrame
from src.bonds import Bonds, bonds


@dataclass
class Report:
    
    bonds: Bonds

    def _fmt_percentage(self, val)-> str:
        return f"{round(val * 100, 2)}%"

    def _fmt_money(self, val)-> str:
        return f"{round(val, 2):,}"

    def _as_df(self, b: Bonds)-> DataFrame:
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

        return self._as_df(b)

    def simulate(self, ticker: str = None, isin: str = None, amount_invested: int = 0, reinvest: bool = True)-> DataFrame:
        if ticker is not None:
            bond = self.bonds.find_by_ticker(ticker)
            assert bond is not None, "Could not find bond"

        if isin is not None:
            bond = self.bonds.find_by_isin(isin)
            assert bond is not None, "Could not find bond"

        assert amount_invested > 0, "Amount invested must be greater than £0"
        
        template = "Holding this bond to maturity and investing {amount} will yield in {years} years and {months} months a total amount of {total}"
        return template.format(
            amount=amount_invested,
            years=bond.get_maturity_years(),
            months=lambda: bond.get_maturity_months() % 12,
            total=bond.get_total_yield(amount_invested),
        )
