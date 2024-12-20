import streamlit as st
import pandas as pd
from utils.utils import snowflake_connection
from analysis.member_analysis import member_analysis
from analysis.general_analysis import general_analysis
from analysis.contributions_analysis import contributions_analysis
from analysis.benevol_disburs_analysis import benevol_disburs_analysis
from analysis.congregational_ops_analysis import congregational_ops_analysis
from analysis.churchhealth_analysis import churchhealth_analysis 



from reports.pca_deep_dives import deep_dive_report

# set page configs
st.set_page_config(
    page_title="PCA Analytics",
    layout="wide",)

# title
st.title('PCA Statistics :church:', help = 'All data is from [The PCA](https://presbyteryportal.pcanet.org/Report/StatsReport)')

# logo
#st.logo(image="images/dl_dark_logo.png", size = "large")

with st.expander("Click to Learn More"):
    st.write("This app displays the Presbyterian Church in America statistics in an interactive frontend for enhanced analysis.")
    st.write("Breakdown the analysis by state, city, or all churches")

# connect and load from snowflake
df = snowflake_connection('select * from metrics_data where stat_year <> 0')

# clean up columns
df.columns = [i.strip("'").replace("_", " ").title() for i in df.columns]

df['Stat Year'] = df['Stat Year'].astype(str)

# create report type
report_options = ["PCA Metrics" , "PCA Stats Deep Dives"]
report_selection = st.segmented_control(
    "Report Types", report_options, selection_mode="single", default ="PCA Metrics"
)


if report_selection == "PCA Stats Deep Dives":
    deep_dive_report(df)
