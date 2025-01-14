import streamlit as st
import pandas as pd
from utils.utils import snowflake_connection
from reports.pca_deep_dives import deep_dive_report
from reports.pca_metrics import pca_metrics

# set page configs
st.set_page_config(
    page_title="PCA Analytics",
    layout="wide",)

# title
st.title('PCA Statistics :church:', help = 'All data is from [The PCA](https://presbyteryportal.pcanet.org/Report/StatsReport)')

# logo
#st.logo(image="images/dl_dark_logo.png", size = "large")

# click to learn more expander
with st.expander("Click to Learn More"):
    st.write("This app displays the Presbyterian Church in America statistics in an interactive frontend for enhanced analysis.")
    st.write("Breakdown the analysis by state, city, or all churches")

# connect and load from snowflake
df = snowflake_connection('select * from analytics_data where stat_year <> 0')

# clean up columns
df.columns = [i.strip("'").replace("_", " ").title() for i in df.columns]

df['Stat Year'] = df['Stat Year'].astype(str)
df['Longitude'] = df['Longitude'].astype(float)
df['Latitude'] = df['Latitude'].astype(float)

# 
map_df = df[df['Stat Year'] == '2023']
map_df = map_df[['Latitude', 'Longitude', 'City', 'State', 'Church']].dropna()
map_df = map_df.drop_duplicates(subset=['City', 'State', 'Church'])
# map of churches
st.map(map_df, latitude = 'Latitude', longitude = 'Longitude')

# create report type
report_options = ["PCA Metrics" , "PCA Stats Deep Dives"]
report_selection = st.segmented_control(
    "Report Types", report_options, selection_mode="single", default ="PCA Metrics"
)

if report_selection == "PCA Metrics":
    pca_metrics(df)
    
elif report_selection == "PCA Stats Deep Dives":
    deep_dive_report(df)
