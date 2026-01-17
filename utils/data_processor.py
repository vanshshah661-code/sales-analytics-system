def parse_transactions(raw_lines):
    """
    Task 1.2: Parse and clean raw data
    """
    transactions = []

    for line in raw_lines:
        parts = line.split("|")

        if len(parts) != 8:
            continue

        try:
            transaction = {
                "TransactionID": parts[0],
                "Date": parts[1],
                "ProductID": parts[2],
                "ProductName": parts[3].replace(",", ""),
                "Quantity": int(parts[4].replace(",", "")),
                "UnitPrice": float(parts[5].replace(",", "")),
                "CustomerID": parts[6],
                "Region": parts[7],
            }

            transactions.append(transaction)

        except ValueError:
            continue

    return transactions


def validate_and_filter(transactions, region=None, min_amount=None, max_amount=None):
    """
    Task 1.3: Validate and filter transactions
    """
    valid = []
    invalid_count = 0
    total_input = len(transactions)

    for t in transactions:
        if (
            t["Quantity"] <= 0
            or t["UnitPrice"] <= 0
            or not t["TransactionID"].startswith("T")
            or not t["ProductID"].startswith("P")
            or not t["CustomerID"].startswith("C")
            or not t["Region"]
        ):
            invalid_count += 1
            continue

        valid.append(t)

    # Display available regions

    def calculate_total_revenue(transactions):
    total = 0.0
    for t in transactions:
        total += t["Quantity"] * t["UnitPrice"]
    return total

def region_wise_sales(transactions):
    region_data = {}
    total_revenue = calculate_total_revenue(transactions)

    for t in transactions:
        region = t["Region"]
        amount = t["Quantity"] * t["UnitPrice"]

        if region not in region_data:
            region_data[region] = {
                "total_sales": 0.0,
                "transaction_count": 0
            }

        region_data[region]["total_sales"] += amount
        region_data[region]["transaction_count"] += 1

    # calculate percentage
    for region in region_data:
        region_data[region]["percentage"] = round(
            (region_data[region]["total_sales"] / total_revenue) * 100, 2
        )

    # sort by total_sales descending
    sorted_regions = dict(
        sorted(
            region_data.items(),
            key=lambda x: x[1]["total_sales"],
            reverse=True
        )
    )

    return sorted_regions
def top_selling_products(transactions, n=5):
    product_data = {}

    for t in transactions:
        product = t["ProductName"]
        qty = t["Quantity"]
        revenue = qty * t["UnitPrice"]

        if product not in product_data:
            product_data[product] = {
                "quantity": 0,
                "revenue": 0.0
            }

        product_data[product]["quantity"] += qty
        product_data[product]["revenue"] += revenue

    sorted_products = sorted(
        product_data.items(),
        key=lambda x: x[1]["quantity"],
        reverse=True
    )

    result = []
    for product, data in sorted_products[:n]:
        result.append((product, data["quantity"], data["revenue"]))

    return result
def customer_analysis(transactions):
    customer_data = {}

    for t in transactions:
        cid = t["CustomerID"]
        amount = t["Quantity"] * t["UnitPrice"]

        if cid not in customer_data:
            customer_data[cid] = {
                "total_spent": 0.0,
                "purchase_count": 0,
                "products_bought": set()
            }

        customer_data[cid]["total_spent"] += amount
        customer_data[cid]["purchase_count"] += 1
        customer_data[cid]["products_bought"].add(t["ProductName"])

    # finalize output
    final_data = {}
    for cid, data in customer_data.items():
        final_data[cid] = {
            "total_spent": data["total_spent"],
            "purchase_count": data["purchase_count"],
            "average_order_value": round(
                data["total_spent"] / data["purchase_count"], 2
            ),
            "products_bought": list(data["products_bought"])
        }

    return dict(
        sorted(
            final_data.items(),
            key=lambda x: x[1]["total_spent"],
            reverse=True
        )
    )

def daily_sales_trend(transactions):
    daily_data = {}

    for t in transactions:
        date = t["Date"]
        revenue = t["Quantity"] * t["UnitPrice"]
        customer = t["CustomerID"]

        if date not in daily_data:
            daily_data[date] = {
                "revenue": 0.0,
                "transaction_count": 0,
                "unique_customers": set()
            }

        daily_data[date]["revenue"] += revenue
        daily_data[date]["transaction_count"] += 1
        daily_data[date]["unique_customers"].add(customer)

    # convert customer sets to counts
    for date in daily_data:
        daily_data[date]["unique_customers"] = len(
            daily_data[date]["unique_customers"]
        )

    # sort by date
    return dict(sorted(daily_data.items()))
def find_peak_sales_day(transactions):
    daily_data = {}

    for t in transactions:
        date = t["Date"]
        revenue = t["Quantity"] * t["UnitPrice"]

        if date not in daily_data:
            daily_data[date] = {
                "revenue": 0.0,
                "transaction_count": 0
            }

        daily_data[date]["revenue"] += revenue
        daily_data[date]["transaction_count"] += 1

    peak_date = None
    max_revenue = 0.0
    peak_transactions = 0

    for date, data in daily_data.items():
        if data["revenue"] > max_revenue:
            max_revenue = data["revenue"]
            peak_date = date
            peak_transactions = data["transaction_count"]

    return (peak_date, max_revenue, peak_transactions)
def low_performing_products(transactions, threshold=10):
    product_data = {}

    for t in transactions:
        product = t["ProductName"]
        qty = t["Quantity"]
        revenue = qty * t["UnitPrice"]

        if product not in product_data:
            product_data[product] = {
                "quantity": 0,
                "revenue": 0.0
            }

        product_data[product]["quantity"] += qty
        product_data[product]["revenue"] += revenue

    low_products = []

    for product, data in product_data.items():
        if data["quantity"] < threshold:
            low_products.append(
                (product, data["quantity"], data["revenue"])
            )

    # sort by total quantity ascending
    low_products.sort(key=lambda x: x[1])

    return low_products
