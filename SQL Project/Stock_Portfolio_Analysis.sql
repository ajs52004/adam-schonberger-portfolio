CREATE DATABASE IF NOT EXISTS portfolio_db;
USE portfolio_db;

DROP TABLE IF EXISTS Transactions;
DROP TABLE IF EXISTS Stocks;

-- Create Stocks table
CREATE TABLE Stocks (
    stock_id INTEGER PRIMARY KEY,
    ticker TEXT,
    company_name TEXT
);

-- Create Transactions table
CREATE TABLE Transactions (
    transaction_id INTEGER PRIMARY KEY,
    stock_id INTEGER,
    transaction_date DATE,
    quantity INTEGER,
    price_per_share REAL,
    transaction_type TEXT,
    FOREIGN KEY (stock_id) REFERENCES Stocks(stock_id)
);

-- Insert data into Stocks
INSERT INTO Stocks VALUES
(1, 'AAPL', 'Apple Inc.'),
(2, 'MSFT', 'Microsoft Corp.'),
(3, 'GOOGL', 'Alphabet Inc.'),
(4, 'TSLA', 'Tesla Inc.'),
(5, 'AMZN', 'Amazon.com Inc.'),
(6, 'NVDA', 'NVIDIA Corp.');

-- Insert data into Transactions
INSERT INTO Transactions VALUES
(1, 1, '2024-01-10', 50, 150.00, 'BUY'),
(2, 1, '2024-03-15', 20, 160.00, 'SELL'),
(3, 2, '2024-02-05', 30, 300.00, 'BUY'),
(4, 3, '2024-01-20', 10, 2800.00, 'BUY'),
(5, 3, '2024-04-10', 5, 2900.00, 'SELL'),
(6, 4, '2024-02-01', 15, 700.00, 'BUY'),
(7, 4, '2024-05-01', 5, 750.00, 'SELL'),
(8, 5, '2024-03-01', 8, 3300.00, 'BUY'),
(9, 6, '2024-04-20', 12, 800.00, 'BUY'),
(10, 6, '2024-05-15', 6, 850.00, 'SELL');

-- Query 1: Net shares per stock
SELECT
    s.ticker,
    SUM(CASE WHEN t.transaction_type = 'BUY' THEN t.quantity ELSE -t.quantity END) AS net_shares
FROM Transactions t
JOIN Stocks s ON t.stock_id = s.stock_id
GROUP BY s.ticker;

-- Query 2: Total invested and earned
SELECT
    s.ticker,
    SUM(CASE WHEN t.transaction_type = 'BUY' THEN t.quantity * t.price_per_share ELSE 0 END) AS total_invested,
    SUM(CASE WHEN t.transaction_type = 'SELL' THEN t.quantity * t.price_per_share ELSE 0 END) AS total_earned
FROM Transactions t
JOIN Stocks s ON t.stock_id = s.stock_id
GROUP BY s.ticker;

-- Query 3: Net cash flow
SELECT
    s.ticker,
    SUM(CASE WHEN t.transaction_type = 'BUY' THEN -t.quantity * t.price_per_share ELSE t.quantity * t.price_per_share END) AS net_cash_flow
FROM Transactions t
JOIN Stocks s ON t.stock_id = s.stock_id
GROUP BY s.ticker;

-- Query 4: Average buy price
SELECT
    s.ticker,
    CASE 
        WHEN SUM(CASE WHEN t.transaction_type = 'BUY' THEN t.quantity ELSE 0 END) > 0 THEN
            SUM(CASE WHEN t.transaction_type = 'BUY' THEN t.quantity * t.price_per_share ELSE 0 END) /
            SUM(CASE WHEN t.transaction_type = 'BUY' THEN t.quantity ELSE 0 END)
        ELSE 0
    END AS avg_buy_price
FROM Transactions t
JOIN Stocks s ON t.stock_id = s.stock_id
GROUP BY s.ticker;

-- Query 5: Unrealized position value (using assumed current prices)
WITH CurrentPrices AS (
    SELECT 'AAPL' AS ticker, 170.00 AS current_price
    UNION ALL SELECT 'MSFT', 310.00
    UNION ALL SELECT 'GOOGL', 2850.00
    UNION ALL SELECT 'TSLA', 720.00
    UNION ALL SELECT 'AMZN', 3400.00
    UNION ALL SELECT 'NVDA', 820.00
)
SELECT
    s.ticker,
    SUM(CASE WHEN t.transaction_type = 'BUY' THEN t.quantity ELSE -t.quantity END) AS net_shares,
    cp.current_price,
    SUM(CASE WHEN t.transaction_type = 'BUY' THEN t.quantity ELSE -t.quantity END) * cp.current_price AS unrealized_value
FROM Transactions t
JOIN Stocks s ON t.stock_id = s.stock_id
JOIN CurrentPrices cp ON s.ticker = cp.ticker
GROUP BY s.ticker, cp.current_price;

