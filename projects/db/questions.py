import marimo

__generated_with = "0.24.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import duckdb
    import matplotlib.pyplot as plt
    from datetime import date, timedelta

    return date, duckdb, mo, plt, timedelta


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Babson Bean Café — Business Questions
    =
    Answered by asking `database.duckdb` through `ask`, a copy of the function in `build.py`.
    """)
    return


@app.cell
def _(date, mo, timedelta):
    as_of = date(2026, 11, 8)
    month_start = date(as_of.year, as_of.month, 1)
    last_month_end = month_start - timedelta(days=1)
    last_month_start = date(last_month_end.year, last_month_end.month, 1)
    last_30_start = as_of - timedelta(days=29)
    last_60_start = as_of - timedelta(days=59)
    mo.md(f"**as_of date: {as_of}.** The last 30 and 60 days include this date; last month is {last_month_start:%B %Y}.")
    return as_of, last_30_start, last_60_start, last_month_start, month_start


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
    **Answer:** In October 2026, Latte sold 31 units, Green Tea 27 and Croissant 26.
    """)
    return


@app.cell
def _(ask, last_month_start, month_start):
    q1_result = ask(f"""
        SELECT p.name, SUM(ol.quantity) AS units
        FROM order_lines ol
        JOIN orders o ON o.order_id = ol.order_id
        JOIN products p ON p.product_id = ol.product_id
        WHERE CAST(o.ordered_at AS DATE) >= DATE '{last_month_start}'
          AND CAST(o.ordered_at AS DATE) < DATE '{month_start}'
        GROUP BY p.product_id, p.name
        ORDER BY units DESC, p.name
        LIMIT 3
    """)
    q1_result
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    2. Revenue, cost and margin by menu category, with what the options earned counted in.
    -
    **Answer:** Food has the highest margin at $2,947.85; its total revenue is $6,934.01 and total cost is $3,986.16.
    """)
    return


@app.cell
def _(ask):
    q2_result = ask("""
        SELECT category,
               product_revenue + option_revenue AS revenue,
               product_cost + option_cost AS cost,
               margin
        FROM category_performance
        ORDER BY margin DESC
    """)
    q2_result
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    3. For each member: orders, total spent and average order, keeping members above the members' average. (three tables or more)
    -
    **Answer:** I read “above the members' average” as total lifetime spend above the average total spend of members who ordered; that benchmark is $365.69, and 23 members are above it.
    """)
    return


@app.cell
def _(ask):
    q3_result = ask("""
        WITH option_totals AS (
            SELECT line_id, SUM(price_charged) AS option_price
            FROM line_options
            GROUP BY line_id
        ), order_totals AS (
            SELECT ol.order_id,
                   SUM(ol.quantity * (ol.price_charged + COALESCE(ot.option_price, 0))) AS order_total
            FROM order_lines ol
            LEFT JOIN option_totals ot ON ot.line_id = ol.line_id
            GROUP BY ol.order_id
        ), member_spend AS (
            SELECT o.member_id,
                   COUNT(*) AS order_count,
                   SUM(t.order_total) AS total_spent,
                   AVG(t.order_total) AS avg_order
            FROM orders o
            JOIN order_totals t ON t.order_id = o.order_id
            WHERE o.member_id IS NOT NULL
            GROUP BY o.member_id
        )
        SELECT m.member_id, m.first_name, s.order_count,
               ROUND(s.total_spent, 2) AS total_spent,
               ROUND(s.avg_order, 2) AS avg_order
        FROM member_spend s
        JOIN members m ON m.member_id = s.member_id
        WHERE s.total_spent > (SELECT AVG(total_spent) FROM member_spend)
        ORDER BY s.total_spent DESC
    """)
    q3_result
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    4. Every order's payments checked against its total, and a list of the orders where they do not match. (three tables or more) (checks a rule)
    -
    **Answer:** Two orders break the rule: order 10 is overpaid by $5.00 ($54.22 paid on $49.22 of sales), and order 25 is overpaid by $5.00 ($40.41 paid on $35.41 of sales).
    """)
    return


@app.cell
def _(ask):
    q4_result = ask("""
        WITH option_totals AS (
            SELECT line_id, SUM(price_charged) AS option_price
            FROM line_options
            GROUP BY line_id
        ), order_totals AS (
            SELECT ol.order_id,
                   SUM(ol.quantity * (ol.price_charged + COALESCE(ot.option_price, 0))) AS order_total
            FROM order_lines ol
            LEFT JOIN option_totals ot ON ot.line_id = ol.line_id
            GROUP BY ol.order_id
        ), paid_totals AS (
            SELECT order_id, SUM(amount) AS paid
            FROM payments
            GROUP BY order_id
        )
        SELECT o.order_id,
               ROUND(t.order_total, 2) AS order_total,
               ROUND(p.paid, 2) AS paid,
               ROUND(p.paid - t.order_total, 2) AS difference
        FROM orders o
        JOIN order_totals t ON t.order_id = o.order_id
        JOIN paid_totals p ON p.order_id = o.order_id
        WHERE ROUND(t.order_total, 2) <> ROUND(p.paid, 2)
        ORDER BY o.order_id
    """)
    q4_result
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    5. The members who joined and have never ordered.
    -
    **Answer:** Five members have never ordered: Lauren (46), Debbie (47), Andrea (48), Tiffany (49) and Angela (50).
    """)
    return


