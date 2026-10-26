import streamlit as st
import pandas as pd
import mysql.connector
import plotly.express as px

st.set_page_config(page_title="Sales Analysis Dashboard - Fariya's Project", layout="wide")
st.title("📊 Sales Analysis Dashboard - Fariya's Project")

# Try MySQL, if fails use Sample Data (for Cloud)
try:
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="sales_analysis"
    )
    query = "SELECT * FROM orders JOIN customers ON orders.customer_id = customers.customer_id JOIN products ON orders.product_id = products.product_id"
    df = pd.read_sql(query, conn)
    conn.close()
    st.success("Connected to MySQL - Live Data")
except Exception as e:
    st.warning("Cloud Demo Mode: Showing sample data (MySQL is local only)")
    # Sample data for cloud demo
    data = {
        'order_date': pd.date_range('2024-01-01', periods=100, freq='D'),
        'amount': [2000, 3500, 1500, 4000, 2800]*20,
        'category': ['Electronics', 'Clothing', 'Books', 'Electronics', 'Clothing']*20,
        'customer_name': ['Fariya', 'Ali', 'Sara']*33 + ['Fariya'],
        'product_name': ['Laptop', 'Shirt', 'Novel', 'Mobile', 'Jeans']*20
    }
    df = pd.DataFrame(data)

# Dashboard
col1, col2, col3 = st.columns(3)
col1.metric("Total Sales", f"₹{df['amount'].sum():,}")
col2.metric("Total Orders", len(df))
col3.metric("Avg Order", f"₹{df['amount'].mean():.0f}")

fig1 = px.line(df.groupby('order_date')['amount'].sum().reset_index(), x='order_date', y='amount', title="Sales Over Time")
st.plotly_chart(fig1, use_container_width=True)

fig2 = px.bar(df.groupby('category')['amount'].sum().reset_index(), x='category', y='amount', title="Sales by Category")
st.plotly_chart(fig2, use_container_width=True)

st.dataframe(df.head(20))
st.caption("Tech Stack: MySQL + Python + Streamlit | By Fariya2026")