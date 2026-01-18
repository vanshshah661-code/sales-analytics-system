from datetime import datetime
from collections import defaultdict


def generate_sales_report(transactions, enriched_transactions, output_file="output/sales_report.txt"):
    # Basic metrics
    total_transactions = len(transactions)
    total_revenue = sum(t["Quantity"] * t["UnitPrice"] for t in transactions)
    avg_order_value = total_revenue / total_transactions if total_transactions else 0

    dates = [t["Date"] for t in transactions]
    date_range = f"{min(dates)} to {max(dates)}" if dates else "N/A"

    # Region-wise stats
    region_stats = defaultdict(lambda: {"revenue": 0, "count": 0})
    for t in transactions:
        amount = t["Quantity"] * t["UnitPrice"]
        region_stats[t["Region"]]["revenue"] += amount
        region_stats[t["Region"]]["count"] += 1

    # Top products
    product_stats = defaultdict(lambda: {"qty": 0, "revenue": 0})
    for t in transactions:
        product_stats[t["ProductName"]]["qty"] += t["Quantity"]
        product_stats[t["ProductName"]]["revenue"] += t["Quantity"] * t["UnitPrice"]

    top_products = sorted(
        product_stats.items(),
        key=lambda x: x[1]["qty"],
        reverse=True
    )[:5]

    # Customer stats
    customer_stats = defaultdict(lambda: {"spent": 0, "count": 0})
    for t in transactions:
        amount = t["Quantity"] * t["UnitPrice"]
        customer_stats[t["CustomerID"]]["spent"] += amount
        customer_stats[t["CustomerID"]]["count"] += 1

    top_customers = sorted(
        customer_stats.items(),
        key=lambda x: x[1]["spent"],
        reverse=True
    )[:5]

    # Daily trend
    daily_stats = defaultdict(lambda: {"revenue": 0, "transactions": 0, "customers": set()})
    for t in transactions:
        amount = t["Quantity"] * t["UnitPrice"]
        daily_stats[t["Date"]]["revenue"] += amount
        daily_stats[t["Date"]]["transactions"] += 1
        daily_stats[t["Date"]]["customers"].add(t["CustomerID"])

    # API enrichment summary
    enriched_count = sum(1 for t in enriched_transactions if t.get("API_Match"))
    total_enriched = len(enriched_transactions)
    success_rate = (enriched_count / total_enriched * 100) if total_enriched else 0

    # Write report
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("SALES ANALYTICS REPORT\n")
        f.write("=" * 40 + "\n")
        f.write(f"Generated: {datetime.now()}\n")
        f.write(f"Records Processed: {total_transactions}\n\n")

        f.write("OVERALL SUMMARY\n")
        f.write("-" * 40 + "\n")
        f.write(f"Total Revenue: {total_revenue:,.2f}\n")
        f.write(f"Total Transactions: {total_transactions}\n")
        f.write(f"Average Order Value: {avg_order_value:,.2f}\n")
        f.write(f"Date Range: {date_range}\n\n")

        f.write("REGION-WISE PERFORMANCE\n")
        f.write("-" * 40 + "\n")
        for region, data in sorted(region_stats.items(), key=lambda x: x[1]["revenue"], reverse=True):
            percent = (data["revenue"] / total_revenue * 100) if total_revenue else 0
            f.write(f"{region}: Revenue={data['revenue']:,.2f}, %={percent:.2f}, Transactions={data['count']}\n")
        f.write("\n")

        f.write("TOP 5 PRODUCTS\n")
        f.write("-" * 40 + "\n")
        for i, (product, data) in enumerate(top_products, 1):
            f.write(f"{i}. {product} | Qty={data['qty']} | Revenue={data['revenue']:,.2f}\n")
        f.write("\n")

        f.write("TOP 5 CUSTOMERS\n")
        f.write("-" * 40 + "\n")
        for i, (cust, data) in enumerate(top_customers, 1):
            f.write(f"{i}. {cust} | Spent={data['spent']:,.2f} | Orders={data['count']}\n")
        f.write("\n")

        f.write("DAILY SALES TREND\n")
        f.write("-" * 40 + "\n")
        for date in sorted(daily_stats):
            d = daily_stats[date]
            f.write(
                f"{date} | Revenue={d['revenue']:,.2f} | "
                f"Transactions={d['transactions']} | "
                f"Unique Customers={len(d['customers'])}\n"
            )
        f.write("\n")

        f.write("API ENRICHMENT SUMMARY\n")
        f.write("-" * 40 + "\n")
        f.write(f"Total Records: {total_enriched}\n")
        f.write(f"Successfully Enriched: {enriched_count}\n")
        f.write(f"Success Rate: {success_rate:.2f}%\n")
