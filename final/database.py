import sqlite3

stocks = "stocks.db"

def init_db() -> None: 
    conn = sqlite3.connect(stocks)
    cursor = conn.cursor()  
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS stocks (
        id INTEGER PRIMARY KEY,
        stock TEXT,
        shares REAL,
        purchase_price REAL,
        purchase_date TEXT)
    """)
    conn.commit()
    conn.close()

def add_stock(stock: str, shares: float, purchase_price: float, purchase_date: str):
    conn = sqlite3.connect(stocks)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO stocks (stock, shares, purchase_price, purchase_date)
        VALUES (?, ?, ?, ?)
        """,
        (stock, shares, purchase_price, purchase_date)
    )
    conn.commit()
    conn.close()

def remove_stock(stock_to_delete: str):
    conn = sqlite3.connect(stocks)
    cursor = conn.cursor()
    cursor.execute(
        """
        DELETE FROM stocks WHERE id = ?
        """,
        (stock_to_delete)
    )
    conn.commit()
    conn.close()

def get_stocks():
    conn = sqlite3.connect(stocks)
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT * FROM stocks
        """
    )
    return cursor.fetchall()

def get_stock(ticker):
    conn = sqlite3.connect(stocks)
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT * FROM stocks
        WHERE id = ?
        """,
        (ticker,)
    )
    return cursor.fetchall()

def update_stock(new_shares: float, new_purchase_price: float, new_purchase_date: str):
    conn = sqlite3.connect(stocks)
    cursor = conn.cursor()
    cursor.execute(
        """
        UPDATE stocks
        SET shares = ?, purchase_price = ?, purchase_date = ?
        WHERE id = ?
        """,
        (new_shares, new_purchase_price, new_purchase_date)
    )
    conn.commit()
    conn.close()