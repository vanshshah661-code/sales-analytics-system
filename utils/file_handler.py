def read_sales_data(file_path):
    records = []
    total_records = 0
    invalid_records = 0

    with open(file_path, "r", encoding="latin-1") as file:
        header = file.readline()  # skip header

        for line in file:
            total_records += 1

            parts = line.strip().split("|")

            # must have exactly 8 fields
            if len(parts) != 8:
                invalid_records += 1
                continue

            transaction_id = parts[0]
            date = parts[1]
            product_id = parts[2]
            product_name = parts[3]
            quantity = parts[4]
            unit_price = parts[5]
            customer_id = parts[6]
            region = parts[7]

            # Rule 1: TransactionID must start with T
            if not transaction_id.startswith("T"):
                invalid_records += 1
                continue

            # Rule 2: CustomerID and Region must exist
            if customer_id.strip() == "" or region.strip() == "":
                invalid_records += 1
                continue

            # Rule 3: Quantity must be > 0
            try:
                quantity = int(quantity.replace(",", ""))
                if quantity <= 0:
                    invalid_records += 1
                    continue
            except:
                invalid_records += 1
                continue

            # Rule 4: UnitPrice must be > 0
            try:
                unit_price = float(unit_price.replace(",", ""))
                if unit_price <= 0:
                    invalid_records += 1
                    continue
            except:
                invalid_records += 1
                continue

            # Clean product name (remove commas)
            product_name = product_name.replace(",", "")

            records.append({
                "transaction_id": transaction_id,
                "product_name": product_name,
                "quantity": quantity,
                "unit_price": unit_price,
                "region": region
            })

    print(f"Total records parsed: {total_records}")
    print(f"Invalid records removed: {invalid_records}")
    print(f"Valid records after cleaning: {len(records)}")

    return records


