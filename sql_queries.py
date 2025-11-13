"""
Contains all 15+ SQL queries for banking analytics.
Each query is a function that returns the SQL string and description.
"""
import pandas as pd
import sqlite3

def get_all_queries():
    """
    Returns a dictionary of all analytical queries.
    """
    
    queries = {
        "Q1: Customers per City with Avg Balance": {
            "description": "How many customers exist per city, and what is their average account balance?",
            "query": """
                SELECT 
                    c.city,
                    COUNT(c.customer_id) as total_customers,
                    ROUND(AVG(a.account_balance), 2) as avg_balance,
                    ROUND(MIN(a.account_balance), 2) as min_balance,
                    ROUND(MAX(a.account_balance), 2) as max_balance
                FROM customers c
                JOIN accounts a ON c.customer_id = a.customer_id
                GROUP BY c.city
                ORDER BY total_customers DESC
            """
        },
        
        "Q2: Account Type with Highest Total Balance": {
            "description": "Which account type holds the highest total balance?",
            "query": """
                SELECT 
                    c.account_type,
                    COUNT(c.customer_id) as total_accounts,
                    ROUND(SUM(a.account_balance), 2) as total_balance,
                    ROUND(AVG(a.account_balance), 2) as avg_balance
                FROM customers c
                JOIN accounts a ON c.customer_id = a.customer_id
                GROUP BY c.account_type
                ORDER BY total_balance DESC
            """
        },
        
        "Q3: Top 10 Customers by Balance": {
            "description": "Who are the top 10 customers by total account balance?",
            "query": """
                SELECT 
                    c.customer_id,
                    c.name,
                    c.city,
                    c.account_type,
                    ROUND(a.account_balance, 2) as balance
                FROM customers c
                JOIN accounts a ON c.customer_id = a.customer_id
                ORDER BY a.account_balance DESC
                LIMIT 10
            """
        },
        
        "Q4: 2023 Customers with Balance > 100K": {
            "description": "Which customers opened accounts in 2023 with balance above ₹1,00,000?",
            "query": """
                SELECT 
                    c.customer_id,
                    c.name,
                    c.city,
                    c.join_date,
                    ROUND(a.account_balance, 2) as balance
                FROM customers c
                JOIN accounts a ON c.customer_id = a.customer_id
                WHERE strftime('%Y', c.join_date) = '2023'
                AND a.account_balance > 100000
                ORDER BY a.account_balance DESC
            """
        },
        
        "Q5: Transaction Volume by Type": {
            "description": "What is the total transaction volume by transaction type?",
            "query": """
                SELECT 
                    txn_type,
                    COUNT(*) as total_transactions,
                    ROUND(SUM(amount), 2) as total_volume,
                    ROUND(AVG(amount), 2) as avg_amount,
                    COUNT(CASE WHEN status = 'success' THEN 1 END) as successful,
                    COUNT(CASE WHEN status = 'failed' THEN 1 END) as failed
                FROM transactions
                GROUP BY txn_type
                ORDER BY total_volume DESC
            """
        },
        
        "Q6: Accounts with 3+ Failed Transactions": {
            "description": "Which accounts have more than 3 failed transactions in a single month?",
            "query": """
                SELECT 
                    t.customer_id,
                    c.name,
                    strftime('%Y-%m', t.txn_time) as month,
                    COUNT(*) as failed_count,
                    ROUND(SUM(t.amount), 2) as total_failed_amount
                FROM transactions t
                JOIN customers c ON t.customer_id = c.customer_id
                WHERE t.status = 'failed'
                GROUP BY t.customer_id, strftime('%Y-%m', t.txn_time)
                HAVING COUNT(*) > 3
                ORDER BY failed_count DESC
            """
        },
        
        "Q7: Top 5 Branches by Transaction Volume (6 months)": {
            "description": "Top 5 branches by total transaction volume in the last 6 months",
            "query": """
                SELECT 
                    b.Branch_Name,
                    b.City,
                    COUNT(DISTINCT l.Customer_ID) as total_customers,
                    COUNT(l.Loan_ID) as total_loans,
                    ROUND(SUM(l.Loan_Amount), 2) as total_loan_volume
                FROM branches b
                LEFT JOIN loans l ON b.City = l.Branch
                WHERE l.Start_Date >= date('now', '-6 months')
                GROUP BY b.Branch_Name, b.City
                ORDER BY total_loan_volume DESC
                LIMIT 5
            """
        },
        
        "Q8: Accounts with 5+ High-Value Transactions": {
            "description": "Which accounts have 5 or more transactions above ₹2,00,000?",
            "query": """
                SELECT 
                    t.customer_id,
                    c.name,
                    c.city,
                    COUNT(*) as high_value_txn_count,
                    ROUND(SUM(t.amount), 2) as total_high_value_amount,
                    ROUND(AVG(t.amount), 2) as avg_high_value_amount
                FROM transactions t
                JOIN customers c ON t.customer_id = c.customer_id
                WHERE t.amount > 200000
                GROUP BY t.customer_id
                HAVING COUNT(*) >= 5
                ORDER BY high_value_txn_count DESC
            """
        },
        
        "Q9: Loan Analysis by Type": {
            "description": "Average loan amount and interest rate by loan type",
            "query": """
                SELECT 
                    Loan_Type,
                    COUNT(*) as total_loans,
                    ROUND(AVG(Loan_Amount), 2) as avg_loan_amount,
                    ROUND(AVG(Interest_Rate), 2) as avg_interest_rate,
                    ROUND(MIN(Loan_Amount), 2) as min_loan_amount,
                    ROUND(MAX(Loan_Amount), 2) as max_loan_amount
                FROM loans
                GROUP BY Loan_Type
                ORDER BY avg_loan_amount DESC
            """
        },
        
        "Q10: Customers with Multiple Active Loans": {
            "description": "Customers with more than one active or approved loan",
            "query": """
                SELECT 
                    l.Customer_ID,
                    COUNT(*) as total_active_loans,
                    ROUND(SUM(l.Loan_Amount), 2) as total_loan_amount,
                    GROUP_CONCAT(l.Loan_Type, ', ') as loan_types
                FROM loans l
                WHERE l.Loan_Status IN ('Active', 'Approved')
                GROUP BY l.Customer_ID
                HAVING COUNT(*) > 1
                ORDER BY total_active_loans DESC
            """
        },
        
        "Q11: Top 5 Outstanding Loan Amounts": {
            "description": "Top 5 customers with highest outstanding (non-closed) loan amounts",
            "query": """
                SELECT 
                    l.Customer_ID,
                    COUNT(*) as total_loans,
                    ROUND(SUM(l.Loan_Amount), 2) as total_outstanding,
                    GROUP_CONCAT(DISTINCT l.Loan_Type, ', ') as loan_types,
                    GROUP_CONCAT(DISTINCT l.Loan_Status, ', ') as statuses
                FROM loans l
                WHERE l.Loan_Status != 'Closed'
                GROUP BY l.Customer_ID
                ORDER BY total_outstanding DESC
                LIMIT 5
            """
        },
        
        "Q12: Branch with Highest Account Balance": {
            "description": "Which branch city holds the highest total account balance?",
            "query": """
                SELECT 
                    c.city as branch_city,
                    COUNT(DISTINCT c.customer_id) as total_customers,
                    ROUND(SUM(a.account_balance), 2) as total_balance,
                    ROUND(AVG(a.account_balance), 2) as avg_balance
                FROM customers c
                JOIN accounts a ON c.customer_id = a.customer_id
                GROUP BY c.city
                ORDER BY total_balance DESC
            """
        },
        
        "Q13: Branch Performance Summary": {
            "description": "Branch performance showing customers, loans, and revenue",
            "query": """
                SELECT 
                    b.Branch_Name,
                    b.City,
                    b.Manager_Name,
                    b.Total_Employees,
                    COUNT(DISTINCT l.Customer_ID) as total_loan_customers,
                    COUNT(l.Loan_ID) as total_loans,
                    ROUND(SUM(l.Loan_Amount), 2) as total_loan_amount,
                    ROUND(b.Branch_Revenue, 2) as branch_revenue,
                    b.Performance_Rating
                FROM branches b
                LEFT JOIN loans l ON b.City = l.Branch
                GROUP BY b.Branch_Name
                ORDER BY b.Performance_Rating DESC, branch_revenue DESC
            """
        },
        
        "Q14: Support Tickets Resolution Time": {
            "description": "Issue categories with longest average resolution time",
            "query": """
                SELECT 
                    Issue_Category,
                    COUNT(*) as total_tickets,
                    COUNT(CASE WHEN Status IN ('Resolved', 'Closed') THEN 1 END) as resolved_tickets,
                    ROUND(AVG(JULIANDAY(Date_Closed) - JULIANDAY(Date_Opened)), 2) as avg_resolution_days,
                    ROUND(AVG(CAST(Customer_Rating AS REAL)), 2) as avg_customer_rating
                FROM support_tickets
                WHERE Date_Closed IS NOT NULL AND Date_Closed != ''
                GROUP BY Issue_Category
                ORDER BY avg_resolution_days DESC
            """
        },
        
        "Q15: Top Support Agents by Critical Tickets": {
            "description": "Support agents with most critical tickets resolved and high ratings",
            "query": """
                SELECT 
                    Support_Agent,
                    COUNT(*) as total_tickets_handled,
                    COUNT(CASE WHEN Priority = 'Critical' THEN 1 END) as critical_tickets,
                    COUNT(CASE WHEN Status IN ('Resolved', 'Closed') THEN 1 END) as resolved_tickets,
                    ROUND(AVG(CAST(Customer_Rating AS REAL)), 2) as avg_rating
                FROM support_tickets
                WHERE Customer_Rating != '' AND CAST(Customer_Rating AS INTEGER) >= 4
                GROUP BY Support_Agent
                HAVING critical_tickets > 0
                ORDER BY critical_tickets DESC, avg_rating DESC
                LIMIT 10
            """
        },
        
        "Q16: Potential Fraud Detection": {
            "description": "Transactions flagged as potential fraud or unusual patterns",
            "query": """
                SELECT 
                    t.txn_id,
                    t.customer_id,
                    c.name,
                    t.txn_type,
                    ROUND(t.amount, 2) as amount,
                    t.txn_time,
                    t.status,
                    CASE 
                        WHEN t.txn_type = 'online fraud' THEN 'Flagged as Fraud'
                        WHEN t.amount > 200000 THEN 'High Value Transaction'
                        WHEN t.status = 'failed' AND t.amount > 100000 THEN 'Failed High Value'
                        ELSE 'Normal'
                    END as risk_flag
                FROM transactions t
                JOIN customers c ON t.customer_id = c.customer_id
                WHERE t.txn_type = 'online fraud' 
                   OR t.amount > 200000 
                   OR (t.status = 'failed' AND t.amount > 100000)
                ORDER BY t.amount DESC
            """
        },
        
        "Q17: Credit Card Utilization Analysis": {
            "description": "Credit card utilization rates and potential over-limit cards",
            "query": """
                SELECT 
                    cc.Card_ID,
                    cc.Customer_ID,
                    cc.Card_Type,
                    cc.Card_Network,
                    ROUND(cc.Credit_Limit, 2) as credit_limit,
                    ROUND(cc.Current_Balance, 2) as current_balance,
                    ROUND((cc.Current_Balance * 100.0 / cc.Credit_Limit), 2) as utilization_percentage,
                    cc.Status,
                    CASE 
                        WHEN (cc.Current_Balance * 100.0 / cc.Credit_Limit) > 90 THEN 'Critical'
                        WHEN (cc.Current_Balance * 100.0 / cc.Credit_Limit) > 70 THEN 'High'
                        WHEN (cc.Current_Balance * 100.0 / cc.Credit_Limit) > 50 THEN 'Medium'
                        ELSE 'Low'
                    END as risk_level
                FROM credit_cards cc
                WHERE cc.Status = 'Active'
                ORDER BY utilization_percentage DESC
                LIMIT 20
            """
        }
    }
    
    return queries

def execute_query(conn, query_key):
    """
    Execute a specific query and return results as DataFrame.
    """
    import pandas as pd
    
    queries = get_all_queries()
    
    if query_key in queries:
        query_info = queries[query_key]
        df = pd.read_sql_query(query_info["query"], conn)
        return df, query_info["description"], query_info["query"]
    else:
        return None, None, None

if __name__ == "__main__":
    import sqlite3
    
    # Test queries
    conn = sqlite3.connect('database/banking.db')
    queries = get_all_queries()
    
    print("Testing all queries...\n")
    for key, query_info in queries.items():
        print(f"Executing: {key}")
        try:
            df = pd.read_sql_query(query_info["query"], conn)
            print(f"✓ Success - Returned {len(df)} rows\n")
        except Exception as e:
            print(f"✗ Error: {e}\n")
    
    conn.close()
