import streamlit as st
import pandas as pd
import pydeck
import numpy as np
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

# analyses
analyses = ['Trend Reports', 'Spatial Reports']
analysis = st.segmented_control(
    "Drill Down Level: ", analyses, selection_mode="single", default ="Trend Reports"
)

if analysis == "Trend Reports":
    # create report type
    # select a report
    reportoption = st.selectbox(
            "Select a Report Type:",
            ("Membership", "General", "Contributions", "Benevol. Disbursments", "Congregational Ops."),
        )
    
    # breakdowns
    breakdown_options = ['All Churches', 'State', 'City', 'Church']
    breakoption = st.segmented_control(
        "Drill Down Level: ", breakdown_options, selection_mode="single", default ="All Churches"
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
                            sorted(pd.unique(inter_2_df['Church'].dropna()).tolist())
                    )
                    
                report_df = inter_2_df[inter_2_df['Church'] == church_sel]
            
            elif breakoption == 'City':
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
        
elif analysis == "Spatial Reports":
    # connect and load from snowflake
    spdf = snowflake_connection('select * from spatial_analytics_data where stat_year <> 0')
    
    # clean up columns
    spdf.columns = [i.strip("'").replace("_", " ").title() for i in spdf.columns]

    spdf['Stat Year'] = spdf['Stat Year'].astype(str)
    spdf['latitude'] = spdf['Latitude'].astype(float)
    spdf['longitude'] = spdf['Longitude'].astype(float)

    spdf = spdf.drop_duplicates(subset=['Church', 'State', 'City']).dropna()

    st.subheader('Spatial Analysis of 2023 Data and a Subset of Churches')
    reportoption = st.selectbox(
            "Select a Report Type:",
            ("Contributions", "Members"),
        )

    if reportoption == "Contributions":

        chart_data = spdf[['longitude', 'latitude', 'Church', 'Total Contrib']]
        chart_data['size'] = np.log(chart_data['Total Contrib']) * 1000
        point_layer = pydeck.Layer(
                        "ScatterplotLayer",
                        data=chart_data,
                        id="Church",
                        get_position=["longitude", "latitude"],
                        get_color="[255, 75, 75]",
                        pickable=True,
                        auto_highlight=True,
                        get_radius="size",
                    )

        view_state = pydeck.ViewState(
        latitude=40, longitude=-117, controller=True, zoom=2.4, pitch=15
    )
    
        chart = pydeck.Deck(
            point_layer,
            initial_view_state=view_state,
            tooltip={"text": "{Church} /n Total Contrib: {Total Contrib}"},
        )
        
        event = st.pydeck_chart(chart, on_select="rerun", selection_mode="multi-object")
    
    
    elif reportoption == "Members":
        chart_data = spdf[['longitude', 'latitude', 'Church', 'Comm', 'Non Comm']]
        chart_data['Total Members'] = chart_data['Comm'] + chart_data['Non Comm']

        chart_data = chart_data[['longitude', 'latitude', 'Church', 'Total Members']]
        chart_data['size'] = chart_data['Total Members'] * 10
        point_layer = pydeck.Layer(
                        "ScatterplotLayer",
                        data=chart_data,
                        id="Church",
                        get_position=["longitude", "latitude"],
                        get_color="[255, 75, 75]",
                        pickable=True,
                        auto_highlight=True,
                        get_radius="size",
                    )

        view_state = pydeck.ViewState(
        latitude=40, longitude=-117, controller=True, zoom=2.4, pitch=15
    )
    
        chart = pydeck.Deck(
            point_layer,
            initial_view_state=view_state,
            tooltip={"text": "{Church} \n Total Members: {Total Members}"},
        )
        
        event = st.pydeck_chart(chart, on_select="rerun", selection_mode="multi-object")
        
    else:
        st.subheader('Select an analysis to get started.')

else:
    st.subheader('Select an analysis to get started.')
    
    
