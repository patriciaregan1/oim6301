import marimo

__generated_with = "0.24.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The Question:
    """)
    return


app._unparsable_cell(
    r"""
    1. Who would use this, and what decision does it help them make? Two or three sentences, in words somebody outside this course would understand.
    """,
    name="_"
)


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


app._unparsable_cell(
    r"""
    2.  Before you ask your agent anything, open the API's address in your browser and read what comes back. Then write how you would solve it: the steps, in order, in plain words, in five lines or more. Then answer these:

    Which functions will your tool need? For each, what goes in and what comes out?
    Which addresses will they request?
    How will you know you have every record?
    Which check will you use in section 6, and which two numbers should agree?
    """,
    name="_"
)


app._unparsable_cell(
    r"""
    1. -Set the county to Middlesex, budget to 700000 maximum, tax mamimum to 8000, and fiscal year to 2026
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

    """,
    name="_"
)


app._unparsable_cell(
    r"""
    csv_columns = 
    """,
    name="_"
)


@app.cell
def _():
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    """)
    return


if __name__ == "__main__":
    app.run()
