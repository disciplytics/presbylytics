import streamlit as st
import pandas as pd
from utils.utils import snowflake_connection
# title
st.title('PCA Statistics :church:', help = 'All data is from [The PCA](https://presbyteryportal.pcanet.org/Report/StatsReport)')

# connect and load from snowflake
df = snowflake_connection('select * from analytics_data')
df.columns = [i.strip("'") for i in df.columns]

# create filters




st.scatter_chart(df, x ='Income,Gini Index Of Income Inequality,Gini Index,Estimate', y = "TOTAL_CONTRIB", color = "STAT_YEAR")
#st.scatter_chart(df, x ='Housing Characteristics,Average Household Size Of Occupied Housing Units By Tenure,Average household size,Estimate', y = "TOTAL_CONTRIB", color = "STAT_YEAR")
#st.scatter_chart(df, x ='Housing Characteristics,Median Selected Monthly Owner Costs As A Percentage Of Household Income In The Past 12 Months,Median selected monthly owner costs as a percentage of household income in the past 12 months,Estimate', y = "TOTAL_CONTRIB", color = "STAT_YEAR")

st.scatter_chart(df, x ='Income,Gini Index Of Income Inequality,Gini Index,Estimate', y = "BENEVOL_GRAND_TOTAL", color = "STAT_YEAR")
