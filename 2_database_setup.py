import sqlite3
import pandas as pd
import json
import os

def create_database():
    """
    Create SQLite database and tables for the banking system.
    """
    
    # Create database directory if it doesn't exist
    if not os.path.exists('database'):
        os.makedirs('database')
    
    # Connect to SQLite database
    conn = sqlite3.connect('database/banking.db')
    cursor = conn.cursor()
    
    print("Creating database tables...")
    
    # 1. Create Customers Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS customers (
        customer_id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        gender TEXT,
        age INTEGER,
        city TEXT,
        account_type TEXT,
        join_date DATE
    )
    ''')
    print("✓ Created customers table")
    
    # 2. Create Accounts Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS accounts (
        customer_id TEXT PRIMARY KEY,
        account_balance REAL,
        last_updated DATETIME,
        FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
    )
    ''')
    print("✓ Created accounts table")
    
    # 3. Create Transactions Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS transactions (
        txn_id TEXT PRIMARY KEY,
        customer_id TEXT,
        txn_type TEXT,
        amount REAL,
        txn_time DATETIME,
        status TEXT,
        FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
    )
    ''')
    print("✓ Created transactions table")
    
    # 4. Create Branches Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS branches (
        Branch_ID INTEGER PRIMARY KEY,
        Branch_Name TEXT,
        City TEXT,
        Manager_Name TEXT,
        Total_Employees INTEGER,
        Branch_Revenue REAL,
        Opening_Date DATE,
        Performance_Rating INTEGER
    )
    ''')
    print("✓ Created branches table")
    
    # 5. Create Loans Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS loans (
        Loan_ID INTEGER PRIMARY KEY,
        Customer_ID INTEGER,
        Account_ID INTEGER,
        Branch TEXT,
        Loan_Type TEXT,
        Loan_Amount INTEGER,
        Interest_Rate REAL,
        Loan_Term_Months INTEGER,
        Start_Date DATE,
        End_Date DATE,
        Loan_Status TEXT
    )
    ''')
    print("✓ Created loans table")
    
    # 6. Create Credit Cards Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS credit_cards (
        Card_ID INTEGER PRIMARY KEY,
        Customer_ID INTEGER,
        Account_ID INTEGER,
        Branch TEXT,
        Card_Number TEXT,
        Card_Type TEXT,
        Card_Network TEXT,
        Credit_Limit INTEGER,
        Current_Balance REAL,
        Issued_Date DATE,
        Expiry_Date DATE,
        Status TEXT
    )
    ''')
    print("✓ Created credit_cards table")
    
    # 7. Create Support Tickets Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS support_tickets (
        Ticket_ID TEXT PRIMARY KEY,
        Customer_ID TEXT,
        Account_ID TEXT,
        Loan_ID TEXT,
        Branch_Name TEXT,
        Issue_Category TEXT,
        Description TEXT,
        Date_Opened DATE,
        Date_Closed DATE,
        Priority TEXT,
        Status TEXT,
        Resolution_Remarks TEXT,
        Support_Agent TEXT,
        Channel TEXT,
        Customer_Rating INTEGER
    )
    ''')
    print("✓ Created support_tickets table")
    
    conn.commit()
    print("\n✅ All tables created successfully!")
    
    return conn

def load_data_to_database(conn):
    """
    Load data from CSV and JSON files into the database.
    """
    
    print("\nLoading data into database...")
    
    # 1. Load Customers
    customers_df = pd.read_csv('data/customers.csv')
    customers_df.to_sql('customers', conn, if_exists='replace', index=False)
    print(f"✓ Loaded {len(customers_df)} customers")
    
    # 2. Load Accounts
    accounts_df = pd.read_csv('data/accounts.csv')
    accounts_df.to_sql('accounts', conn, if_exists='replace', index=False)
    print(f"✓ Loaded {len(accounts_df)} accounts")
    
    # 3. Load Transactions
    transactions_df = pd.read_csv('data/transactions.csv')
    transactions_df.to_sql('transactions', conn, if_exists='replace', index=False)
    print(f"✓ Loaded {len(transactions_df)} transactions")
    
    # 4. Load Branches
    with open('data/branches.json', 'r') as f:
        branches_data = json.load(f)
    branches_df = pd.DataFrame(branches_data)
    branches_df.to_sql('branches', conn, if_exists='replace', index=False)
    print(f"✓ Loaded {len(branches_df)} branches")
    
    # 5. Load Loans
    with open('data/loans.json', 'r') as f:
        loans_data = json.load(f)
    loans_df = pd.DataFrame(loans_data)
    loans_df.to_sql('loans', conn, if_exists='replace', index=False)
    print(f"✓ Loaded {len(loans_df)} loans")
    
    # 6. Load Credit Cards
    with open('data/credit_cards.json', 'r') as f:
        credit_cards_data = json.load(f)
    credit_cards_df = pd.DataFrame(credit_cards_data)
    credit_cards_df.to_sql('credit_cards', conn, if_exists='replace', index=False)
    print(f"✓ Loaded {len(credit_cards_df)} credit cards")
    
    # 7. Load Support Tickets
    support_tickets_df = pd.read_csv('data/support_tickets.csv')
    support_tickets_df.to_sql('support_tickets', conn, if_exists='replace', index=False)
    print(f"✓ Loaded {len(support_tickets_df)} support tickets")
    
    conn.commit()
    print("\n✅ All data loaded successfully!")

if __name__ == "__main__":
    conn = create_database()
    load_data_to_database(conn)
    conn.close()
    print("\n🎉 Database setup complete! Database saved at: database/banking.db")
