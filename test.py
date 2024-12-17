import streamlit as st
import pandas as pd

conn = st.connection("snowflake")

print(conn.query('select * from analytics_data', ttl=0))