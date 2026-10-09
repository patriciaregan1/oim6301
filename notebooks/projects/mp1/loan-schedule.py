# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "marimo",
# ]
# ///
"""Mini Project 1.
"""

import marimo

__generated_with = "0.24.2"
app = marimo.App(width="medium", sql_output="polars")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Mini Project 1

    Your choice of project, what each one asks for, the due date and how it is graded are on the Mini Project 1 page of the course site, linked from the calendar. This notebook is the shape to build it in. Keep the headings, and replace each line in italics with your own.

    Save it in your course repository as `projects/mp1/<your-tool>.py`, named for what it does, such as `loan-schedule.py`, and open it with `uv run marimo edit`.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 1. The Question

    *Who would use this, and what decision does it help them make? Two or three sentences, in words somebody outside this course would understand.*
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    This is a side by side calculation of two mortage options, anybody looking to sign a mortgage (such as the friend looking to buy a condo) can refer to this list to help decide which option is better for them. The decision they are making is between a 30 year or 15 year mortgage, and the comparison will help them understand the trade-offs between monthly payments and built up interest.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 2. My Plan Before AI

    *Before you ask your agent anything, write how you would solve it: the steps, in order, in plain words, in five lines or more. Then answer these two questions:*

    - *What does your loop carry from one step to the next, the way a running total carries its sum?*
    - *Which check will you use in section 6, and which two numbers should agree?*

    *Commit this notebook with the message `mp1: plan before AI`.*
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    First I would set up the inputs (that will need to be changed upon the lendors quote) :
    loan_amount = 400000
    annual_rates = {30: 0.0703, 15: 0.0642}.
    Then, set up 2 for-loops, the outer loop that runs once per loan term and once per month.
    I would calculate the rate per term in the outer loop:  loan_amount * r / (1 - (1 + r) ** -n) - this will run once per row.
    Then I would create a running list for rows per month, so the code will run once per every month.
    This will compute interest on the current balance, then subtracted by principale paid.
    Finally, I would run a check to make sure the balance is fully paid off, and the sum of principale and loan amount equal eachother.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 3. Inputs

    Every number the project starts from goes in the cell below, and nowhere else, so that changing one input changes every result after it.

    Copy in the default inputs for your project from the Mini Project 1 page. If you chose your own project, type your data in here, or ask your agent to generate it with `faker`. The required part reads no file.
    """)
    return


@app.cell
def _():
    loan_amount = 400000
    annual_rates = {30: 0.0703, 15: 0.0642}
    return annual_rates, loan_amount


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 4. The Work

    Add as many cells as you need. Try each step yourself before you ask your agent, and commit as you go.
    """)
    return


@app.cell
def _(annual_rates, loan_amount):
    schedules = {}
    payments = {}
    total_interest = {}
    principal_paid = {}
    for years, rate in annual_rates.items():
        monthly_rate = rate / 12
        num_payments = years * 12  # total count of payments in this loan
        monthly_payment = loan_amount * monthly_rate / (1 - (1 + monthly_rate) ** -num_payments)
        payments[years] = monthly_payment
        balance = loan_amount
        schedule = []
        total_paid_interest = 0
        total_principal_paid = 0
        for payment_number in range(num_payments):  # walking through each individual month
            interest = round(balance * monthly_rate, 2)
            principal = round(monthly_payment - interest, 2)
            balance = round(balance - principal, 2)
            total_paid_interest = total_paid_interest + interest
            total_principal_paid = total_principal_paid + principal
            schedule.append(balance)
        schedules[years] = schedule
        total_interest[years] = total_paid_interest
        principal_paid[years] = total_principal_paid
    return payments, principal_paid, total_interest


@app.cell
def _(annual_rates, loan_amount, payments, total_interest):
    extra_payment = 200
    months_with_extra = {}
    interest_with_extra = {}

    for loan_term, loan_rate in annual_rates.items():
        monthly_rate_extra = loan_rate / 12
        new_payment = payments[loan_term] + extra_payment
        remaining_balance = loan_amount
        month_count = 0
        interest_paid_extra = 0
        while remaining_balance > 0:
            month_interest = round(remaining_balance * monthly_rate_extra, 2)
            month_principal = new_payment - month_interest
            if month_principal > remaining_balance:
                month_principal = remaining_balance
            remaining_balance = round(remaining_balance - month_principal, 2)
            interest_paid_extra = interest_paid_extra + month_interest
            month_count = month_count + 1
        months_with_extra[loan_term] = month_count
        interest_with_extra[loan_term] = interest_paid_extra

    for loan_term in annual_rates:
        original_months = loan_term * 12
        months_saved = original_months - months_with_extra[loan_term]
        interest_saved = total_interest[loan_term] - interest_with_extra[loan_term]
        print(f"{loan_term}-year loan: paying off {months_saved} months early, saving ${interest_saved:,.2f} in interest")
    return


@app.cell
def _():
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 5. The Answer

    *A table of your results in the cell below, printed with `print` and f-strings, then one sentence here that answers the question in section 1, with the number in it.*
    """)
    return


@app.cell
def _(annual_rates, payments, total_interest):
    for term, term_rate in annual_rates.items():
        print(f"{term}-year loan: payment ${payments[term]:,.2f}/month, total interest paid ${total_interest[term]:,.2f}")
    return


@app.cell
def _(payments, total_interest):
    total_cost_15 = payments[15]
    total_cost_30 = payments [30] 
    total_interest_15 = total_interest [15] 
    total_interest_30 = total_interest [30]
    return total_cost_15, total_cost_30, total_interest_15, total_interest_30


@app.cell
def _(total_cost_15, total_cost_30, total_interest_15, total_interest_30):
    monthly_difference = total_cost_15 - total_cost_30 
    interest_savings = total_interest_30 - total_interest_15 

    return interest_savings, monthly_difference


@app.cell
def _(interest_savings, monthly_difference):
    f"The 15-year loan costs ${monthly_difference:,.2f} more per month, but saves ${interest_savings:,.2f} in interest over the life of the loan."
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 6. How I Know These Numbers Are Right

    *At least one check that reaches a result a second, independent way. Name what you compared and what came out.*
    """)
    return


@app.cell
def _(loan_amount, principal_paid):
    round(principal_paid[30]) == loan_amount, round(principal_paid[15]) == loan_amount
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    I checked that the sum of every month's principal payments equals the original loan amount($400000).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    I found that both the loans were off due to rounding in the monthly payment schedule.
    """)
    return


@app.cell
def _():
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 7. Working With the Agent

    *Pick one piece of AI output you did not accept as-is. What did it give you, what did you change, and how did you know? Point to the commit or the cell.*

    *If the agent got it right the first time: what did you do to verify that?*
    """)
    return


@app.cell
def _():
    # My code in line 8 of section 2 would not run, I had asked the AI to help me with next step, which was calculating the monthly payment for each term, the AI wrongly gave me the code monthly_payments = loan_amount + monthly_rate/ (1+ monthly_rate) ** - number_of_payments, I had not fed it my original code that labelled the variables, so the AI gave random generic names that fit the description. I realized this was wrong because I have to slowly read the code line by line and saw that number_of_payments was a new label
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 8. Going Further

    *Take at least one step past the main task, in any direction, and use your agent as much as you like. It does not have to work. State what you tried, what you found, and where it is in this notebook.*
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Pay an extra 200 every month. How many months, and how much interest, does that save on each loan?
    """)
    return


if __name__ == "__main__":
    app.run()
