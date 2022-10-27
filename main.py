from sqlite3 import DateFromTicks
import typer
import numpy as np
import pandas as pd

app = typer.Typer()


@app.command()
def create_df(month: str):
    month = month.lower()
    data = {
        "bill": [
            "car_payment",
            "cell_phone",
            "internet",
            "insurence",
            "credit_cards",
            "bank_loan",
            "ira",
            "google",
            "power",
            "water",
            "rent",
        ],
        "payment": 0,
    }
    df = pd.DataFrame(data=data)
    df.set_index("bill", inplace=True)
    df.to_csv(f"bills_by_month\{month}.csv")


# fix this
@app.command()
def new_bill(month: str, bill: str, amount: float):
    bill = bill.lower()
    month = month.lower()
    new_row = pd.Series({"bill": bill, "payment": amount})
    df = get_db(month)
    df = pd.concat([df, new_row.to_frame().T], ignore_index=True)
    df.set_index("bill", inplace=True)
    df.to_csv(f"bills_by_month\{month}.csv")
    print(df)


@app.command()
def enter_amount(month: str, bill: str, amount: float):
    bill = bill.lower()
    month = month.lower()
    df = get_db(month)
    df.set_index("bill", inplace=True)
    df.loc[[bill], ["payment"]] = amount
    df.to_csv(f"bills_by_month\{month}.csv")
    print(df)


@app.command()
def get_db(month: str, display: bool = False):
    df = pd.read_csv(f"bills_by_month\{month}.csv")
    if display:
        print(df)
    return df


@app.command()
def get_bill(month: str, bill: str):
    bill = bill.lower()
    month = month.lower()
    df = get_db(month)
    df.set_index("bill", inplace=True)
    print(df.loc[bill])


if __name__ == "__main__":
    app()
