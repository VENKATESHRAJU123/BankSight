import sys
import streamlit as st
import pandas as pd
import sqlite3
import json
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go
sys.path.append('Scripts')
from Scripts.sql_queries import get_all_queries, execute_query

# Page configuration
st.set_page_config(
    page_title="BankSight: Transaction Intelligence Dashboard",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        padding: 1rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #ff7f0e;
        margin-top: 1rem;
        margin-bottom: 1rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .stButton>button {
        width: 100%;
        background-color: #1f77b4;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# Database connection
@st.cache_resource
def get_database_connection():
    """Create and return database connection."""
    return sqlite3.connect('database/banking.db', check_same_thread=False)

conn = get_database_connection()

# Sidebar navigation
st.sidebar.title("🏦 BankSight Navigation")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Choose a page:",
    ["🏠 Introduction", "📊 View Tables", "🔍 Filter Data", 
     "✏️ CRUD Operations", "💰 Credit/Debit Simulation", 
     "🧠 Analytical Insights", "👩‍💻 About Creator"]
)

st.sidebar.markdown("---")
st.sidebar.info("**BankSight v1.0**\n\nA comprehensive banking analytics platform")

# ===================== PAGE 1: INTRODUCTION =====================
if page == "🏠 Introduction":
    st.markdown('<p class="main-header">🏦 BankSight: Transaction Intelligence Dashboard</p>', unsafe_allow_html=True)
    
    st.markdown("""
    ## Welcome to BankSight
    
    BankSight is a comprehensive banking analytics platform designed to provide deep insights into:
    - Customer demographics and behavior
    - Transaction patterns and trends
    - Loan portfolio analysis
    - Credit card utilization
    - Support ticket management
    - Branch performance metrics
    
    ### 🎯 Project Objectives
    
    1. **Customer Analytics**: Profile customer transaction behavior to tailor banking products
    2. **Fraud Detection**: Identify high-risk transactions and accounts for fraud prevention
    3. **Performance Evaluation**: Assess branch performance based on transactions and accounts
    4. **Interactive Queries**: Enable customers and bank officials to query transaction histories
    
    ### 📁 Datasets Used
    
    This system integrates **7 comprehensive datasets**:
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **Core Banking Data:**
        - 👥 **Customers** - Demographics and account info
        - 💰 **Accounts** - Balance and transaction history
        - 💸 **Transactions** - Detailed transaction logs
        - 🏢 **Branches** - Branch locations and performance
        """)
    
    with col2:
        st.markdown("""
        **Financial Products:**
        - 📋 **Loans** - Loan details and repayment status
        - 💳 **Credit Cards** - Card info and utilization
        - 🎫 **Support Tickets** - Customer service interactions
        """)
    
    st.markdown("---")
    
    # Display key metrics
    st.markdown("### 📊 System Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_customers = pd.read_sql_query("SELECT COUNT(*) as count FROM customers", conn).iloc[0]['count']
        st.metric("Total Customers", f"{total_customers:,}")
    
    with col2:
        total_transactions = pd.read_sql_query("SELECT COUNT(*) as count FROM transactions", conn).iloc[0]['count']
        st.metric("Total Transactions", f"{total_transactions:,}")
    
    with col3:
        total_loans = pd.read_sql_query("SELECT COUNT(*) as count FROM loans", conn).iloc[0]['count']
        st.metric("Total Loans", f"{total_loans:,}")
    
    with col4:
        total_branches = pd.read_sql_query("SELECT COUNT(*) as count FROM branches", conn).iloc[0]['count']
        st.metric("Total Branches", f"{total_branches:,}")
    
    st.markdown("---")
    
    st.markdown("""
    ### 🚀 Features
    
    - **View Tables**: Browse all datasets directly from the database
    - **Filter Data**: Apply multi-column filters to any dataset
    - **CRUD Operations**: Create, Read, Update, and Delete records
    - **Credit/Debit Simulation**: Simulate banking transactions with balance validation
    - **Analytical Insights**: Execute 17+ pre-built analytical queries
    
    ---
    
    ### 🛠️ Technical Stack
    
    - **Frontend**: Streamlit
    - **Database**: SQLite3
    - **Data Processing**: Pandas, NumPy
    - **Visualization**: Plotly
    - **Language**: Python 3.8+
    """)

# ===================== PAGE 2: VIEW TABLES =====================
elif page == "📊 View Tables":
    st.markdown('<p class="main-header">📊 View Database Tables</p>', unsafe_allow_html=True)
    
    tables = {
        "Customers": "customers",
        "Accounts": "accounts",
        "Transactions": "transactions",
        "Branches": "branches",
        "Loans": "loans",
        "Credit Cards": "credit_cards",
        "Support Tickets": "support_tickets"
    }
    
    selected_table = st.selectbox("Select a table to view:", list(tables.keys()))
    
    if selected_table:
        table_name = tables[selected_table]
        
        # Get record count
        count_query = f"SELECT COUNT(*) as count FROM {table_name}"
        record_count = pd.read_sql_query(count_query, conn).iloc[0]['count']
        
        st.info(f"**Total Records**: {record_count:,}")
        
        # Pagination
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col1:
            page_size = st.selectbox("Records per page:", [10, 25, 50, 100], index=1)
        
        with col2:
            total_pages = (record_count + page_size - 1) // page_size
            current_page = st.number_input("Page:", min_value=1, max_value=total_pages, value=1)
        
        offset = (current_page - 1) * page_size
        
        # Fetch data
        query = f"SELECT * FROM {table_name} LIMIT {page_size} OFFSET {offset}"
        df = pd.read_sql_query(query, conn)
        
        st.dataframe(df, use_container_width=True, height=500)
        
        # Download button
        csv = df.to_csv(index=False)
        st.download_button(
            label="📥 Download as CSV",
            data=csv,
            file_name=f"{table_name}.csv",
            mime="text/csv"
        )

# ===================== PAGE 3: FILTER DATA =====================
elif page == "🔍 Filter Data":
    st.markdown('<p class="main-header">🔍 Filter Data</p>', unsafe_allow_html=True)
    
    tables = {
        "Customers": "customers",
        "Accounts": "accounts",
        "Transactions": "transactions",
        "Branches": "branches",
        "Loans": "loans",
        "Credit Cards": "credit_cards",
        "Support Tickets": "support_tickets"
    }
    
    selected_table = st.selectbox("Select a table:", list(tables.keys()))
    table_name = tables[selected_table]
    
    # Get columns
    cursor = conn.cursor()
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns_info = cursor.fetchall()
    column_names = [col[1] for col in columns_info]
    
    st.markdown("### Apply Filters")
    
    # Multi-select for columns to filter
    filter_columns = st.multiselect("Select columns to filter:", column_names)
    
    filters = {}
    
    if filter_columns:
        for col in filter_columns:
            st.markdown(f"**Filter: {col}**")
            
            # Get unique values for the column
            unique_query = f"SELECT DISTINCT {col} FROM {table_name} WHERE {col} IS NOT NULL LIMIT 100"
            unique_values = pd.read_sql_query(unique_query, conn)[col].tolist()
            
            if len(unique_values) <= 20:
                # Use multiselect for small number of unique values
                selected_values = st.multiselect(f"Select {col} values:", unique_values)
                if selected_values:
                    filters[col] = selected_values
            else:
                # Use text input for large number of unique values
                filter_text = st.text_input(f"Enter {col} value (supports wildcards %):")
                if filter_text:
                    filters[col] = filter_text
    
    if st.button("Apply Filters"):
        # Build query with filters
        query = f"SELECT * FROM {table_name}"
        
        if filters:
            where_clauses = []
            for col, value in filters.items():
                if isinstance(value, list):
                    # Multiple values - use IN clause
                    value_str = "', '".join(str(v) for v in value)
                    where_clauses.append(f"{col} IN ('{value_str}')")
                else:
                    # Single value - use LIKE for text search
                    where_clauses.append(f"{col} LIKE '{value}'")
            
            if where_clauses:
                query += " WHERE " + " AND ".join(where_clauses)
        
        # Execute query
        try:
            df = pd.read_sql_query(query, conn)
            
            st.success(f"Found {len(df)} records")
            st.dataframe(df, use_container_width=True)
            
            # Download button
            csv = df.to_csv(index=False)
            st.download_button(
                label="📥 Download Filtered Data",
                data=csv,
                file_name=f"filtered_{table_name}.csv",
                mime="text/csv"
            )
        except Exception as e:
            st.error(f"Error executing query: {e}")

# ===================== PAGE 4: CRUD OPERATIONS =====================
elif page == "✏️ CRUD Operations":
    st.markdown('<p class="main-header">✏️ CRUD Operations</p>', unsafe_allow_html=True)
    
    tables = {
        "Customers": "customers",
        "Accounts": "accounts",
        "Transactions": "transactions",
        "Support Tickets": "support_tickets"
    }
    
    operation = st.radio("Select Operation:", ["Create", "Read", "Update", "Delete"])
    
    selected_table = st.selectbox("Select Table:", list(tables.keys()))
    table_name = tables[selected_table]
    
    # Get columns
    cursor = conn.cursor()
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns_info = cursor.fetchall()
    column_names = [col[1] for col in columns_info]
    
    st.markdown("---")
    
    # CREATE OPERATION
    if operation == "Create":
        st.markdown("### ➕ Create New Record")
        
        with st.form("create_form"):
            new_record = {}
            
            for col in column_names:
                new_record[col] = st.text_input(f"{col}:")
            
            submitted = st.form_submit_button("Create Record")
            
            if submitted:
                try:
                    cols = ", ".join(column_names)
                    placeholders = ", ".join(["?" for _ in column_names])
                    values = [new_record[col] for col in column_names]
                    
                    insert_query = f"INSERT INTO {table_name} ({cols}) VALUES ({placeholders})"
                    cursor.execute(insert_query, values)
                    conn.commit()
                    
                    st.success("✅ Record created successfully!")
                except Exception as e:
                    st.error(f"❌ Error: {e}")
    
    # READ OPERATION
    elif operation == "Read":
        st.markdown("### 🔍 Read Records")
        
        search_col = st.selectbox("Search by column:", column_names)
        search_value = st.text_input(f"Enter {search_col} value:")
        
        if st.button("Search"):
            try:
                query = f"SELECT * FROM {table_name} WHERE {search_col} LIKE '%{search_value}%'"
                df = pd.read_sql_query(query, conn)
                
                st.dataframe(df, use_container_width=True)
            except Exception as e:
                st.error(f"❌ Error: {e}")
    
    # UPDATE OPERATION
    elif operation == "Update":
        st.markdown("### ✏️ Update Record")
        
        primary_key = column_names[0]  # Assume first column is primary key
        
        record_id = st.text_input(f"Enter {primary_key} to update:")
        
        if record_id:
            # Fetch existing record
            query = f"SELECT * FROM {table_name} WHERE {primary_key} = '{record_id}'"
            existing_df = pd.read_sql_query(query, conn)
            
            if len(existing_df) > 0:
                st.info("Current values:")
                st.dataframe(existing_df)
                
                with st.form("update_form"):
                    updated_record = {}
                    
                    for col in column_names[1:]:  # Skip primary key
                        current_value = str(existing_df.iloc[0][col])
                        updated_record[col] = st.text_input(f"{col}:", value=current_value)
                    
                    submitted = st.form_submit_button("Update Record")
                    
                    if submitted:
                        try:
                            set_clause = ", ".join([f"{col} = ?" for col in column_names[1:]])
                            values = [updated_record[col] for col in column_names[1:]]
                            values.append(record_id)
                            
                            update_query = f"UPDATE {table_name} SET {set_clause} WHERE {primary_key} = ?"
                            cursor.execute(update_query, values)
                            conn.commit()
                            
                            st.success("✅ Record updated successfully!")
                        except Exception as e:
                            st.error(f"❌ Error: {e}")
            else:
                st.warning("No record found with that ID")
    
    # DELETE OPERATION
    elif operation == "Delete":
        st.markdown("### 🗑️ Delete Record")
        
        primary_key = column_names[0]
        
        record_id = st.text_input(f"Enter {primary_key} to delete:")
        
        if record_id:
            # Show record to be deleted
            query = f"SELECT * FROM {table_name} WHERE {primary_key} = '{record_id}'"
            df = pd.read_sql_query(query, conn)
            
            if len(df) > 0:
                st.warning("⚠️ You are about to delete this record:")
                st.dataframe(df)
                
                if st.button("🗑️ Confirm Delete", type="primary"):
                    try:
                        delete_query = f"DELETE FROM {table_name} WHERE {primary_key} = ?"
                        cursor.execute(delete_query, (record_id,))
                        conn.commit()
                        
                        st.success("✅ Record deleted successfully!")
                    except Exception as e:
                        st.error(f"❌ Error: {e}")
            else:
                st.info("No record found with that ID")

# ===================== PAGE 5: CREDIT/DEBIT SIMULATION =====================
elif page == "💰 Credit/Debit Simulation":
    st.markdown('<p class="main-header">💰 Credit/Debit Simulation</p>', unsafe_allow_html=True)
    
    st.markdown("""
    This module simulates real banking operations with the following rules:
    - Minimum balance requirement: ₹1,000
    - All transactions are logged in real-time
    - Balance is updated immediately in the database
    """)
    
    st.markdown("---")
    
    # Account selection
    account_id = st.text_input("Enter Customer ID (e.g., CUST00001):")
    
    if account_id:
        # Fetch account details
        query = f"""
        SELECT c.customer_id, c.name, c.city, a.account_balance
        FROM customers c
        JOIN accounts a ON c.customer_id = a.customer_id
        WHERE c.customer_id = '{account_id}'
        """
        
        account_df = pd.read_sql_query(query, conn)
        
        if len(account_df) > 0:
            current_balance = account_df.iloc[0]['account_balance']
            customer_name = account_df.iloc[0]['name']
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.success(f"**Customer**: {customer_name}")
            
            with col2:
                st.success(f"**Current Balance**: ₹{current_balance:,.2f}")
            
            st.markdown("---")
            
            # Transaction type
            transaction_type = st.radio("Select Transaction Type:", ["Deposit", "Withdraw"])
            
            amount = st.number_input("Enter Amount (₹):", min_value=0.01, step=100.0)
            
            if st.button("Process Transaction", type="primary"):
                if transaction_type == "Deposit":
                    new_balance = current_balance + amount
                    txn_type = "deposit"
                    
                    # Update balance
                    update_query = f"UPDATE accounts SET account_balance = {new_balance}, last_updated = '{datetime.now()}' WHERE customer_id = '{account_id}'"
                    cursor = conn.cursor()
                    cursor.execute(update_query)
                    conn.commit()
                    
                    st.success(f"✅ Deposit of ₹{amount:,.2f} successful!")
                    st.info(f"New Balance: ₹{new_balance:,.2f}")
                    
                else:  # Withdraw
                    if current_balance - amount >= 1000:
                        new_balance = current_balance - amount
                        txn_type = "withdrawal"
                        
                        # Update balance
                        update_query = f"UPDATE accounts SET account_balance = {new_balance}, last_updated = '{datetime.now()}' WHERE customer_id = '{account_id}'"
                        cursor = conn.cursor()
                        cursor.execute(update_query)
                        conn.commit()
                        
                        st.success(f"✅ Withdrawal of ₹{amount:,.2f} successful!")
                        st.info(f"New Balance: ₹{new_balance:,.2f}")
                    else:
                        st.error("❌ Insufficient balance! Minimum balance of ₹1,000 must be maintained.")
                        st.warning(f"Available for withdrawal: ₹{max(0, current_balance - 1000):,.2f}")
        else:
            st.error("❌ Customer ID not found!")

# ===================== PAGE 6: ANALYTICAL INSIGHTS =====================
elif page == "🧠 Analytical Insights":
    st.markdown('<p class="main-header">🧠 Analytical Insights</p>', unsafe_allow_html=True)
    
    queries = get_all_queries()
    
    query_options = list(queries.keys())
    
    selected_query = st.selectbox("Select an analytical query:", query_options)
    
    if selected_query:
        query_info = queries[selected_query]
        
        st.markdown(f"### {selected_query}")
        st.info(f"**Description**: {query_info['description']}")
        
        # Show SQL query
        with st.expander("📝 View SQL Query"):
            st.code(query_info['query'], language='sql')
        
        if st.button("🚀 Execute Query"):
            try:
                df = pd.read_sql_query(query_info['query'], conn)
                
                st.success(f"✅ Query executed successfully! Returned {len(df)} rows.")
                
                # Display results
                st.dataframe(df, use_container_width=True)
                
                # Visualization (if applicable)
                if len(df) > 0 and len(df.columns) >= 2:
                    st.markdown("### 📊 Visualization")
                    
                    # Determine chart type based on data
                    numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns.tolist()
                    
                    if len(numeric_cols) >= 1:
                        chart_type = st.selectbox("Select Chart Type:", ["Bar Chart", "Line Chart", "Pie Chart"])
                        
                        if chart_type == "Bar Chart":
                            fig = px.bar(df.head(10), x=df.columns[0], y=numeric_cols[0], 
                                        title=f"{selected_query} - Bar Chart")
                            st.plotly_chart(fig, use_container_width=True)
                        
                        elif chart_type == "Line Chart":
                            fig = px.line(df.head(10), x=df.columns[0], y=numeric_cols[0],
                                         title=f"{selected_query} - Line Chart")
                            st.plotly_chart(fig, use_container_width=True)
                        
                        elif chart_type == "Pie Chart" and len(df) <= 10:
                            fig = px.pie(df, names=df.columns[0], values=numeric_cols[0],
                                        title=f"{selected_query} - Pie Chart")
                            st.plotly_chart(fig, use_container_width=True)
                
                # Download button
                csv = df.to_csv(index=False)
                st.download_button(
                    label="📥 Download Results as CSV",
                    data=csv,
                    file_name=f"{selected_query.replace(' ', '_')}.csv",
                    mime="text/csv"
                )
                
            except Exception as e:
                st.error(f"❌ Error executing query: {e}")

# ===================== PAGE 7: ABOUT CREATOR =====================
elif page == "👩‍💻 About Creator":
    st.markdown('<p class="main-header">👩‍💻 About the Creator</p>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        # Placeholder for profile image
        st.image("https://via.placeholder.com/300x300.png?text=Your+Photo", width=250)
    
    with col2:
        st.markdown("""
        ## [Your Name]
        ### Banking Analytics & Data Science Professional
        
        ---
        
        **Expertise:**
        - Banking & Financial Analytics
        - Data Engineering
        - SQL & Database Design
        - Python Development
        - Streamlit Applications
        - Machine Learning & AI
        
        ---
        
        **Contact Information:**
        - 📧 Email: your.email@example.com
        - 💼 LinkedIn: linkedin.com/in/yourprofile
        - 🐱 GitHub: github.com/yourusername
        - 🌐 Portfolio: yourwebsite.com
        
        ---
        
        **About This Project:**
        
        BankSight was developed as a comprehensive banking analytics platform to demonstrate:
        - Full-stack data application development
        - Database design and SQL query optimization
        - Interactive data visualization
        - Real-world banking operations simulation
        - CRUD operations and data management
        
        The project integrates 7 datasets with 17+ analytical queries to provide actionable insights
        for banking operations, fraud detection, and customer behavior analysis.
        """)
    
    st.markdown("---")
    
    st.markdown("""
    ### 🏆 Project Achievements
    
    - ✅ Integrated 7 comprehensive banking datasets
    - ✅ Implemented 17+ analytical SQL queries
    - ✅ Built full CRUD functionality for all tables
    - ✅ Created interactive filtering system
    - ✅ Developed credit/debit transaction simulator
    - ✅ Designed responsive UI with Streamlit
    - ✅ Implemented data visualization with Plotly
    
    ---
    
    ### 🙏 Acknowledgments
    
    Special thanks to all the open-source libraries and frameworks that made this project possible:
    - Streamlit
    - Pandas
    - SQLite
    - Plotly
    - Python Community
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p>BankSight: Transaction Intelligence Dashboard v1.0</p>
    <p>Developed with ❤️ using Streamlit & Python</p>
</div>
""", unsafe_allow_html=True)
