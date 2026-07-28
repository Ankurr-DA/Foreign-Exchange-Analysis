# Foreign Exchange Revenue & Risk Analysis

> 📌 **Project Documentation & Workflow**  
> To view the complete step-by-step code execution, SQL views, audit conditions, and risk modeling logic, access the full PDF document:  
> 📄 [**Read the Foreign Exchange Project Workflow (PDF)**]()

---

## Project Overview
This end-to-end foreign exchange data & risk analysis project transforms raw international payment records and exchange rates into structured Excel risk reports and an executive risk dashboard. The objective of this analysis is to monitor global currency corridor performance, track cross-border fee revenue, and flag operational failures to calculate fee revenue at risk.

## Data Pipeline & Architecture
The project follows a structured ETL (Extract, Transform, Load) pipeline:  
**CSV → MySQL → SQL Views → Python Data Audit → Excel → Tableau**

1. **Database Ingestion:** Ingested three core raw dataset files (`fx_rates.csv`, `international_payments.csv`, `payment_status.csv`) into a MySQL database via Python `sqlalchemy`.
2. **SQL Auditing & Views:** Ran comprehensive data quality checks to identify missing foreign exchange rates, unlinked payment IDs, negative transaction values, and invalid currency pair strings. Created optimized SQL views (`v_payment_rates` and `v_delivery_status`) for stream processing.
3. **Python Cleaning & Normalization:** Standardized currency pair separators (`-` and `_` to `/`), cleaned country names to uppercase, parsed date objects, and enforced positive absolute values across financial metrics.
4. **Audit Classification & Reporting:** Built a dynamic rule engine in Python (`np.select`) to flag non-compliant transactions into four audit risk buckets, producing two core executive exports:
   - **Operational Failure Report:** Aggregates transaction volume, total impacted amount, fee at risk, and percentage financial impact across flagged audit statuses.
   - **FX Corridor Report:** Ranks valid currency pairs by fee revenue, total volume sent, average delivery SLA hours, and top sender country.
5. **Dashboard Visualization:** Connected the output reports into a Tableau dashboard to highlight KPI metric cards, currency corridor volumes, and fee risk breakdowns.

---

## Project Deliverables & Visual Preview

### 1. Operational Failure Report
Evaluates unresolved transactions across audit failure categories (Missing Rate & Pair, Missing Status, Missing Financials, and Missing Delivery Time), calculating total financial exposure and fee at risk.  
![Operational Failure Report]()

### 2. FX Corridor Report
Tracks global payment corridors (e.g., USD/GBP, USD/EUR, EUR/GBP), analyzing total fee generation, amount circulated, average transfer delivery hours, and sender market concentration.  
![FX Corridor Report]()

---

### 3. Live Tableau Executive Dashboard
Interactive dashboard displaying key financial metrics: **$4.20M** total circulated amount, **$73K** fee revenue generated, **508** unresolved transactions, **$571K** unresolved amount, and **$9,259** total fee revenue at risk. Features breakdown charts for currency pair volumes, issue impacts, country fee contributions, and fee at risk per audit status.  
![Foreign Exchange Revenue & Risk Dashboard](Dashboard_image.jpg)

---

## Repository Structure
* `Foreign_Exchange_Project_Workflow.pdf`: Full project documentation, SQL scripts, and Python transformation logic.
* `fx_rates.csv`: Raw exchange rate market data.
* `international_payments.csv`: Raw cross-border transaction logs.
* `payment_status.csv`: Raw delivery time and failure log dataset.
* `data_transfer2.py`: Python script loading CSV files into MySQL.
* `SQL_Analytics2.sql`: Audit queries, data cleanliness checks, and view definitions.
* `python_analytics2.py`: Data cleaning script, audit classification logic, and report exports.
* `Final_Operational_Failure.xlsx`: Generated operational failure and risk report export.
* `Final_FX_Corridor.xlsx`: Generated currency corridor performance export.

## Technologies Used
* **Languages:** Python (`pandas`, `sqlalchemy`, `numpy`), SQL
* **Database:** MySQL
* **Reporting & Viz:** Excel, Tableau, Matplotlib
* **Environment:** VS Code
