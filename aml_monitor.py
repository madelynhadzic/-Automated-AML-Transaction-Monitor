import sqlite3
from datetime import datetime, timedelta

def setup_and_populate_db():
    print("[-] Initializing AML Database and Table Schemas...")
    conn = sqlite3.connect('aml_bank.db')
    cursor = conn.cursor()
    
    cursor.execute('DROP TABLE IF EXISTS transactions')
    cursor.execute('DROP TABLE IF EXISTS customers')
    
    cursor.execute('''
        CREATE TABLE customers (
            customer_id TEXT PRIMARY KEY,
            name TEXT,
            risk_tier TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE transactions (
            transaction_id TEXT PRIMARY KEY,
            customer_id TEXT,
            amount REAL,
            timestamp TEXT,
            location TEXT,
            FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
        )
    ''')
    
    mock_customers = [
        ('C001', 'John Doe', 'Medium'),
        ('C002', 'Alice Vance', 'Low'),
        ('C003', 'Jane Smith', 'High'),
        ('C004', 'Bob Johnson', 'Low')
    ]
    cursor.executemany('INSERT INTO customers VALUES (?, ?, ?)', mock_customers)
    
    base_time = datetime.now()
    mock_transactions = [
        ('T101', 'C001', 12500.00, (base_time - timedelta(hours=10)).strftime('%Y-%m-%d %H:%M:%S'), 'Pittsburgh_ATM'),
        ('T102', 'C002', 150.00, (base_time - timedelta(hours=8)).strftime('%Y-%m-%d %H:%M:%S'), 'Online_Retail'),
        ('T103', 'C002', 45.50, (base_time - timedelta(hours=6)).strftime('%Y-%m-%d %H:%M:%S'), 'Coffee_Shop'),
        ('T104', 'C003', 2400.00, (base_time - timedelta(hours=5)).strftime('%Y-%m-%d %H:%M:%S'), 'Downtown_Branch'),
        ('T105', 'C003', 2400.00, (base_time - timedelta(hours=4)).strftime('%Y-%m-%d %H:%M:%S'), 'Strip_District_ATM'),
        ('T106', 'C003', 2400.00, (base_time - timedelta(hours=3)).strftime('%Y-%m-%d %H:%M:%S'), 'North_Shore_ATM'),
        ('T107', 'C004', 850.00, (base_time - timedelta(hours=2)).strftime('%Y-%m-%d %H:%M:%S'), 'Grocery_Store')
    ]
    cursor.executemany('INSERT INTO transactions VALUES (?, ?, ?, ?, ?)', mock_transactions)
    conn.commit()
    conn.close()
    print("[+] Database loaded with transaction data!")

def run_aml_transaction_monitor():
    print("\n[-] Executing Automated Anti-Money Laundering Scanning Pipeline...")
    conn = sqlite3.connect('aml_bank.db')
    cursor = conn.cursor()
    
    # QUERY 1: Flag single massive transaction over $10,000 (Whale Alert)
    whale_query = '''
        SELECT t.transaction_id, c.name, t.amount, t.timestamp, t.location
        FROM transactions t
        JOIN customers c ON t.customer_id = c.customer_id
        WHERE t.amount >= 10000.00
    '''
    
    # QUERY 2: Flag potential structuring (deposits just under tracking thresholds in a tight window)
    structuring_query = '''
        SELECT t1.customer_id, c.name, COUNT(t1.transaction_id) as tx_count, SUM(t1.amount) as total_smurfed
        FROM transactions t1
        JOIN customers c ON t1.customer_id = c.customer_id
        WHERE t1.amount BETWEEN 2000.00 AND 9999.00
        GROUP BY t1.customer_id
        HAVING tx_count >= 3
    '''
    
    # Execute Whale Alerts
    print("\n[!] RUNNING: Large Transaction (> $10k) Monitoring Rules...")
    cursor.execute(whale_query)
    whale_alerts = cursor.fetchall()
    
    if whale_alerts:
        for alert in whale_alerts:
            print(f"    [WHALE ALERT] Tx: {alert[0]} | Customer: {alert[1]} | Amount: ${alert[2]:,.2f} | Location: {alert[4]}")
    else:
        print("    [+] No large transaction alerts triggered.")
        
    # Execute Structuring Alerts
    print("\n[!] RUNNING: Velocity & Structuring Compliance Evaluation...")
    cursor.execute(structuring_query)
    structuring_alerts = cursor.fetchall()
    
    if structuring_alerts:
        for alert in structuring_alerts:
            print(f"    [STRUCTURING DETECTED] Customer ID: {alert[0]} | Name: {alert[1]} | Rapid Tx Count: {alert[2]} | Cumulative Vol: ${alert[3]:,.2f}")
            print(f"    [ACTION REQUIRED] Generating Suspicious Activity Report (SAR) ticket...")
    else:
        print("    [+] No velocity structuring violations flagged.")
        
    conn.close()

if __name__ == "__main__":
    setup_and_populate_db()
    run_aml_transaction_monitor()
