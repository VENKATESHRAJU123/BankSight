import pandas as pd
import json
import numpy as np
from datetime import datetime, timedelta
import random

def generate_sample_data():
    """
    Generate sample datasets for the banking system.
    This creates realistic sample data matching the schema.
    """
    
    # 1. Generate Customers Dataset
    print("Generating customers data...")
    cities = ['Mumbai', 'Delhi', 'Bangalore', 'Hyderabad', 'Chennai', 'Kolkata', 'Pune', 'Ahmedabad']
    account_types = ['Savings', 'Current', 'Salary', 'Fixed Deposit']
    genders = ['M', 'F']
    
    customers_data = []
    for i in range(1, 501):  # 500 customers
        customer_id = f'CUST{str(i).zfill(5)}'
        name = f'Customer {i}'
        gender = random.choice(genders)
        age = random.randint(18, 75)
        city = random.choice(cities)
        account_type = random.choice(account_types)
        join_date = (datetime.now() - timedelta(days=random.randint(1, 1825))).strftime('%Y-%m-%d')
        
        customers_data.append({
            'customer_id': customer_id,
            'name': name,
            'gender': gender,
            'age': age,
            'city': city,
            'account_type': account_type,
            'join_date': join_date
        })
    
    customers_df = pd.DataFrame(customers_data)
    customers_df.to_csv('data/customers.csv', index=False)
    print(f"✓ Created customers.csv with {len(customers_df)} records")
    
    # 2. Generate Accounts Dataset
    print("Generating accounts data...")
    accounts_data = []
    for customer_id in customers_df['customer_id']:
        account_balance = round(random.uniform(1000, 500000), 2)
        last_updated = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        accounts_data.append({
            'customer_id': customer_id,
            'account_balance': account_balance,
            'last_updated': last_updated
        })
    
    accounts_df = pd.DataFrame(accounts_data)
    accounts_df.to_csv('data/accounts.csv', index=False)
    print(f"✓ Created accounts.csv with {len(accounts_df)} records")
    
    # 3. Generate Transactions Dataset
    print("Generating transactions data...")
    txn_types = ['deposit', 'withdrawal', 'transfer', 'online purchase', 'ATM withdrawal', 'online fraud']
    statuses = ['success', 'failed']
    
    transactions_data = []
    txn_count = 0
    
    for customer_id in customers_df['customer_id'].sample(n=400):  # 400 customers have transactions
        num_transactions = random.randint(5, 30)
        
        for _ in range(num_transactions):
            txn_count += 1
            txn_id = f'TXN{str(txn_count).zfill(7)}'
            txn_type = random.choice(txn_types)
            
            # Fraud transactions are rare and have different amounts
            if txn_type == 'online fraud':
                amount = round(random.uniform(50000, 200000), 2)
                status = random.choice(['success', 'failed', 'failed'])  # More likely to fail
            else:
                amount = round(random.uniform(100, 50000), 2)
                status = random.choice(statuses) if random.random() > 0.9 else 'success'
            
            txn_time = (datetime.now() - timedelta(days=random.randint(1, 365), 
                                                   hours=random.randint(0, 23),
                                                   minutes=random.randint(0, 59))).strftime('%Y-%m-%d %H:%M:%S')
            
            transactions_data.append({
                'txn_id': txn_id,
                'customer_id': customer_id,
                'txn_type': txn_type,
                'amount': amount,
                'txn_time': txn_time,
                'status': status
            })
    
    transactions_df = pd.DataFrame(transactions_data)
    transactions_df.to_csv('data/transactions.csv', index=False)
    print(f"✓ Created transactions.csv with {len(transactions_df)} records")
    
    # 4. Generate Branches Dataset
    print("Generating branches data...")
    branches_data = []
    branch_cities = ['Mumbai', 'Delhi', 'Bangalore', 'Hyderabad', 'Chennai', 'Kolkata', 'Pune', 'Ahmedabad']
    
    for i, city in enumerate(branch_cities, 1):
        branches_data.append({
            'Branch_ID': i,
            'Branch_Name': f'{city} Main Branch',
            'City': city,
            'Manager_Name': f'Manager {i}',
            'Total_Employees': random.randint(15, 50),
            'Branch_Revenue': round(random.uniform(5000000, 20000000), 2),
            'Opening_Date': (datetime.now() - timedelta(days=random.randint(365, 3650))).strftime('%Y-%m-%d'),
            'Performance_Rating': random.randint(3, 5)
        })
    
    with open('data/branches.json', 'w') as f:
        json.dump(branches_data, f, indent=2)
    print(f"✓ Created branches.json with {len(branches_data)} records")
    
    # 5. Generate Loans Dataset
    print("Generating loans data...")
    loan_types = ['Personal', 'Home', 'Auto', 'Business', 'Education']
    loan_statuses = ['Active', 'Closed', 'Approved']
    
    loans_data = []
    for i in range(1, 301):  # 300 loans
        customer_id_num = random.randint(1, 500)
        loans_data.append({
            'Loan_ID': i,
            'Customer_ID': customer_id_num,
            'Account_ID': customer_id_num,
            'Branch': random.choice(branch_cities),
            'Loan_Type': random.choice(loan_types),
            'Loan_Amount': random.randint(50000, 5000000),
            'Interest_Rate': round(random.uniform(7.5, 15.0), 2),
            'Loan_Term_Months': random.choice([12, 24, 36, 48, 60, 84, 120, 180, 240]),
            'Start_Date': (datetime.now() - timedelta(days=random.randint(1, 730))).strftime('%Y-%m-%d'),
            'End_Date': (datetime.now() + timedelta(days=random.randint(365, 3650))).strftime('%Y-%m-%d'),
            'Loan_Status': random.choice(loan_statuses)
        })
    
    with open('data/loans.json', 'w') as f:
        json.dump(loans_data, f, indent=2)
    print(f"✓ Created loans.json with {len(loans_data)} records")
    
    # 6. Generate Credit Cards Dataset
    print("Generating credit cards data...")
    card_types = ['Silver', 'Gold', 'Platinum', 'Business']
    card_networks = ['Visa', 'MasterCard', 'RuPay', 'Amex']
    card_statuses = ['Active', 'Expired', 'Blocked']
    
    credit_cards_data = []
    for i in range(1, 401):  # 400 credit cards
        customer_id_num = random.randint(1, 500)
        issued_date = datetime.now() - timedelta(days=random.randint(1, 1825))
        
        credit_cards_data.append({
            'Card_ID': i,
            'Customer_ID': customer_id_num,
            'Account_ID': customer_id_num,
            'Branch': random.choice(branch_cities),
            'Card_Number': ''.join([str(random.randint(0, 9)) for _ in range(16)]),
            'Card_Type': random.choice(card_types),
            'Card_Network': random.choice(card_networks),
            'Credit_Limit': random.choice([50000, 100000, 200000, 500000, 1000000]),
            'Current_Balance': round(random.uniform(0, 50000), 2),
            'Issued_Date': issued_date.strftime('%Y-%m-%d'),
            'Expiry_Date': (issued_date + timedelta(days=1825)).strftime('%Y-%m-%d'),
            'Status': random.choice(card_statuses)
        })
    
    with open('data/credit_cards.json', 'w') as f:
        json.dump(credit_cards_data, f, indent=2)
    print(f"✓ Created credit_cards.json with {len(credit_cards_data)} records")
    
    # 7. Generate Support Tickets Dataset
    print("Generating support tickets data...")
    issue_categories = ['Loan Payment Delay', 'Card Not Working', 'EMI Auto-debit Failed', 
                       'Account Balance Mismatch', 'Online Banking Issue', 'ATM Card Blocked']
    priorities = ['Low', 'Medium', 'High', 'Critical']
    ticket_statuses = ['Resolved', 'Closed', 'In Progress', 'Open']
    channels = ['Email', 'Phone', 'In-person', 'Chat']
    
    support_tickets_data = []
    for i in range(1, 251):  # 250 support tickets
        date_opened = datetime.now() - timedelta(days=random.randint(1, 365))
        is_closed = random.choice([True, True, False])  # 2/3 chance of being closed
        
        support_tickets_data.append({
            'Ticket_ID': f'TKT{str(i).zfill(5)}',
            'Customer_ID': f'CUST{str(random.randint(1, 500)).zfill(5)}',
            'Account_ID': f'CUST{str(random.randint(1, 500)).zfill(5)}',
            'Loan_ID': random.randint(1, 300) if random.random() > 0.5 else '',
            'Branch_Name': random.choice([f'{city} Main Branch' for city in branch_cities]),
            'Issue_Category': random.choice(issue_categories),
            'Description': f'Issue description for ticket {i}',
            'Date_Opened': date_opened.strftime('%Y-%m-%d'),
            'Date_Closed': (date_opened + timedelta(days=random.randint(1, 30))).strftime('%Y-%m-%d') if is_closed else '',
            'Priority': random.choice(priorities),
            'Status': random.choice(['Resolved', 'Closed']) if is_closed else random.choice(['In Progress', 'Open']),
            'Resolution_Remarks': f'Resolution remarks for ticket {i}' if is_closed else '',
            'Support_Agent': f'Agent {random.randint(1, 20)}',
            'Channel': random.choice(channels),
            'Customer_Rating': random.randint(1, 5) if is_closed else ''
        })
    
    support_tickets_df = pd.DataFrame(support_tickets_data)
    support_tickets_df.to_csv('data/support_tickets.csv', index=False)
    print(f"✓ Created support_tickets.csv with {len(support_tickets_df)} records")
    
    print("\n✅ All datasets generated successfully!")

if __name__ == "__main__":
    import os
    
    # Create data directory if it doesn't exist
    if not os.path.exists('data'):
        os.makedirs('data')
    
    generate_sample_data()
