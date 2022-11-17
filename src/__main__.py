import click
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

@click.command()
@click.option("-a", "--amount", help="amount to invest", required=True, type=int)
def simulate(amount: int):
    click.echo(f"Simulate investing £{amount:,} in bonds")

@click.command()
@click.option("-o", "--output", help="output file", required=False, default=None)
@click.option("-b", "--based", help="bond based in country", default=None)
@click.option("-c", "--coupon", help="coupon must be greater than", default=None, type=float)
@click.option("-m", "--maturity", help="max maturity level [s - short, m - medium, l - long]", default=None)
@click.option("-ig", "--investment-grade", help="only investment grade bonds", default=False, is_flag=True)
@click.option("-hg", "--high-yield-grade", help="only high yield grade bonds", default=False, is_flag=True)
@click.option("-p", "--premium", help="only premium price bonds", default=False, is_flag=True)
@click.option("-d", "--discount", help="only discount price bonds", default=False, is_flag=True)
@click.option("-a", "--available", help="only available bonds", default=False, is_flag=True)
@click.argument("file")
def filter(file, output, based, coupon, maturity, investment_grade, high_yield_grade, premium, discount, available):

    b = load_bonds_from_csv(file)

    if based is not None:
        b = b.only_country(based)

    if coupon is not None:
        b = b.only_coupon_gt(coupon)

    if investment_grade:
        b = b.only_investment_grade()
    elif high_yield_grade:
        b = b.only_high_yield_grade()

    if premium:
        b = b.only_premium_price()
    elif discount:
        b = b.only_discount_price()

    if maturity is not None:
        if maturity not in ["s", "m", "l"]:
            raise click.BadParameter("Should be one of s, m, l")
        b = b.only_maturity(maturity)

    if available:
        b = b.only_available()

    if output is not None:
        b.to_df().to_csv(output, index=False)

    click.echo(b.to_df())

@click.group()
def cli():
    pass

cli.add_command(filter, "filter")

cli.add_command(simulate, "simulate")

def main():
    cli()

if __name__ == "__main__":
    main()