@app.cell
def _(ask):
    q5_result = ask("""
        SELECT m.member_id, m.first_name, m.join_date
        FROM members m
        WHERE NOT EXISTS (
            SELECT 1 FROM orders o WHERE o.member_id = m.member_id
        )
        ORDER BY m.member_id
    """)
    q5_result
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    6. The share of orders paid at least partly with points, for each month.
    -
    **Answer:** Points were used on 20.00% of November 2026 orders (4 of 20); the monthly query treats an order as points-paid if any of its payments used points.
    """)
    return


@app.cell
def _(ask):
    q6_result = ask("""
        WITH monthly_orders AS (
            SELECT DATE_TRUNC('month', o.ordered_at)::DATE AS month,
                   o.order_id,
                   MAX(CASE WHEN p.method = 'points' THEN 1 ELSE 0 END) AS used_points
            FROM orders o
            JOIN payments p ON p.order_id = o.order_id
            GROUP BY month, o.order_id
        )
        SELECT month,
               COUNT(*) AS orders,
               SUM(used_points) AS orders_with_points,
               ROUND(100.0 * SUM(used_points) / COUNT(*), 2) AS points_order_share_percent
        FROM monthly_orders
        GROUP BY month
        ORDER BY month
    """)
    q6_result
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    7. The products, available today or not, that have not sold in the last 60 days.
    -
    **Answer:** Bagel (available), Chai Latte (available) and Drip Coffee (available) had no sales from September 10 through November 8, 2026.
    """)
    return


@app.cell
def _(ask, as_of, last_60_start):
    q7_result = ask(f"""
        SELECT p.product_id, p.name, p.is_available
        FROM products p
        WHERE NOT EXISTS (
            SELECT 1
            FROM order_lines ol
            JOIN orders o ON o.order_id = ol.order_id
            WHERE ol.product_id = p.product_id
              AND CAST(o.ordered_at AS DATE) >= DATE '{last_60_start}'
              AND CAST(o.ordered_at AS DATE) <= DATE '{as_of}'
        )
        ORDER BY p.product_id
    """)
    q7_result
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    8. For each coffee and tea product, the average number of options on its lines, counting a line with no options as zero. (three tables or more)
    -
    **Answer:** Across the 10 coffee and tea products, the average options per line range from 0.75 for Drip Coffee to 0.94 for Iced Tea; lines with no options count as zero.
    """)
    return


@app.cell
def _(ask):
    q8_result = ask("""
        WITH line_option_counts AS (
            SELECT ol.line_id, ol.product_id, COUNT(lo.option_id) AS option_count
            FROM order_lines ol
            LEFT JOIN line_options lo ON lo.line_id = ol.line_id
            GROUP BY ol.line_id, ol.product_id
        )
        SELECT p.category, p.name,
               ROUND(AVG(c.option_count), 2) AS average_options,
               COUNT(c.line_id) AS lines_sold
        FROM products p
        LEFT JOIN line_option_counts c ON c.product_id = p.product_id
        WHERE p.category IN ('coffee', 'tea')
        GROUP BY p.product_id, p.name, p.category
        ORDER BY p.category, p.name
    """)
    q8_result
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    9. Which hour was busiest in the last 30 days?
    -
    **Answer:** 2 p.m. was busiest, with 11 orders from October 10 through November 8, 2026.
    """)
    return


@app.cell
def _(ask, last_30_start, as_of):
    q9_hourly = ask(f"""
        SELECT EXTRACT(HOUR FROM ordered_at)::INTEGER AS hour,
               COUNT(*) AS orders
        FROM orders
        WHERE CAST(ordered_at AS DATE) >= DATE '{last_30_start}'
          AND CAST(ordered_at AS DATE) <= DATE '{as_of}'
        GROUP BY hour
        ORDER BY hour
    """)
    q9_hourly
    return


