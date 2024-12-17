import streamlit as st
import pandas as pd
from utils.utils import snowflake_connection
from analysis.member_analysis import member_analysis

# title
st.title('PCA Statistics :church:', help = 'All data is from [The PCA](https://presbyteryportal.pcanet.org/Report/StatsReport)')

with st.expander("Click to Learn More"):
        st.write("This app displays the Presbyterian Church in America statistics in an interactive frontend for enhanced analysis.")

# connect and load from snowflake
df = snowflake_connection('select * from analytics_data')

# clean up columns
df.columns = [i.strip("'").replace("_", " ").title() for i in df.columns]

st.write(df.columns)

df['Stat Year'] = df['Stat Year'].astype(str)

# create filters
st.sidebar.subheader("Filtering Options")
year_sel = st.sidebar.multiselect(
    'Select a Stat Year:', 
    pd.Series(pd.unique(df['Stat Year'])).sort_values(),
    pd.Series(pd.unique(df['Stat Year'])).sort_values()
  )

city_sel = st.sidebar.multiselect(
    'Select Church City:', 
    pd.Series(pd.unique(df['City'])).sort_values(),
    pd.Series(pd.unique(df['City'])).sort_values()
  )

state_sel = st.sidebar.multiselect(
    'Select Church State:', 
    pd.Series(pd.unique(df['State'])).sort_values(),
    pd.Series(pd.unique(df['State'])).sort_values()
  )

church_sel = st.sidebar.multiselect(
    'Select Church Name:',
    pd.Series(pd.unique(df['Church'])).sort_values(),
    pd.Series(pd.unique(df['Church'])).sort_values()
  )


filtered_df = df[
        (df['Stat Year'].isin(year_sel)) & 
        (df['City'].isin(city_sel)) &
        (df['State'].isin(state_sel)) &
        (df['Church'].isin(church_sel))
      ]

tab_list = ['Member Data', 'General Data', 'Contributions Data', 'Benevol. Disbur. Data', 'Conregation Ops.']
member_tab, general_tab, contrib_tab, benevol_tab, cong_ops_tab = st.tabs(tab_list)
# MEMBERS
with member_tab:
        member_analysis(filtered_df)
        #st.subheader('Member Count Trends')
        #st.bar_chart(
        #  filtered_df.groupby(['Stat Year'])[['Comm', 'Non Comm']].sum(),
        #  y = ['Comm', 'Non Comm']
        #)
#st.scatter_chart(filtered_df, x ='Income,Gini Index Of Income Inequality,Gini Index,Estimate', y = "TOTAL_CONTRIB", color = "STAT_YEAR")
#st.scatter_chart(df, x ='Housing Characteristics,Average Household Size Of Occupied Housing Units By Tenure,Average household size,Estimate', y = "TOTAL_CONTRIB", color = "STAT_YEAR")
#st.scatter_chart(df, x ='Housing Characteristics,Median Selected Monthly Owner Costs As A Percentage Of Household Income In The Past 12 Months,Median selected monthly owner costs as a percentage of household income in the past 12 months,Estimate', y = "TOTAL_CONTRIB", color = "STAT_YEAR")

#st.scatter_chart(df, x ='Income,Gini Index Of Income Inequality,Gini Index,Estimate', y = "BENEVOL_GRAND_TOTAL", color = "STAT_YEAR")
