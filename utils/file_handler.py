def read_sales_data(filename):
    """
    Task 1.1: Read sales data handling encoding issues
    Returns list of raw lines (strings)
    """
    encodings = ["utf-8", "latin-1", "cp1252"]

    for enc in encodings:
        try:
            with open(filename, "r", encoding=enc) as file:
                lines = file.readlines()

            raw_lines = []
            for line in lines[1:]:  # skip header
                line = line.strip()
                if line:
                    raw_lines.append(line)

            return raw_lines

        except UnicodeDecodeError:
            continue

        except FileNotFoundError:
            print(f"Error: File '{filename}' not found.")
            return []

    print("Error: Unable to read file due to encoding issues.")
    return []

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


