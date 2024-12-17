import streamlit as st
import pandas as pd
from utils.utils import snowflake_connection
from analysis.member_analysis import member_analysis
from analysis.general_analysis import general_analysis
from analysis.contributions_analysis import contributions_analysis
from analysis.benevol_disburs_analysis import benevol_disburs_analysis

# title
st.title('PCA Statistics :church:', help = 'All data is from [The PCA](https://presbyteryportal.pcanet.org/Report/StatsReport)')

with st.expander("Click to Learn More"):
        st.write("This app displays the Presbyterian Church in America statistics in an interactive frontend for enhanced analysis.")

# connect and load from snowflake
df = snowflake_connection('select * from analytics_data')

# clean up columns
df.columns = [i.strip("'").replace("_", " ").title() for i in df.columns]

df['Stat Year'] = df['Stat Year'].astype(str)

st.write(df.columns)
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

tab_list = ['Member Data', 'General Data', 'Contributions Data', 'Benevolent Disbursements Data', 'Conregation Ops']
member_tab, general_tab, contrib_tab, benevol_tab, cong_ops_tab = st.tabs(tab_list)

# analysus
with member_tab:
        member_analysis(filtered_df)
with general_tab:
        general_analysis(filtered_df)
with contrib_tab:
        contributions_analysis(filtered_df)
with benevol_tab:
        benevol_disburs_analysis(filtered_df)
        

