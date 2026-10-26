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

    return alt, csv, pl


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
    return


@app.cell
def _(mo):
    county_input = mo.ui.text(value="Middlesex", label="County")
    budget_input = mo.ui.number(value=700000, label="Budget maximum ($)")
    tax_input = mo.ui.number(value=8000, label="Tax maximum ($)")
    fiscal_year_input = mo.ui.number(value=2026, label="Fiscal year")

    mo.vstack([county_input, budget_input, tax_input, fiscal_year_input])
    return budget_input, county_input, fiscal_year_input, tax_input


@app.cell
def _(budget_input, county_input, fiscal_year_input, tax_input):
    county = county_input.value
    budget_dollars = budget_input.value
    tax_limit_dollars = tax_input.value
    fiscal_year = fiscal_year_input.value
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

    qualifying_towns
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
        for _record in qualifying_towns:
            _writer.writerow(_record)

    ma_taxes_csv.name
    return (ma_taxes_csv,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Answer
    """)
    return


@app.cell
def _(ma_taxes_csv, pl):
    town_table = pl.read_csv(ma_taxes_csv)
    town_table
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    print(f"{'Town':<15}{'Value ($)':>12}{'Rate':>8}{'Bill ($)':>10}")
    for _record in qualifying_towns:
        print(f"{_record['name']:<15}{_record['average_single_family_value_dollars']:>12,}{_record['residential_rate_per_thousand']:>8}{_record['average_single_family_bill_dollars']:>10,}")

    if len(qualifying_towns) > 0:
        cheapest = qualifying_towns[0]
        print(f"\nIn {county} county for fiscal year {fiscal_year}, {len(qualifying_towns)} towns have an average home value under ${budget_dollars:,} and an average yearly tax bill under ${tax_limit_dollars:,}, with {cheapest['name']} being the cheapest at ${cheapest['average_single_family_bill_dollars']:,} per year.")
    else:
        print(f"\nNo towns in {county} county meet a budget of ${budget_dollars:,} and a tax limit of ${tax_limit_dollars:,} for fiscal year {fiscal_year}.")
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    6. How I Know These Numbers Are Right
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    This check makes sure the number of town records I actually collected matches the total the API says exists, this confirms all towns are accounted for and none were lost due to pagination
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    7. Work With the Agent
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    writerows(qualifying_towns) was a one-line call that wrote the whole list at once. I replaced it with a for loop over qualifying_towns that calls writerow on each _record in turn , same result, one row written per pass through the loop.This wasn't exactly wrong for the agent to compute, but the task asks for for-loops instead of one-line calls.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    8. -Read it Back
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    qualifying_towns = []

    for _record in town_2026_figures:
        if _record["average_single_family_value_dollars"] <= budget_dollars and _record["average_single_family_bill_dollars"] <= tax_limit_dollars:
            qualifying_towns.append(_record)

    qualifying_towns.sort(key=lambda r: r["average_single_family_bill_dollars"])

    qualifying_towns
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    qualifying_towns = [] goes in, nothing comes out, this is a new empty list called qualifying_towns

    for_record in
    town_2026_figures:

    Goes in: the list town_2026_figures
    Comes out: nothing yet, each pass through the loop, and _record takes one record from that list

    if _record["average_single_family_value_dollars"] <= budget_dollars and _record["average_single_family_bill_dollars"] <= tax_limit_dollars:

    Goes in: two fields read by name from _records, plus budget_dollars and tax_limit_dollars.
        Comes out: True or False

    qualifying_towns.append(_record)

    Goes in: the current _record
    Comes out: nothing - ut just adds that record to qualifying_towns when the comdition was True

    qualifying_towns.sort(key=lambda r: r["average_single_family_bill_dollars"])

    Goes in: the list qualifying_towns
    Comes Out: nothing, this just reorders the list in place, cheapest bill first
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Line I had to ask the agent about: qualifying_towns.sort(key=lambda r: r["average_single_family_bill_dollars"])
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    lambda is a short throw away function that is used here to sort which fields to compare
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    print(f"{'Town':<15}{'Value ($)':>12}{'Rate':>8}{'Bill ($)':>10}")
    for _record in qualifying_towns:

    Goes in: an f-string with four text labels ('Town', 'Value', '$', 'Rate','Bill','$'each told how wide to print and way to line up.
    Comes Out: nothing is returned, print just displays one line of text (the column headings)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    I asked my agent about the <15 and >12 parts, these are formating instructions inside an f-string. <15 means "line up to the left in a space 15 characters wide," and >12 means "line up to the right in a space 12 characters wide "
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    8. Changing what the tool does
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    I am going to lower the budget maximum and tax maximum by 10%, I am expecting the results to decrease proportionally.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    I found that 10%  decrease was not a large enough difference to see any results, so then changed the maximums by increasing by 10% . I then found that 30 towns have a average home value under 840,000, which shows that a 10% increase gives homebuyers 11 more towns to choose from.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Where is it: my input cells have already ben converted to allow the couple to change them there selves, all I did was increase $700,000 by $140,000 and $8,000 by $800 to see the difference.
    """)
    return


@app.cell
def _():
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
 
    """)
    return


@app.cell
def _(county, get_towns):
    middlesex_towns, middlesex_total = get_towns(county)
    len(middlesex_towns) == middlesex_total
    return (middlesex_towns,)


@app.cell
def _(mo):
    mo.md(r"""
    Going Further: 10-Year Bill History for the Three Cheapest Towns
    """)
    return


@app.cell
def _(middlesex_towns, qualifying_towns):
    cheapest_three = qualifying_towns[0:3]

    cheapest_three_codes = []

    for _cheap_town in cheapest_three:
        for _town in middlesex_towns:
            if _town["name"] == _cheap_town["name"]:
                cheapest_three_codes.append({"name": _town["name"], "dor_code": _town["dor_code"]})

    cheapest_three_codes
    return (cheapest_three_codes,)


@app.cell
def _(cheapest_three_codes, get_town_history, pl):
    ten_year_rows = []

    for _code_record in cheapest_three_codes:
        _history = get_town_history(_code_record["dor_code"])
        _last_ten_years = _history[-10:]
        for _year in _last_ten_years:
            ten_year_rows.append({
                "name": _code_record["name"],
                "fiscal_year": _year["fiscal_year"],
                "average_single_family_bill_dollars": _year["average_single_family_bill_dollars"],
            })

    ten_year_df = pl.DataFrame(ten_year_rows)
    ten_year_df
    return (ten_year_df,)


@app.cell
def _(alt, ten_year_df):
    bill_history_chart = alt.Chart(ten_year_df).mark_line(point=True).encode(
        x=alt.X("fiscal_year:O", title="Fiscal year"),
        y=alt.Y("average_single_family_bill_dollars:Q", title="Average bill ($)"),
        color=alt.Color("name:N", title="Town"),
        tooltip=["name", "fiscal_year", "average_single_family_bill_dollars"],
    ).properties(
        title="10-Year Average Tax Bill: Three Cheapest Qualifying Towns",
        width=500,
        height=300,
    )

    bill_history_chart
    return


@app.cell
def _():
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Time Spent: about 8 hours in total
    """)
    return


if __name__ == "__main__":
    app.run()