@app.cell
def _(plt, q9_hourly):
    q9_fig, q9_ax = plt.subplots()
    q9_ax.bar(q9_hourly["hour"].to_list(), q9_hourly["orders"].to_list())
    q9_ax.set_xlabel("Hour of day")
    q9_ax.set_ylabel("Orders in the last 30 days")
    q9_ax.set_title("Babson Bean orders by hour")
    q9_fig
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    10. How many orders came through the app and counter?
    -
    **Answer:** 512 orders (51.20%) came through the app and 488 (48.80%) came through the counter, a 24-order difference.
    """)
    return


@app.cell
def _(ask):
    q10_result = ask("""
        SELECT channel, COUNT(*) AS orders,
               ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM orders), 2) AS order_share_percent
        FROM orders
        GROUP BY channel
        ORDER BY orders DESC
    """)
    q10_result
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    1. How I Know These Numbers Are Right
    -
    The payment check compares its two flagged order IDs with the two IDs deliberately generated in Part A. The hour chart's counts are also checked against a separate direct count of orders in the same 30-day window.
    """)
    return


@app.cell
def _(q4_result):
    q4_expected_ids = [10, 25]
    q4_actual_ids = q4_result.get_column("order_id").to_list()
    print(f"Part A expected mismatch order IDs: {q4_expected_ids}")
    print(f"Q4 query returned mismatch order IDs: {q4_actual_ids}")
    assert q4_actual_ids == q4_expected_ids
    return


@app.cell
def _(ask, as_of, last_30_start, q9_hourly):
    q9_hour_bucket_total = int(q9_hourly.get_column("orders").sum())
    q9_direct_total = int(ask(f"""
        SELECT COUNT(*) AS order_count
        FROM orders
        WHERE CAST(ordered_at AS DATE) >= DATE '{last_30_start}'
          AND CAST(ordered_at AS DATE) <= DATE '{as_of}'
    """).get_column("order_count")[0])
    print(f"Sum of Q9 hourly counts: {q9_hour_bucket_total}")
    print(f"Direct count of orders in that date range: {q9_direct_total}")
    assert q9_hour_bucket_total == q9_direct_total
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    2. Working With the Agent
    -
    The first Q8 draft ordered by `p.category` without grouping that column, so DuckDB rejected it. I added `p.category` to the `GROUP BY`; the corrected query ran and returned all 10 coffee and tea products with their line counts. This is the Q8 SQL/result cell. Part B also exposed a Part A mistake: `payments.amount` allowed zero even though the rule says it must be positive. I changed its `CHECK` in `build.py` to `amount > 0`, rebuilt the database, and verified a zero-dollar insert is refused.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    3. Reading It Back
    -
    **The question I picked before answering:** Question 2, *"Revenue, cost and margin by menu category, with what the options earned counted in."* Its join uses `order_lines`, `products`, `line_options` and `options`.

    **My prediction, committed first as `db: prediction`:** The joins should produce about 2,990 rows before grouping.

    ```sql
    FROM order_lines ol
    JOIN products p ON p.product_id = ol.product_id
    LEFT JOIN line_options lo ON lo.line_id = ol.line_id
    LEFT JOIN options opt ON opt.option_id = lo.option_id
    ```

    `order_lines` has 2,491 rows. Joining products does not change that count because each line has one product. The left join keeps an unmodified line once, and a line with options once per option; the final options join does not multiply rows because each option ID is unique.
    """)
    return


@app.cell
def _(ask):
    reading_back_count = ask("""
        SELECT COUNT(*) AS joined_rows
        FROM order_lines ol
        JOIN products p ON p.product_id = ol.product_id
        LEFT JOIN line_options lo ON lo.line_id = ol.line_id
        LEFT JOIN options opt ON opt.option_id = lo.option_id
    """)
    reading_back_count
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The joins produced **3,002 rows**, 12 more than my approximate prediction, so it was close but not exact. The generator made 2,036 line-option rows across 1,525 lines; the count is `2,491 - 1,525 + 2,036 = 3,002`, since lines without options remain once and lines with options contribute one row per option. One row of the grouped category result represents all product lines in that category, including each attached option's revenue and cost.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    4. Going Further
    -
    I charted order volume by hour for the last 30 days. The busiest hour was 2 p.m. with 11 orders; the chart appears under Question 9, with both axes labeled.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    5. Time Spent
    -
    About ___ hours outside class.
    """)
    return


if __name__ == "__main__":
    app.run()
