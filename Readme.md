
# Sales Analytics System

This project reads raw sales transaction data from a text file, cleans and validates the data, performs sales analysis, and generates a summary report.

---

##  Project Structure

```
sales-analytics-system/
│
├── main.py
├── requirements.txt
├── README.md
│
├── utils/
│   ├── file_handler.py
│   └── data_processor.py
│
├── data/
│   └── sales_data.txt
│
└── output/
    └── report.txt
```

---

##  Requirements

- Python 3.x
- No external libraries required

---

##  How to Run the Code

1. Make sure the file `sales_data.txt` is placed inside the `data` folder.
2. Open a terminal in the project root directory (`sales-analytics-system`).
3. Run the following command:

```
python main.py
```

---

##  Output

After running the program:

- The terminal displays:
  - Total records parsed
  - Invalid records removed
  - Valid records after cleaning

- A report file is generated at:

```
output/report.txt
```

The report includes:
- Total sales
- Sales by region
- Top-selling products

---

##  Data Cleaning Rules

- TransactionID must start with `T`
- Quantity must be greater than 0
- Unit price must be greater than 0
- CustomerID and Region must not be empty
- Commas are removed from numeric fields and product names

Records that violate these rules are excluded from analysis.

---

##  Notes

- The input file must be pipe (`|`) delimited.
- The program is modular and separates file handling and data processing logic.
- The project can be extended to include API integration if required.

---

##  Author

Vansh Shah
```
