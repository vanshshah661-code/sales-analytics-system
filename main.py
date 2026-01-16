from utils.file_handler import read_sales_data
from utils.data_processor import calculate_total_sales, sales_by_region, top_products

DATA_PATH = "data/sales_data.txt"
OUTPUT_PATH = "output/report.txt"


def main():
    records = read_sales_data(DATA_PATH)

    total_sales = calculate_total_sales(records)
    region_sales = sales_by_region(records)
    top_items = top_products(records)

    with open(OUTPUT_PATH, "w") as file:
        file.write("SALES ANALYTICS REPORT\n")
        file.write("-" * 30 + "\n")
        file.write(f"Total Sales: {total_sales}\n\n")

        file.write("Sales by Region:\n")
        for region, amount in region_sales.items():
            file.write(f"{region}: {amount}\n")


        file.write("\nTop Selling Products:\n")
        for product, amount in top_items:
            file.write(f"{product}: {amount}\n")

    print("Report generated successfully.")


if __name__ == "__main__":
    main()
