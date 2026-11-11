import marimo

__generated_with = "0.24.2"
app = marimo.App(width="medium")


@app.cell
def _():
    return


@app.cell
def _():
    import marimo as mo 
    import duckdb

    return duckdb, mo


@app.cell
def _():
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The Tables
    -
    One CREATE TABLE for each table in your ERD, with every primary key and foreign key declared, and with NOT NULL, CHECK, UNIQUE and DEFAULT where the scenario's rules call for them. Chapter D of the SQL handbook, §24, has the syntax.
    """)
    return


@app.cell
def _():
    return


@app.cell
def _(duckdb, mo):
    _file = mo.notebook_dir() / "database.duckdb"

    with duckdb.connect(str(_file)) as _con:
        _con.execute("""
        CREATE TABLE IF NOT EXISTS members (
            member_id INTEGER PRIMARY KEY,
            first_name VARCHAR NOT NULL,
            mobile_number VARCHAR NOT NULL,
            email VARCHAR,
            join_date DATE NOT NULL,
            points_balance INTEGER NOT NULL DEFAULT 0 CHECK (points_balance >= 0)
        );

        CREATE TABLE IF NOT EXISTS products (
            product_id INTEGER PRIMARY KEY,
            name VARCHAR NOT NULL,
            category VARCHAR NOT NULL CHECK (category IN ('coffee', 'tea', 'food', 'other')),
            price DECIMAL(10,2) NOT NULL CHECK (price >= 0),
            cost DECIMAL(10,2) NOT NULL CHECK (cost >= 0),
            is_available BOOLEAN NOT NULL DEFAULT TRUE
        );

        CREATE TABLE IF NOT EXISTS options (
            option_id INTEGER PRIMARY KEY,
            name VARCHAR NOT NULL,
            price DECIMAL(10,2) NOT NULL CHECK (price >= 0),
            cost DECIMAL(10,2) NOT NULL CHECK (cost >= 0)
        );CREATE TABLE IF NOT EXISTS orders (
            order_id INTEGER PRIMARY KEY,
            ordered_at TIMESTAMP NOT NULL,
            member_id INTEGER REFERENCES members(member_id),
            channel VARCHAR NOT NULL CHECK (channel IN ('counter', 'app'))
        );

        CREATE TABLE IF NOT EXISTS order_lines (
            line_id INTEGER PRIMARY KEY,
            order_id INTEGER NOT NULL REFERENCES orders(order_id),
            product_id INTEGER NOT NULL REFERENCES products(product_id),
            quantity INTEGER NOT NULL CHECK (quantity > 0),
            price_charged DECIMAL(10,2) NOT NULL CHECK (price_charged >= 0)
        );

        CREATE TABLE IF NOT EXISTS line_options (
            line_id INTEGER NOT NULL REFERENCES order_lines(line_id),
            option_id INTEGER NOT NULL REFERENCES options(option_id),
            price_charged DECIMAL(10,2) NOT NULL CHECK (price_charged >= 0),
            PRIMARY KEY (line_id, option_id)
        );

        CREATE TABLE IF NOT EXISTS payments (
            payment_id INTEGER PRIMARY KEY,
            order_id INTEGER NOT NULL REFERENCES orders(order_id),
            method VARCHAR NOT NULL CHECK (method IN ('cash', 'card', 'app', 'points')),
            amount DECIMAL(10,2) NOT NULL CHECK (amount >= 0)
        );
        """)
    return


if __name__ == "__main__":
    app.run()
