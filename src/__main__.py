from pprint import pprint
import cli.app
import csv
from src.bond import Bond
from src.bonds import Bonds, bonds


def load_bonds_from_csv(file_path: str)-> Bonds:
    """Read CSV file, and return content as bonds collection."""
    b = bonds()
    with open(file_path, newline="") as csvfile:
        spamreader = csv.reader(csvfile, delimiter=",", quotechar="\"")
        [ b.append(Bond(*row)) for i, row in enumerate(spamreader) if i != 0 ]

    return b

def simulate(b: Bonds, init_amount: int):
    print(f"Simulate investing £{init_amount:,} in bonds")

@cli.app.CommandLineApp
def bond_calc(app):
    file = app.params.file
    output = app.params.output
    based = app.params.based
    coupon = app.params.coupon 
    output_file = app.params.output_file
    maturity = app.params.maturity
    goodgrade = app.params.goodgrade
    badgrade = app.params.badgrade
    cmd = app.params.cmd # use this for positionl argument nr 1

    b = load_bonds_from_csv(file)

    b = b.only_secured_seniority()\
        .only_bond_type()\
        .only_country(based)\
        .only_fixed_coupon()\
        .only_available()

    if coupon is not None:
        b = b.only_coupon_gt(coupon)

    if goodgrade:
        b = b.only_good_grade()
    elif badgrade:
        b = b.only_bad_grade()

    if maturity is not None:
        assert maturity in ["s", "m", "l"], "Maturity value must be either one of s, m or l."
        b = b.only_maturity(maturity)
    
    if cmd == "simulate":
        amount = app.params.amount
        simulate(b, amount)
        exit(0)

    match output:
        case "dataframe":
            print(b.to_df())
            if output_file is not None and ".csv" in output_file:
                b.to_df().to_csv(output_file)
        case "ticker":
            pprint(b.to_tickers())
        case "company":
            pprint(b.to_company_names())
        case _:
            pprint(b.to_df())


bond_calc.add_param("-f", "--file", help="csv file to load the data from", required=True)

bond_calc.add_param("-o", "--output", help="output format", default="dataframe")

bond_calc.add_param("-of", "--output_file", help="output file, can work only with -o as dataframe", default=None)

bond_calc.add_param("-b", "--based", help="bond based in country", default="GB")

bond_calc.add_param("-c", "--coupon", help="coupon must be greater than", default=None, type=float)

bond_calc.add_param("-m", "--maturity", help="max maturity level [s - short, m - medium, l - long]", default=None)

bond_calc.add_param("-gg", "--goodgrade", help="only good grade bonds", default=False, action="store_true")

bond_calc.add_param("-bg", "--badgrade", help="only bad grade bonds", default=False, action="store_true")

bond_calc.add_param("-a", "--amount", help="amount in £ to invest in bonds [just for simulating]", type=int, default=20_000)

bond_calc.add_param("cmd", help="action to be completed", choices=["simulate"], nargs="?", default=None)

def main():
    try:
        bond_calc.run()
    except Exception as err:
        print(err)

if __name__ == "__main__":
    main()