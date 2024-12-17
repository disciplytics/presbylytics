import streamlit as st
import pandas as pd
from utils.utils import snowflake_connection

# title
st.title('PCA Statistics :church:', help = 'All data is from [The PCA](https://presbyteryportal.pcanet.org/Report/StatsReport)')

# connect and load from snowflake
df = snowflake_connection('select * from analytics_data')

# clean up columns
df.columns = [i.strip("'") for i in df.columns]

# create filters
year_filter_col, city_filter_col, state_filter_col, church_filter_col = st.columns(4)

year_sel = year_filter_col.multiselect(
  'Stat Year', df['STAT_YEAR'].unique().sort(), df['STAT_YEAR'].unique().sort()
)

city_sel = city_filter_col.multiselect(
  'City', df['CITY'].unique().sort(), df['CITY'].unique().sort()
)

state_sel = state_filter_col.multiselect(
  'State', df['STATE'].unique().sort(), df['STATE'].unique().sort()
)

church_sel = church_filter_col.multiselect(
  'Church Name', df['CHURCH'].unique().sort(), df['CHURCH'].unique().sort()
)




st.scatter_chart(df, x ='Income,Gini Index Of Income Inequality,Gini Index,Estimate', y = "TOTAL_CONTRIB", color = "STAT_YEAR")
#st.scatter_chart(df, x ='Housing Characteristics,Average Household Size Of Occupied Housing Units By Tenure,Average household size,Estimate', y = "TOTAL_CONTRIB", color = "STAT_YEAR")
#st.scatter_chart(df, x ='Housing Characteristics,Median Selected Monthly Owner Costs As A Percentage Of Household Income In The Past 12 Months,Median selected monthly owner costs as a percentage of household income in the past 12 months,Estimate', y = "TOTAL_CONTRIB", color = "STAT_YEAR")

st.scatter_chart(df, x ='Income,Gini Index Of Income Inequality,Gini Index,Estimate', y = "BENEVOL_GRAND_TOTAL", color = "STAT_YEAR")
