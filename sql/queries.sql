-- Top 5 funds by AUM

SELECT scheme_name, aum_crore
FROM fact_performance
ORDER BY aum_crore DESC
LIMIT 5;

-- Average 1 Year Return

SELECT AVG(return_1yr_pct) AS avg_return
FROM fact_performance;

-- Average Expense Ratio

SELECT AVG(expense_ratio_pct) AS avg_expense_ratio
FROM fact_performance;

-- Total Transactions

SELECT COUNT(*) AS total_transactions
FROM fact_transactions;

-- Transaction Type Distribution

SELECT transaction_type, COUNT(*)
FROM fact_transactions
GROUP BY transaction_type;

-- Highest NAV

SELECT MAX(nav) AS highest_nav
FROM fact_nav;

-- Lowest NAV

SELECT MIN(nav) AS lowest_nav
FROM fact_nav;

-- Average NAV

SELECT AVG(nav) AS average_nav
FROM fact_nav;

-- Fund Count by Category

SELECT category, COUNT(*)
FROM fact_performance
GROUP BY category;

-- Fund Count by Plan

SELECT plan, COUNT(*)
FROM fact_performance
GROUP BY plan;