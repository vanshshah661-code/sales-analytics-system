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
