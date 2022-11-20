import click
import csv
from src.report import Report
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
@click.option("-s", "--sort", help="sort by", required=False, type=str)
@click.option("-a", "--asc", help="sort ascending", required=False, type=bool, is_flag=True)
@click.argument("file")
def report(file, sort: str, asc: bool):
    click.echo(f"Generating report")

    direction = "desc"
    if asc:
        direction = "asc"

    df = Report(load_bonds_from_csv(file)).generate_report(sort, direction)
    
    click.echo(df)


@click.command()
@click.option("-o", "--output", help="output file", required=False, default=None)
@click.option("-b", "--based", help="bond based in country", default=None)
@click.option("-c", "--coupon", help="coupon must be greater than", default=None, type=float)
@click.option("-cy", "--current-yield", help="current yield must be greater than", default=None, type=float)
@click.option("-mm", "--maturity-months", help="max maturity in months", default=None, type=int)
@click.option("-my", "--maturity-years", help="max maturity in years", default=None, type=int)
@click.option("-ig", "--investment-grade", help="only investment grade bonds", default=False, is_flag=True)
@click.option("-hg", "--high-yield-grade", help="only high yield grade bonds", default=False, is_flag=True)
@click.option("-p", "--premium", help="only premium price bonds", default=False, is_flag=True)
@click.option("-d", "--discount", help="only discount price bonds", default=False, is_flag=True)
@click.option("-a", "--available", help="only available bonds", default=False, is_flag=True)
@click.argument("file")
def filter(
    file: str, 
    output: str, 
    based: str, 
    coupon: float,
    current_yield: float, 
    maturity_months: int,
    maturity_years: int,
    investment_grade: bool, 
    high_yield_grade: bool, 
    premium: bool, 
    discount: bool, 
    available: bool)-> None:

    b = load_bonds_from_csv(file)

    if based is not None:
        b = b.only_country(based)

    if coupon is not None:
        b = b.only_coupon_gt(coupon)

    if current_yield is not None:
        b = b.only_current_yield_gt(current_yield)

    if investment_grade:
        b = b.only_investment_grade()
    elif high_yield_grade:
        b = b.only_high_yield_grade()

    if premium:
        b = b.only_premium_price()
    elif discount:
        b = b.only_discount_price()

    if maturity_months is not None:
        b = b.only_max_maturity_months(maturity_months)
    elif maturity_years is not None:
        b = b.only_max_maturity_years(maturity_years)

    if available:
        b = b.only_available()

    df = b.to_df()
    if df is None:
        click.echo(click.style("No bounds found", bg="red"))
        exit(0)

    if output is not None:
        df.to_csv(output, index=False)

    click.echo(df)

@click.group()
def cli():
    pass

cli.add_command(filter, "filter")

cli.add_command(report, "report")

def main():
    cli()

if __name__ == "__main__":
    main()