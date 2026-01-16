def calculate_total_sales(records):
    total = 0
    for r in records:
        total += r["quantity"] * r["unit_price"]
    return total


def sales_by_region(records):
    region_sales = {}

    for r in records:
        region = r["region"]
        region_sales[region] = region_sales.get(region, 0) + (
            r["quantity"] * r["unit_price"]
        )

    return region_sales


def top_products(records, top_n=3):
    product_sales = {}

    for r in records:
        product = r["product_name"]
        product_sales[product] = product_sales.get(product, 0) + (
            r["quantity"] * r["unit_price"]
        )

    sorted_products = sorted(
        product_sales.items(),
        key=lambda x: x[1],
        reverse=True
    )

    return sorted_products[:top_n]
