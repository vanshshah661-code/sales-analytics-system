import requests


def fetch_all_products():
    """
    Task 3.1(a): Fetch all products from DummyJSON API
    """
    url = "https://dummyjson.com/products?limit=100"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        print("API fetch successful")
        return data.get("products", [])

    except requests.RequestException as e:
        print("API fetch failed:", e)
        return []


def create_product_mapping(api_products):
    """
    Task 3.1(b): Create mapping of product ID to product info
    """
    mapping = {}

    for product in api_products:
        pid = product.get("id")
        mapping[pid] = {
            "category": product.get("category"),
            "brand": product.get("brand"),
            "rating": product.get("rating"),
        }

    return mapping


def enrich_sales_data(transactions, product_mapping):
    """
    Task 3.2: Enrich sales data with API product info
    """
    enriched = []

    for t in transactions:
        enriched_t = t.copy()

        # Extract numeric ID from ProductID (P101 -> 101)
        try:
            numeric_id = int(t["ProductID"][1:])
        except:
            numeric_id = None

        if numeric_id in product_mapping:
            api_info = product_mapping[numeric_id]
            enriched_t["API_Category"] = api_info["category"]
            enriched_t["API_Brand"] = api_info["brand"]
            enriched_t["API_Rating"] = api_info["rating"]
            enriched_t["API_Match"] = True
        else:
            enriched_t["API_Category"] = None
            enriched_t["API_Brand"] = None
            enriched_t["API_Rating"] = None
            enriched_t["API_Match"] = False

        enriched.append(enriched_t)

    return enriched


def save_enriched_data(enriched_transactions, filename="data/enriched_sales_data.txt"):
    """
    Saves enriched transactions to pipe-delimited file
    """
    headers = [
        "TransactionID", "Date", "ProductID", "ProductName",
        "Quantity", "UnitPrice", "CustomerID", "Region",
        "API_Category", "API_Brand", "API_Rating", "API_Match"
    ]

    with open(filename, "w", encoding="utf-8") as file:
        file.write("|".join(headers) + "\n")

        for t in enriched_transactions:
            row = [
                str(t.get("TransactionID")),
                str(t.get("Date")),
                str(t.get("ProductID")),
                str(t.get("ProductName")),
                str(t.get("Quantity")),
                str(t.get("UnitPrice")),
                str(t.get("CustomerID")),
                str(t.get("Region")),
                str(t.get("API_Category")),
                str(t.get("API_Brand")),
                str(t.get("API_Rating")),
                str(t.get("API_Match")),
            ]
            file.write("|".join(row) + "\n")

    print("Enriched data saved to", filename)
