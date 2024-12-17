import streamlit as st
import pandas as pd
from utils.utils import snowflake_connection

# title
st.title('PCA Statistics :church:', help = 'All data is from [The PCA](https://presbyteryportal.pcanet.org/Report/StatsReport)')

# connect and load from snowflake
df = snowflake_connection('select * from analytics_data')

# clean up columns
df.columns = [i.strip("'") for i in df.columns]

st.write(df)

# create filters
year_filter_col, city_filter_col, state_filter_col, church_filter_col = st.columns(4)

with year_filter_col:
  year_sel = st.multiselect(
    'Stat Year', df['STAT_YEAR'].unique().sort(), df['STAT_YEAR'].unique().sort()
  )

with city_filter_col:
  city_sel = st.multiselect(
    'City', df['CITY'].unique().sort(), df['CITY'].unique().sort()
  )

with state_filter_col:
  state_sel = st.multiselect(
    'State', df['STATE'].unique().sort(), df['STATE'].unique().sort()
  )

with church_filter_col:
  church_sel = st.multiselect(
    'Church Name', df['CHURCH'].unique().sort(), df['CHURCH'].unique().sort()
  )


filtered_df = df[
        (df['STAT_YEAR'].isin(year_sel)) & 
        (df['CITY'].isin(city_sel)) &
        (df['STATE'].isin(state_sel)) &
        (df['CHURCH'].isin(church_sel))
      ]

st.scatter_chart(filtered_df, x ='Income,Gini Index Of Income Inequality,Gini Index,Estimate', y = "TOTAL_CONTRIB", color = "STAT_YEAR")
#st.scatter_chart(df, x ='Housing Characteristics,Average Household Size Of Occupied Housing Units By Tenure,Average household size,Estimate', y = "TOTAL_CONTRIB", color = "STAT_YEAR")
#st.scatter_chart(df, x ='Housing Characteristics,Median Selected Monthly Owner Costs As A Percentage Of Household Income In The Past 12 Months,Median selected monthly owner costs as a percentage of household income in the past 12 months,Estimate', y = "TOTAL_CONTRIB", color = "STAT_YEAR")

#st.scatter_chart(df, x ='Income,Gini Index Of Income Inequality,Gini Index,Estimate', y = "BENEVOL_GRAND_TOTAL", color = "STAT_YEAR")
