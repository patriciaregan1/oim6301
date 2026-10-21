import marimo

__generated_with = "0.24.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import requests

    return mo, requests


@app.cell
def _():
    import csv

    import altair as alt
    import polars as pl

    return (csv,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The Question:
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    1.Who would use this, and what decision does it help them make? Two or three sentences, in words somebody outside this course would understand.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Any individual, family, or couple looking to buy a home in Massachusetts. It is especially helpful for first-term homebuyers. It will help them understand which countys are within their budget and give them a clear understanding of cost per county.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    My Plan Before AI
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    2.  Before you ask your agent anything, open the APIs address in your browser and read what comes back. Then write how you would solve it: the steps, in order, in plain words, in five lines or more. Then answer these:

    Which functions will your tool need? For each, what goes in and what comes out?
    Which addresses will they request?
    How will you know you have every record?
    Which check will you use in section 6, and which two numbers should agree?
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    1. Set the county to Middlesex, budget to 700000 maximum, tax mamimum to 8000, and fiscal year to 2026
    - Use the API to retrieve all towns in the Middlesex county,with name, population, income, value, bill
    - Retrieve each towns property tax history and find the average home value, residental tax rate, and average property bill tax of 2026 n
    - Compare each towns average home value against the 700000 maximum and average tax bill against the 8000 yearly limit
    - Keep only the homes that meet both constraints
    - Display the result in a table showing each qualifying town with average home value, residental tax rate, and -average bill , with the cheapest bill first
    - Write one quick sentence that summarizes the table using simple terms with the numbers in it
    - Allow the couple to edit the county, budget, tax and fiscal year without changing the code

    2. One function to get all the towns in the county : def get_towns(county):using town names and page settings as inputs and returning town names and pagnition details : params={"county": county, "per_page": x}
     Second function will return each towns tax history by taking its towns code as the input and returning annual home value, tax rates and bill . Third function will filter and sort the towns based on budget and annual tax limit
    3. First request /ma/towns?county=Middlesex to retrieve the towns in the Middlesex county. Then for each town request /ma/towns/{dor_code}/history for tax rates and single family bills by fiscal year
    4. I will know I have every record by checking the pagnition information in the first response which will tell me the total number of towns and towns per page
    5. Check: the number of records you collected equals the total the API reports
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Inputs
    """)
    return


@app.cell
def _():
    county = "Middlesex"
    budget_dollars = 700000
    tax_limit_dollars = 8000
    fiscal_year = 2026
    return budget_dollars, county, fiscal_year, tax_limit_dollars


@app.cell
def _(requests):
    def get_towns(county):
        first_reply = requests.get(
            "https://oim.zhili.dev/ma/towns",
            params={"county": county, "page": 1, "per_page": 100}
        ).json()

        towns = first_reply["items"]
        total_pages = first_reply["pagination"]["pages"]

        for page_number in range(2, total_pages + 1):
            next_reply = requests.get(
                "https://oim.zhili.dev/ma/towns",
                params={"county": county, "page": page_number, "per_page": 100}
            ).json()
            towns = towns + next_reply["items"]

        return towns, first_reply["pagination"]["total"] 


    return (get_towns,)


@app.cell
def _(county, get_towns):
    middlesex_towns, middlesex_total = get_towns(county)
    len(middlesex_towns) == middlesex_total
    return (middlesex_towns,)


@app.cell
def _(middlesex_towns):
    middlesex_towns[0]
    return


@app.cell
def _(requests):
    _check = requests.get("https://oim.zhili.dev/ma/towns/002/history").json()
    _check
    return


@app.cell
def _(requests):
    def get_town_history(dor_code):
        reply = requests.get(f"https://oim.zhili.dev/ma/towns/{dor_code}/history").json()
        return reply["years"]

    return (get_town_history,)


@app.cell
def _(fiscal_year, get_town_history, middlesex_towns):
    town_2026_figures = []
    skipped_towns = 0

    for town in middlesex_towns:
        history = get_town_history(town["dor_code"])
        found = False
        for year in history:
            if year["fiscal_year"] == fiscal_year:
                record = {
                    "name": town["name"],
                    "average_single_family_value_dollars": year["average_single_family_value_dollars"],
                    "residential_rate_per_thousand": year["residential_rate_per_thousand"],
                    "average_single_family_bill_dollars": year["average_single_family_bill_dollars"],
                }
                town_2026_figures.append(record)
                found = True
        if found == False:
            skipped_towns = skipped_towns + 1

    #town_2026_figures
    return (town_2026_figures,)


@app.cell
def _(budget_dollars, tax_limit_dollars, town_2026_figures):
    qualifying_towns = []

    for _record in town_2026_figures:
        if _record["average_single_family_value_dollars"] <= budget_dollars and _record["average_single_family_bill_dollars"] <= tax_limit_dollars:
            qualifying_towns.append(_record)

    qualifying_towns.sort(key=lambda r: r["average_single_family_bill_dollars"])

    #qualifying_towns
    return (qualifying_towns,)


@app.cell
def _(csv, mo, qualifying_towns):
    csv_columns = [
        "name",
        "average_single_family_value_dollars",
        "residential_rate_per_thousand",
        "average_single_family_bill_dollars",
    ]
    ma_taxes_csv = mo.notebook_dir().parent / "data" / "ma_taxes.csv"
    ma_taxes_csv.parent.mkdir(exist_ok=True)

    with open(ma_taxes_csv, "w", newline="", encoding="utf-8") as _file:
        _writer = csv.DictWriter(_file, fieldnames=csv_columns)
        _writer.writeheader()
        _writer.writerows(qualifying_towns)

    ma_taxes_csv.name
    return


if __name__ == "__main__":
    app.run()
