import marimo

__generated_with = "0.24.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import duckdb
    import polars as pl

    return duckdb, mo, pl


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    1. The Tables
    -
    One `CREATE TABLE` for each table in the ERD, with every primary key and foreign key declared, and with `NOT NULL`, `CHECK`, `UNIQUE` and `DEFAULT` where the café's rules call for them.

    **Nothing may keep the database open.** This one cell deletes the old file, opens a new one, creates every table, loads the CSV files in `data/`, creates the weekly view, and closes the file when the `with` block ends.
    """)
    return


@app.cell
def _(duckdb, mo, pl):
    _file = mo.notebook_dir() / "database.duckdb"
    _file.unlink(missing_ok=True)

    _data_dir = mo.notebook_dir() / "data"
    members_rows = pl.read_csv(_data_dir / "members.csv", null_values=[""])
    products_rows = pl.read_csv(_data_dir / "products.csv")
    options_rows = pl.read_csv(_data_dir / "options.csv")
    orders_rows = pl.read_csv(_data_dir / "orders.csv", null_values=[""])
    order_lines_rows = pl.read_csv(_data_dir / "order_lines.csv")
    line_options_rows = pl.read_csv(_data_dir / "line_options.csv")
    payments_rows = pl.read_csv(_data_dir / "payments.csv")

    with duckdb.connect(_file) as _con:
        _con.execute("""
            CREATE TABLE members (
                member_id INTEGER PRIMARY KEY,
                first_name VARCHAR NOT NULL,
                mobile_number VARCHAR NOT NULL UNIQUE,
                email VARCHAR,
                join_date DATE NOT NULL,
                points_balance INTEGER NOT NULL DEFAULT 0 CHECK (points_balance >= 0)
            )
        """)
        _con.execute("""
            CREATE TABLE products (
                product_id INTEGER PRIMARY KEY,
                name VARCHAR NOT NULL,
                category VARCHAR NOT NULL CHECK (category IN ('coffee', 'tea', 'food', 'other')),
                price DECIMAL(10,2) NOT NULL CHECK (price >= 0),
                cost DECIMAL(10,2) NOT NULL CHECK (cost >= 0),
                is_available BOOLEAN NOT NULL DEFAULT TRUE,
                CHECK (price >= cost)
            )
        """)
        _con.execute("""
            CREATE TABLE options (
                option_id INTEGER PRIMARY KEY,
                name VARCHAR NOT NULL,
                price DECIMAL(10,2) NOT NULL CHECK (price >= 0),
                cost DECIMAL(10,2) NOT NULL CHECK (cost >= 0)
            )
        """)
        _con.execute("""
            CREATE TABLE orders (
                order_id INTEGER PRIMARY KEY,
                ordered_at TIMESTAMP NOT NULL,
                member_id INTEGER REFERENCES members(member_id),
                channel VARCHAR NOT NULL CHECK (channel IN ('counter', 'app'))
            )
        """)
        _con.execute("""
            CREATE TABLE order_lines (
                line_id INTEGER PRIMARY KEY,
                order_id INTEGER NOT NULL REFERENCES orders(order_id),
                product_id INTEGER NOT NULL REFERENCES products(product_id),
                quantity INTEGER NOT NULL CHECK (quantity > 0),
                price_charged DECIMAL(10,2) NOT NULL CHECK (price_charged >= 0)
            )
        """)
        _con.execute("""
            CREATE TABLE line_options (
                line_id INTEGER NOT NULL REFERENCES order_lines(line_id),
                option_id INTEGER NOT NULL REFERENCES options(option_id),
                price_charged DECIMAL(10,2) NOT NULL CHECK (price_charged >= 0),
                PRIMARY KEY (line_id, option_id)
            )
        """)
        _con.execute("""
            CREATE TABLE payments (
                payment_id INTEGER PRIMARY KEY,
                order_id INTEGER NOT NULL REFERENCES orders(order_id),
                method VARCHAR NOT NULL CHECK (method IN ('cash', 'card', 'app', 'points')),
                amount DECIMAL(10,2) NOT NULL CHECK (amount >= 0)
            )
        """)

        # members and products load first: orders and order_lines reference them
        _con.execute("INSERT INTO members SELECT * FROM members_rows")
        _con.execute("INSERT INTO products SELECT * FROM products_rows")
        _con.execute("INSERT INTO options SELECT * FROM options_rows")
        _con.execute("INSERT INTO orders SELECT * FROM orders_rows")
        _con.execute("INSERT INTO order_lines SELECT * FROM order_lines_rows")
        _con.execute("INSERT INTO line_options SELECT * FROM line_options_rows")
        _con.execute("INSERT INTO payments SELECT * FROM payments_rows")

        _con.execute("""
            CREATE VIEW category_performance AS
                WITH line_opts AS (
                    SELECT lo.line_id,
                           SUM(lo.price_charged) AS opt_price_per_unit,
                           SUM(opt.cost) AS opt_cost_per_unit
                    FROM line_options lo
                    JOIN options opt ON opt.option_id = lo.option_id
                    GROUP BY lo.line_id
                )
                SELECT
                    p.category,
                    SUM(ol.quantity * ol.price_charged) AS product_revenue,
                    SUM(ol.quantity * p.cost) AS product_cost,
                    SUM(ol.quantity * COALESCE(lo.opt_price_per_unit, 0)) AS option_revenue,
                    SUM(ol.quantity * COALESCE(lo.opt_cost_per_unit, 0)) AS option_cost,
                    SUM(ol.quantity * (ol.price_charged + COALESCE(lo.opt_price_per_unit, 0)))
                        - SUM(ol.quantity * (p.cost + COALESCE(lo.opt_cost_per_unit, 0))) AS margin
                FROM order_lines ol
                JOIN products p ON p.product_id = ol.product_id
                LEFT JOIN line_opts lo ON lo.line_id = ol.line_id
                GROUP BY p.category
        """)

    database = _file
    database.name
    return (database,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Every other cell asks through `ask`.** It opens the file only to read, runs one query, hands back the result as a table, and closes the file again.
    """)
    return


