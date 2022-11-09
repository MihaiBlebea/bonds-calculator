from pprint import pprint
import cli.app
import csv
from src.bond import Bond
from src.bonds import bonds


@cli.app.CommandLineApp
def bond_calc(app):
    file = app.params.file
    output = app.params.output

    b = bonds()
    with open(file, newline="") as csvfile:
        spamreader = csv.reader(csvfile, delimiter=",", quotechar="\"")
        for i, row in enumerate(spamreader):
            if i == 0:
                continue

            b.append(Bond(*row))

    b = b.only_secured_seniority()\
        .only_bond_type()\
        .only_uk_based()\
        .only_fixed_coupon()\
        .only_coupon_gt(0.05)\
        .only_available()

    match output:
        case "dataframe":
            print(b.to_df())
        case "ticker":
            pprint(b.to_tickers())
        case "company":
            pprint(b.to_company_names())
        case _:
            pprint(b.to_df())


bond_calc.add_param("-f", "--file", help="csv file to load the data from", required=True)

bond_calc.add_param("-o", "--output", help="output format", default="dataframe", )

if __name__ == "__main__":
    bond_calc.run()