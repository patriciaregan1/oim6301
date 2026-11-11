"""Writes one CSV file per table for the Babson Bean Café database.

Run with: uv run python projects/db/make_data.py
"""

import random
from datetime import date, datetime, timedelta
from pathlib import Path

from faker import Faker

SEED = 42
random.seed(SEED)
fake = Faker()
Faker.seed(SEED)

AS_OF = date(2026, 11, 8)
WINDOW_START = AS_OF - timedelta(days=365)  # 12 months of data up to as_of
STALE_CUTOFF = AS_OF - timedelta(days=60)  # Q7 needs products unsold in the last 60 days

DATA_DIR = Path(__file__).parent / "data"
DATA_DIR.mkdir(exist_ok=True)

NUM_MEMBERS = 50
NUM_MEMBERS_WITH_NO_ORDERS = 5  # last 5 member ids, for Q5
NUM_PRODUCTS = 20
NUM_STALE_PRODUCTS = 3  # not sold in the last 60 days, for Q7
NUM_OPTIONS = 8
NUM_ORDERS = 1000


# ---------------------------------------------------------------------------
# Members
# ---------------------------------------------------------------------------
members = []
used_mobiles = set()
for member_id in range(1, NUM_MEMBERS + 1):
    first_name = fake.first_name()

    mobile_number = fake.numerify("###-###-####")
    while mobile_number in used_mobiles:  # mobile_number is UNIQUE in the table
        mobile_number = fake.numerify("###-###-####")
    used_mobiles.add(mobile_number)

    email = fake.email() if random.random() > 0.2 else ""  # email is optional
    join_date = fake.date_between(start_date=WINDOW_START, end_date=AS_OF)
    points_balance = random.randint(0, 500)

    members.append(
        {
            "member_id": member_id,
            "first_name": first_name,
            "mobile_number": mobile_number,
            "email": email,
            "join_date": join_date,
            "points_balance": points_balance,
        }
    )

# These member ids never place an order, so Q5 has an answer.
members_with_orders = [
    m["member_id"] for m in members
][: NUM_MEMBERS - NUM_MEMBERS_WITH_NO_ORDERS]


# ---------------------------------------------------------------------------
# Products
# ---------------------------------------------------------------------------
product_names = {
    "coffee": ["Drip Coffee", "Latte", "Cappuccino", "Americano", "Cold Brew", "Mocha"],
    "tea": ["Green Tea", "Chai Latte", "Iced Tea", "Herbal Tea"],
    "food": ["Bagel", "Croissant", "Muffin", "Avocado Toast", "Breakfast Sandwich"],
    "other": ["Bottled Water", "Orange Juice", "Granola Bar", "Fruit Cup", "Cookie"],
}
all_names = [(name, cat) for cat, names in product_names.items() for name in names]
random.shuffle(all_names)

products = []
for product_id in range(1, NUM_PRODUCTS + 1):
    name, category = all_names[(product_id - 1) % len(all_names)]
    cost = round(random.uniform(0.5, 4.0), 2)
    price = round(cost + random.uniform(0.5, 3.0), 2)  # price never below cost
    is_available = random.random() > 0.15  # most products are available today
    products.append(
        {
            "product_id": product_id,
            "name": name,
            "category": category,
            "price": price,
            "cost": cost,
            "is_available": is_available,
        }
    )

# These product ids are not sold in the last 60 days, so Q7 has an answer.
stale_product_ids = set(range(1, NUM_STALE_PRODUCTS + 1))
fresh_product_ids = [p["product_id"] for p in products if p["product_id"] not in stale_product_ids]


# ---------------------------------------------------------------------------
# Options
# ---------------------------------------------------------------------------
option_names = [
    "Extra Shot", "Oat Milk", "Almond Milk", "Vanilla Syrup",
    "Caramel Syrup", "Whipped Cream", "Extra Espresso", "Decaf",
]
options = []
for option_id, name in enumerate(option_names[:NUM_OPTIONS], start=1):
    price = round(random.uniform(0, 1.5), 2)
    cost = round(price * random.uniform(0.2, 0.5), 2)
    options.append({"option_id": option_id, "name": name, "price": price, "cost": cost})