@app.cell
def _(database, duckdb):
    def ask(sql):
        with duckdb.connect(database, read_only=True) as _con:
            return _con.sql(sql).pl()

    return (ask,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    2. The Data
    -
    `projects/db/make_data.py` writes one CSV file per table into `projects/db/data/`, with a fixed random seed so it writes the same files every time. It covers the 12 months up to `as_of` = 2026-11-08.

    It breaks the rule "an order's payments add up to the order's total" on purpose, in exactly two rows: the payments for order_id 10 and order_id 25 are each overcharged by $5.00. The tables cannot hold this rule with a `CHECK`, because it compares sums across three tables, so it is checked with a query instead, in section 6 below.

    It also includes, on purpose, rows with nothing attached: 5 members have never placed an order, and 3 products have not sold in the last 60 days before `as_of`.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    3. A Look at the Data
    -
    """)
    return


@app.cell
def _(mo, pl):
    import matplotlib.pyplot as plt

    _orders = pl.read_csv(mo.notebook_dir() / "data" / "orders.csv", try_parse_dates=True)
    _by_hour = (
        _orders.with_columns(pl.col("ordered_at").dt.hour().alias("hour"))
        .group_by("hour")
        .len()
        .sort("hour")
    )

    _fig, _ax = plt.subplots()
    _ax.bar(_by_hour["hour"], _by_hour["len"])
    _ax.set_xlabel("Hour of day")
    _ax.set_ylabel("Number of orders")
    _ax.set_title("Orders by hour")
    _fig
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Orders are spread evenly from 7am to 6pm; a real café would show peaks at breakfast and lunch instead, so `make_data.py` should weight the order hour toward 8-10am and noon rather than picking it uniformly at random.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    4. Row Counts
    -
    """)
    return


@app.cell
def _(ask):
    ask("""
        SELECT 'members' AS table_name, count(*) AS rows FROM members
        UNION ALL SELECT 'products', count(*) FROM products
        UNION ALL SELECT 'options', count(*) FROM options
        UNION ALL SELECT 'orders', count(*) FROM orders
        UNION ALL SELECT 'order_lines', count(*) FROM order_lines
        UNION ALL SELECT 'line_options', count(*) FROM line_options
        UNION ALL SELECT 'payments', count(*) FROM payments
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    5. A Row It Refuses
    -
    A product whose price is below its cost breaks `CHECK (price >= cost)`.
    """)
    return


@app.cell
def _(database, duckdb):
    try:
        with duckdb.connect(database) as _con:
            _con.execute("""
                INSERT INTO products (product_id, name, category, price, cost, is_available)
                VALUES (9999, 'Underpriced Latte', 'coffee', 1.00, 5.00, TRUE)
            """)
    except Exception as _e:
        print(_e)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    6. Answers You Already Knew
    -
    `make_data.py` made 50 members and only let the first 45 member ids place orders, so exactly 5 members should have never ordered.
    """)
    return


@app.cell
def _(ask):
    ask("""
        SELECT count(*) AS members_with_no_orders
        FROM members m
        WHERE NOT EXISTS (SELECT 1 FROM orders o WHERE o.member_id = m.member_id)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    `make_data.py` makes exactly 1000 orders, one row per order, so `orders` should have exactly 1000 rows.
    """)
    return


@app.cell
def _(ask):
    ask("SELECT count(*) AS order_count FROM orders")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    `make_data.py` broke the payments-match-total rule in exactly two orders, order_id 10 and order_id 25, so this query should return exactly those two rows.
    """)
    return


@app.cell
def _(ask):
    ask("""
        WITH line_totals AS (
            SELECT ol.order_id,
                   SUM(ol.quantity * ol.price_charged) AS product_total,
                   SUM(ol.quantity * COALESCE(x.opt_total, 0)) AS option_total
            FROM order_lines ol
            LEFT JOIN (
                SELECT line_id, SUM(price_charged) AS opt_total
                FROM line_options
                GROUP BY line_id
            ) x ON x.line_id = ol.line_id
            GROUP BY ol.order_id
        ),
        paid_totals AS (
            SELECT order_id, SUM(amount) AS paid
            FROM payments
            GROUP BY order_id
        )
        SELECT o.order_id,
               round(l.product_total + l.option_total, 2) AS order_total,
               round(p.paid, 2) AS paid
        FROM orders o
        JOIN line_totals l ON l.order_id = o.order_id
        JOIN paid_totals p ON p.order_id = o.order_id
        WHERE round(l.product_total + l.option_total, 2) <> round(p.paid, 2)
        ORDER BY o.order_id
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    7. A View
    -
    The café would ask every week which menu category is earning its keep. `category_performance`, created in the build cell above, answers that by name and always reflects the current rows.
    """)
    return


@app.cell
def _(ask):
    ask("SELECT * FROM category_performance ORDER BY margin DESC")
    return


if __name__ == "__main__":
    app.run()
