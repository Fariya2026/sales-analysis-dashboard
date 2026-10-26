import mysql.connector
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(page_title="Fariya Sales Dashboard", layout="wide")
st.title("📊 Sales Analysis Dashboard - Fariya's Project")

# No password needed
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="fariya123",
    database="sales_analysis"
)

# Queries
q1 = pd.read_sql("""
    SELECT c.city, SUM(p.price*o.quantity) as total_sales 
    FROM orders o 
    JOIN customers c ON o.customer_id=c.customer_id 
    JOIN products p ON o.product_id=p.product_id 
    GROUP BY c.city ORDER BY total_sales DESC
""", conn)

q2 = pd.read_sql("""
    SELECT p.category, SUM(p.price*o.quantity) as total_sales 
    FROM orders o JOIN products p ON o.product_id=p.product_id 
    GROUP BY p.category
""", conn)

q3 = pd.read_sql("""
    SELECT MONTH(order_date) as month, SUM(p.price*o.quantity) as total_sales 
    FROM orders o JOIN products p ON o.product_id=p.product_id 
    GROUP BY MONTH(order_date) ORDER BY month
""", conn)

# Display
col1, col2 = st.columns(2)

with col1:
    st.subheader("Sales by City (Your Q1)")
    st.bar_chart(q1.set_index('city'))
    st.dataframe(q1)

with col2:
    st.subheader("Sales by Category (Your Q2)")
    st.bar_chart(q2.set_index('category'))
    st.dataframe(q2)

st.subheader("Monthly Sales Trend (Your Q3)")
st.line_chart(q3.set_index('month'))
st.dataframe(q3)

st.success("Database: sales_analysis | Tables: customers, products, orders")