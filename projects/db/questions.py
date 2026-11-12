import marimo

__generated_with = "0.24.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import duckdb
    import polars as pl
    from datetime import date

    return date, duckdb, mo, pl


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Babson Bean Café — Business Questions
    =
    Answered by asking `database.duckdb` through `ask`, a copy of the function in `build.py`.
    """)
    return


@app.cell
def _(date, mo):
    as_of = date(2026, 11, 8)
    mo.md(f"**as_of date: {as_of}.** Every \"last 30 days\" is the 30 days ending on this date, and \"last month\" is the last full calendar month before it.")
    return (as_of,)


@app.cell
def _(mo):
    database = mo.notebook_dir() / "database.duckdb"
    return (database,)


@app.cell
def _(database, duckdb):
    def ask(sql):
        with duckdb.connect(database, read_only=True) as _con:
            return _con.sql(sql).pl()

    return (ask,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    1. The three best-selling products last month, by units.
    -
    *(not yet answered)*
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    2. Revenue, cost and margin by menu category, with what the options earned counted in.
    -
    *(not yet answered)*
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    3. For each member: orders, total spent and average order, keeping members above the members' average. (three tables or more)
    -
    *(not yet answered)*
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    4. Every order's payments checked against its total, and a list of the orders where they do not match. (three tables or more) (checks a rule)
    -
    *(not yet answered)*
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    5. The members who joined and have never ordered.
    -
    *(not yet answered)*
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    6. The share of orders paid at least partly with points, for each month.
    -
    *(not yet answered)*
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    7. The products, available today or not, that have not sold in the last 60 days.
    -
    *(not yet answered)*
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    8. For each coffee and tea product, the average number of options on its lines, counting a line with no options as zero. (three tables or more)
    -
    *(not yet answered)*
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    9. My own question
    -
    *(not yet chosen)*
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    10. My own question
    -
    *(not yet chosen)*
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    1. How I Know These Numbers Are Right
    -
    *(to fill in after the 10 answers)*
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    2. Working With the Agent
    -
    *(to fill in after the 10 answers)*
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    3. Reading It Back
    -
    **The question I picked:** Question 2, *"Revenue, cost and margin by menu category, with what the options earned counted in, each option under the category of the product on its line."* It needs four tables: `order_lines`, `products`, `line_options` and `options`.

    **My prediction, before running anything.** The joins I plan to use are:

    ```sql
    FROM order_lines ol
    JOIN products p ON p.product_id = ol.product_id
    LEFT JOIN line_options lo ON lo.line_id = ol.line_id
    LEFT JOIN options opt ON opt.option_id = lo.option_id
    ```

    `order_lines` has 2,491 rows (shown in `build.py` section 4). Joining `products` does not change the row count: every order line has exactly one product, so that join is one-to-one.

    The row count only grows at the `line_options` join, because a line can carry 0, 1 or 2 options (`make_data.py` draws the option count from `[0, 0, 1, 1, 2]` for every line, so roughly 40% of lines get 0 options, 40% get 1, and 20% get 2). A `LEFT JOIN` keeps a line with 0 options as one row with nulls, so each line contributes `max(options on that line, 1)` rows. The `options` join after that does not fan out further, since `line_options.option_id` points at exactly one row in `options`.

    So I expect roughly: (lines with 0 options) × 1 + (lines with 1 option) × 1 + (lines with 2 options) × 2. With about 40%/40%/20% of 2,491 lines, that is about 996 + 996 + (498 × 2) ≈ **2,990 rows**, close to but a bit more than the 2,491 order lines, and well under 2,491 + 2,036 = 4,527 (what it would be if every line's options added a row instead of only the second one).

    **After running the joins (fill in once the 10 questions are answered):**

    - Actual row count: *TBD*
    - Did the prediction match? *TBD*
    - What one row of the final, grouped result means: *TBD*
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    4. Going Further
    -
    *(to fill in after the 10 answers)*
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    5. Time Spent
    -
    *(to fill in after the 10 answers)*
    """)
    return


if __name__ == "__main__":
    app.run()