# ---------------------------------------------------------------------------
# Orders, order lines, line options, payments
# ---------------------------------------------------------------------------
orders = []
order_lines = []
line_options = []
payments = []

line_id = 1
payment_id = 1

for order_id in range(1, NUM_ORDERS + 1):
    days_offset = random.randint(0, (AS_OF - WINDOW_START).days)
    order_day = WINDOW_START + timedelta(days=days_offset)
    order_time = datetime.combine(order_day, datetime.min.time()) + timedelta(
        hours=random.randint(7, 18), minutes=random.randint(0, 59)
    )

    member_id = random.choice(members_with_orders) if random.random() < 0.7 else ""
    channel = random.choice(["counter", "app"])

    orders.append(
        {
            "order_id": order_id,
            "ordered_at": order_time,
            "member_id": member_id,
            "channel": channel,
        }
    )

    # a product sold in the last 60 days can't be one of the stale ones
    available_product_ids = (
        fresh_product_ids if order_day >= STALE_CUTOFF else [p["product_id"] for p in products]
    )

    order_total = 0.0
    num_lines = random.randint(1, 4)  # every order has one line or more
    for _ in range(num_lines):
        product_id = random.choice(available_product_ids)
        product = products[product_id - 1]
        quantity = random.randint(1, 3)
        price_charged = product["price"]

        order_lines.append(
            {
                "line_id": line_id,
                "order_id": order_id,
                "product_id": product_id,
                "quantity": quantity,
                "price_charged": price_charged,
            }
        )
        line_total = quantity * price_charged

        # 0-2 options on this line, each option at most once per line
        num_options = random.choice([0, 0, 1, 1, 2])
        for option in random.sample(options, k=min(num_options, len(options))):
            option_price = option["price"]
            line_options.append(
                {
                    "line_id": line_id,
                    "option_id": option["option_id"],
                    "price_charged": option_price,
                }
            )
            line_total += quantity * option_price

        order_total += line_total
        line_id += 1

    order_total = round(order_total, 2)

    # one payment most of the time, two payments the rest, always summing to the total
    methods = ["cash", "card", "app", "points"]
    if random.random() < 0.8:
        payments.append(
            {
                "payment_id": payment_id,
                "order_id": order_id,
                "method": random.choice(methods),
                "amount": order_total,
            }
        )
        payment_id += 1
    else:
        first_share = round(order_total * random.uniform(0.3, 0.7), 2)
        second_share = round(order_total - first_share, 2)
        method_a, method_b = random.sample(methods, 2)
        payments.append(
            {"payment_id": payment_id, "order_id": order_id, "method": method_a, "amount": first_share}
        )
        payment_id += 1
        payments.append(
            {"payment_id": payment_id, "order_id": order_id, "method": method_b, "amount": second_share}
        )
        payment_id += 1

# Q4 (checks a rule): break "payments add up to the order's total" on purpose, in exactly two orders.
broken_order_ids = [orders[9]["order_id"], orders[24]["order_id"]]
for broken_order_id in broken_order_ids:
    for payment in payments:
        if payment["order_id"] == broken_order_id:
            payment["amount"] = round(payment["amount"] + 5.00, 2)
            break  # only the first payment found for that order is changed

print("Rows that break 'payments add up to the order's total' on purpose:")
for broken_order_id in broken_order_ids:
    print(f"  order_id {broken_order_id}: one payment overcharged by $5.00")


# ---------------------------------------------------------------------------
# Write CSV files
# ---------------------------------------------------------------------------
import csv


def write_csv(filename, rows):
    path = DATA_DIR / filename
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
    print(f"wrote {len(rows)} rows to {path}")


write_csv("members.csv", members)
write_csv("products.csv", products)
write_csv("options.csv", options)
write_csv("orders.csv", orders)
write_csv("order_lines.csv", order_lines)
write_csv("line_options.csv", line_options)
write_csv("payments.csv", payments)
