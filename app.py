import streamlit as st
import pandas as pd
from utils.utils import snowflake_connection

# title
st.title('PCA Statistics :church:', help = 'All data is from [The PCA](https://presbyteryportal.pcanet.org/Report/StatsReport)')

# connect and load from snowflake
df = snowflake_connection('select * from analytics_data')

# clean up columns
df.columns = [i.strip("'") for i in df.columns]
df['STAT_YEAR'] = df['STAT_YEAR'].astype(str)

# create filters
st.sidebar.subheader("Filtering Options")
year_sel = st.sidebar.multiselect(
    'Select a Stat Year:', 
    pd.Series(pd.unique(df['STAT_YEAR'])).sort_values(),
    pd.Series(pd.unique(df['STAT_YEAR'])).sort_values()
  )

city_sel = st.sidebar.multiselect(
    'Select Church City:', 
    pd.Series(pd.unique(df['CITY'])).sort_values(),
    pd.Series(pd.unique(df['CITY'])).sort_values()
  )

state_sel = st.sidebar.multiselect(
    'Select Church State:', 
    pd.Series(pd.unique(df['STATE'])).sort_values(),
    pd.Series(pd.unique(df['STATE'])).sort_values()
  )

church_sel = st.sidebar.multiselect(
    'Select Church Name:',
    pd.Series(pd.unique(df['CHURCH'])).sort_values(),
    pd.Series(pd.unique(df['CHURCH'])).sort_values()
  )


filtered_df = df[
        (df['STAT_YEAR'].isin(year_sel)) & 
        (df['CITY'].isin(city_sel)) &
        (df['STATE'].isin(state_sel)) &
        (df['CHURCH'].isin(church_sel))
      ]

st.line_chart(
  filtered_df,
  x = 'STAT_YEAR',
  y = ['COMM', 'NON_COMM']
)
#st.scatter_chart(filtered_df, x ='Income,Gini Index Of Income Inequality,Gini Index,Estimate', y = "TOTAL_CONTRIB", color = "STAT_YEAR")
#st.scatter_chart(df, x ='Housing Characteristics,Average Household Size Of Occupied Housing Units By Tenure,Average household size,Estimate', y = "TOTAL_CONTRIB", color = "STAT_YEAR")
#st.scatter_chart(df, x ='Housing Characteristics,Median Selected Monthly Owner Costs As A Percentage Of Household Income In The Past 12 Months,Median selected monthly owner costs as a percentage of household income in the past 12 months,Estimate', y = "TOTAL_CONTRIB", color = "STAT_YEAR")

#st.scatter_chart(df, x ='Income,Gini Index Of Income Inequality,Gini Index,Estimate', y = "BENEVOL_GRAND_TOTAL", color = "STAT_YEAR")
