import typer
import numpy as np
import pandas as pd

from data import data

app = typer.Typer()


@app.command()
def create_df(month_year: str):
    month_year = month_year.lower()

    df = pd.DataFrame(data=data)
    df.set_index("bill", inplace=True)
    df.to_csv(f"bills_by_month_year\{month_year}.csv")


@app.command()
def new_bill(month_year_year: str, bill: str, amount: float, date: str):
    bill = bill.lower()
    month_year = month_year.lower()
    new_row = pd.Series({"bill": bill, "payment": amount, "date": date})
    df = get_db(month_year)
    df = pd.concat([df, new_row.to_frame().T], ignore_index=True)
    df.set_index("bill", inplace=True)
    df.to_csv(f"bills_by_month_year\{month_year}.csv")
    print(df)


@app.command()
def del_bill(month_year: str, bill: str):
    bill = bill.lower()
    month_year = month_year.lower()
    df = get_db(month_year)
    df.set_index("bill", inplace=True)
    df = df.drop(bill)
    df.to_csv(f"bills_by_month_year\{month_year}.csv")
    print(df)


@app.command()
def enter_amount(month_year: str, bill: str, amount: float, date: str):
    bill = bill.lower()
    month_year = month_year.lower()
    df = get_db(month_year)
    df.set_index("bill", inplace=True)
    df.loc[[bill], ["payment"]] = amount
    df.loc[[bill], ["date"]] = date
    df.to_csv(f"bills_by_month_year\{month_year}.csv")
    print(df)


@app.command()
def get_db(month_year: str, display: bool = False):
    df = pd.read_csv(f"bills_by_month_year\{month_year}.csv")
    if display:
        print(df)
    return df


@app.command()
def get_bill(month_year: str, bill: str):
    bill = bill.lower()
    month_year = month_year.lower()
    df = get_db(month_year)
    df.set_index("bill", inplace=True)
    print(df.loc[bill])

@app.command()
def bills_total(month_year: str, bill: str):
    month_year = month_year.lower()
    bill = bill.lower()
    df = get_db(month_year)
    df.set_index("bill", inplace=True)
    print(f"Total payout for month is: ${sum(df[bill].tolist())}")

if __name__ == "__main__":
    app()
