from utils.file_handler import read_sales_data

from utils.data_processor import (
    parse_transactions,
    validate_and_filter,
    calculate_total_revenue,
    region_wise_sales,
    top_selling_products,
    daily_sales_trend,
    find_peak_sales_day,
    low_performing_products
)

from utils.api_handler import (
    fetch_all_products,
    create_product_mapping,
    enrich_sales_data,
    save_enriched_data
)

from utils.report_generator import generate_sales_report
def main():
    # Step 1: Read raw data
    raw_lines = read_sales_data("data/sales_data.txt")

    # Step 2: Parse transactions
    transactions = parse_transactions(raw_lines)

    # Step 3: Validate and filter
    valid = validate_and_filter(transactions)

    # Step 4: Analysis
    total_sales = calculate_total_revenue(valid)
    region_data = region_wise_sales(valid)
    top_products = top_selling_products(valid)

    print("Total Revenue:", total_sales)
    print("Regions:", region_data.keys())
    print("Top Products:", top_products)

    # Step 5: API integration
    api_products = fetch_all_products()
    product_mapping = create_product_mapping(api_products)
    enriched = enrich_sales_data(valid, product_mapping)
    save_enriched_data(enriched)

    # Step 6: Report generation
    generate_sales_report(valid, enriched)
    print("Sales report generated at output/sales_report.txt")


if __name__ == "__main__":
    main()



