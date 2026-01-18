def parse_transactions(raw_lines):
    transactions = []

    for line in raw_lines:
        parts = line.split("|")
        if len(parts) != 8:
            continue

        try:
            transactions.append({
                "TransactionID": parts[0],
                "Date": parts[1],
                "ProductID": parts[2],
                "ProductName": parts[3].replace(",", ""),
                "Quantity": int(parts[4].replace(",", "")),
                "UnitPrice": float(parts[5].replace(",", "")),
                "CustomerID": parts[6],
                "Region": parts[7],
            })
        except:
            continue

    return transactions


def validate_and_filter(transactions):
    valid = []
    invalid = 0

    for t in transactions:
        if (
            t["Quantity"] <= 0
            or t["UnitPrice"] <= 0
            or not t["TransactionID"].startswith("T")
            or not t["ProductID"].startswith("P")
            or not t["CustomerID"].startswith("C")
            or not t["Region"]
        ):
            invalid += 1
            continue
        valid.append(t)

    print(f"Invalid records removed: {invalid}")
    print(f"Valid records after cleaning: {len(valid)}")

    return valid


def calculate_total_revenue(transactions):
    total = 0.0
    for t in transactions:
        total += t["Quantity"] * t["UnitPrice"]
    return total


def region_wise_sales(transactions):
    data = {}
    total = calculate_total_revenue(transactions)

    for t in transactions:
        region = t["Region"]
        amount = t["Quantity"] * t["UnitPrice"]

        if region not in data:
            data[region] = {"total_sales": 0, "transaction_count": 0}

        data[region]["total_sales"] += amount
        data[region]["transaction_count"] += 1

    for r in data:
        data[r]["percentage"] = round((data[r]["total_sales"] / total) * 100, 2)

    return dict(sorted(data.items(), key=lambda x: x[1]["total_sales"], reverse=True))


def top_selling_products(transactions, n=5):
    products = {}

    for t in transactions:
        p = t["ProductName"]
        qty = t["Quantity"]
        revenue = qty * t["UnitPrice"]

        if p not in products:
            products[p] = {"qty": 0, "revenue": 0}

        products[p]["qty"] += qty
        products[p]["revenue"] += revenue

    sorted_products = sorted(products.items(), key=lambda x: x[1]["qty"], reverse=True)

    return [(p, d["qty"], d["revenue"]) for p, d in sorted_products[:n]]


def daily_sales_trend(transactions):
    daily = {}

    for t in transactions:
        d = t["Date"]
        amt = t["Quantity"] * t["UnitPrice"]

        if d not in daily:
            daily[d] = {"revenue": 0, "transaction_count": 0, "customers": set()}

        daily[d]["revenue"] += amt
        daily[d]["transaction_count"] += 1
        daily[d]["customers"].add(t["CustomerID"])

    for d in daily:
        daily[d]["unique_customers"] = len(daily[d]["customers"])
        del daily[d]["customers"]

    return dict(sorted(daily.items()))


def find_peak_sales_day(transactions):
    daily = daily_sales_trend(transactions)

    peak_date = None
    max_revenue = 0
    count = 0

    for d, v in daily.items():
        if v["revenue"] > max_revenue:
            max_revenue = v["revenue"]
            peak_date = d
            count = v["transaction_count"]

    return peak_date, max_revenue, count


def low_performing_products(transactions, threshold=10):
    products = {}

    for t in transactions:
        p = t["ProductName"]
        qty = t["Quantity"]
        revenue = qty * t["UnitPrice"]

        if p not in products:
            products[p] = {"qty": 0, "revenue": 0}

        products[p]["qty"] += qty
        products[p]["revenue"] += revenue

    low = [(p, d["qty"], d["revenue"]) for p, d in products.items() if d["qty"] < threshold]
    low.sort(key=lambda x: x[1])
    return low
