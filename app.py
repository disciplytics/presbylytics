import streamlit as st
import pandas as pd
from utils.utils import snowflake_connection
from reports.pca_deep_dives import deep_dive_report
from reports.pca_metrics import pca_metrics
from analysis.member_analysis import member_analysis
from analysis.general_analysis import general_analysis
from analysis.contributions_analysis import contributions_analysis
from analysis.congregational_ops_analysis import congregational_ops_analysis
from analysis.benevol_disburs_analysis import benevol_disburs_analysis

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
df = snowflake_connection('select * from metrics_data where stat_year <> 0')

# clean up columns
df.columns = [i.strip("'").replace("_", " ").title() for i in df.columns]

df['Stat Year'] = df['Stat Year'].astype(str)

# create report type
# select a report
reportoption = st.selectbox(
        "Select a Report Type:",
        ("Membership", "General", "Contributions", "Benevol. Disbursments", "Congregational Ops."),
    )

# breakdowns
breakdown_options = ['All Churches', 'State', 'City', 'Church']
breakoption = st.segmented_control(
    "Breakdown By: ", breakdown_options, selection_mode="single", default ="All Churches"
)
    

if breakoption == 'All Churches':
    report_df = df.copy()
elif breakoption == 'State' or breakoption == 'City' or breakoption == 'Church':
    state_sel = st.selectbox(
                    "Select a State:",
                    sorted(pd.unique(df['State'].dropna()).tolist())
        )
        
    inter_df = df[df['State'] == state_sel]

    if breakoption == 'City' or breakoption == 'Church':
        city_sel = st.selectbox(
                    "Select a City:",
                    sorted(pd.unique(inter_df['City'].dropna()).tolist())
            )
        inter_2_df = inter_df[inter_df['City'] == city_sel]
        if breakoption == 'Church':
            church_sel = st.selectbox(
                    "Select a Church:",
                    sorted(pd.unique(inter_df['Church'].dropna()).tolist())
            )
        report_df = inter_2_df[inter_2_df['Church'] == church_sel]
        
        else:
            report_df = inter_2_df.copy()
            
    elif breakoption == 'State':
        report_df = inter_df.copy()
            
# populate the reports
try:
    if reportoption == "Membership":
        member_analysis(report_df)
    elif reportoption == "General":
        general_analysis(report_df)
    elif reportoption == "Contributions":
        contributions_analysis(report_df)
    elif reportoption == "Benevol. Disbursments":
        benevol_disburs_analysis(report_df)
    elif reportoption == "Congregational Ops.":
        congregational_ops_analysis(report_df)
except:
    st.write('Data is not good! Select Other Data.')
