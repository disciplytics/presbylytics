import streamlit as st
import pandas as pd

conn = st.connection("snowflake")

df = conn.query('select * from analytics_data', ttl=0)

st.scatter_chart(df, x ="'Income,Gini Index Of Income Inequality,Gini Index,Estimate'", y = "TOTAL_CHURCH_INCOME")
