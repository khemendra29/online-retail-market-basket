# Retail Product Association Analysis

Finding which products are bought together in online retail data, using FP-Growth.

## Problem
Online retailers need to know which products are frequently bought together so they can
design product recommendations, promotions and store layouts.

## Dataset
UCI Online Retail dataset: https://archive.ics.uci.edu/dataset/352/online+retail

Chen, D. (2015). *Online Retail* [Dataset]. UCI Machine Learning Repository.
https://doi.org/10.24432/C5BW33

The data is not stored in this repository. Download `Online Retail.xlsx` from the link
above and place it next to the notebook.

| Column | Meaning |
|---|---|
| InvoiceNo | Order number (a leading "C" marks a cancellation) |
| StockCode | Product code |
| Description | Product name |
| Quantity | Units in the order line |
| InvoiceDate | Date and time of the order |
| UnitPrice | Price per unit in GBP |
| CustomerID | Customer number (many missing) |
| Country | Customer's country |

## Method
1. **Cleaning** (541,909 -> 522,504 rows): removed cancellations, zero or negative
   quantity and price, non-product codes (POST, DOT, M, vouchers) and 5,221 duplicates;
   gave each product code one consistent name.
2. **Baskets:** kept UK orders and the 150 most popular products; one invoice = one basket;
   kept baskets with 2+ items (12,884); 80/20 train/test split (10,307 / 2,577).
3. **FP-Growth** with minimum support 0.02 -> 514 frequent itemsets -> 612 rules
   (confidence >= 0.3, lift > 1).
4. **Comparison** of FP-Growth and Apriori at four support levels.
5. **Evaluation** on unseen baskets: one item is hidden and the rules try to predict it.

## Results
- Hit rate @5: 27.4% (about 9x random guessing), coverage 87.2%, precision when covered 31.5%
- FP-Growth and Apriori find identical itemsets; FP-Growth is faster at low minimum support.
- Example rule: Roses Regency Teacup and Saucer -> Regency Cakestand 3 Tier
  (confidence 0.48, lift 3.8)

## How to run
1. Open `notebooks/fp_growth.ipynb` in Google Colab, upload `Online Retail.xlsx`, run all
   cells. The last cells create `basket.db`.
2. Put `basket.db` in the `app/` folder, then:
```
pip install -r requirements.txt
cd app
python -m streamlit run app.py
```

## Limitations
One UK retailer with many wholesale customers, one seasonal year, top 150 products only,
and associations are not causes.

## Author
Khemendra
