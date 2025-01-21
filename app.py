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
analyses = ['Trend Reports', 'Spatial Reports', 'Forecast Reports']
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
    spdf = snowflake_connection("""select *, geocode['latitude'] as latitude, geocode['longitude'] as longitude from geocoded_metrics_data where stat_year <> 0""")
    # clean up columns
    spdf.columns = [i.strip("'").replace("_", " ").title() for i in spdf.columns]

    spdf['Stat Year'] = spdf['Stat Year'].astype(str)
    spdf['latitude'] = spdf['Latitude'].astype(float)
    spdf['longitude'] = spdf['Longitude'].astype(float)
    spdf['Benevol % Grand Total'] = spdf['Benevol Grand Total'].astype(float)
    spdf['Per Capita Giving'] = spdf['Per Capita Giving'].astype(float)
    

    spdf = spdf.drop_duplicates(subset=['Church', 'State', 'City']).dropna()

    st.subheader('Spatial Analysis of 2023 Data')
    reportoption = st.selectbox(
            "Select a Report Type:",
            ("Contributions", "Members", "Per Capita Giving", "Benevol % Grand Total"),
        )

    if reportoption == "Contributions":

        chart_data = spdf[['longitude', 'latitude', 'Church', 'State', 'City', 'Total Contrib']]

        chart_data['Total Contrib'] = np.round(chart_data['Total Contrib'] / 1000000, 2)
        chart_data['size'] = chart_data['Total Contrib']*1000 #(chart_data['Total Contrib'] - np.mean(chart_data['Total Contrib']))/500

        chart_data['Total Contrib'] = chart_data['Total Contrib'].apply("{:,}".format)
        point_layer = pydeck.Layer(
                        "ScatterplotLayer",
                        data=chart_data,
                        id="Church-City-State",
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
            map_provider='mapbox',
            map_style=pydeck.map_styles.CARTO_ROAD,
            tooltip={"text": "{Church} \n City: {City} \n State: {State} \n Total Contrib: ${Total Contrib}M"},
        )
        
        event = st.pydeck_chart(chart, on_select="rerun", selection_mode="multi-object")

    elif reportoption == "Per Capita Giving":

        chart_data = spdf[['longitude', 'latitude', 'Church', 'State', 'City', 'Per Capita Giving']]

        chart_data['Per Capita Giving'] = np.round(chart_data['Per Capita Giving'] / 1000, 2)
        chart_data['size'] = chart_data['Per Capita Giving']*1000 #(chart_data['Total Contrib'] - np.mean(chart_data['Total Contrib']))/500

        chart_data['Per Capita Giving'] = chart_data['Per Capita Giving'].apply("{:,}".format)
        point_layer = pydeck.Layer(
                        "ScatterplotLayer",
                        data=chart_data,
                        opacity=0.5,
                        id="Church-City-State",
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
            map_provider='mapbox',
            map_style=pydeck.map_styles.CARTO_ROAD,
            tooltip={"text": "{Church} \n City: {City} \n State: {State} \n Per Capita Giving: ${Per Capita Giving}K"},
        )
        
        event = st.pydeck_chart(chart, on_select="rerun", selection_mode="multi-object")

    elif reportoption == "Benevol % Grand Total":

        chart_data = spdf[['longitude', 'latitude', 'Church', 'State', 'City', 'Benevol % Grand Total']]

        chart_data['Benevol % Grand Total'] = np.round(chart_data['Benevol % Grand Total']*100, 2)
        chart_data['size'] = chart_data['Benevol % Grand Total']*250 

        chart_data['Benevol % Grand Total'] = chart_data['Benevol % Grand Total'].apply("{:,}".format)
        point_layer = pydeck.Layer(
                        "ScatterplotLayer",
                        data=chart_data,
                        opacity=0.5,
                        id="Church-City-State",
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
            map_provider='mapbox',
            map_style=pydeck.map_styles.CARTO_ROAD,
            tooltip={"text": "{Church} \n City: {City} \n State: {State} \n Benevol % Grand Total: {Benevol % Grand Total}%"},
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
            map_provider='mapbox',
            map_style=pydeck.map_styles.CARTO_ROAD,
            initial_view_state=view_state,
            tooltip={"text": "{Church} \n Total Members: {Total Members}"},
        )
        
        event = st.pydeck_chart(chart, on_select="rerun", selection_mode="multi-object")

        #st.write(event)
        
    else:
        st.subheader('Select an analysis to get started.')

elif analysis == "Forecast Reports":
    # connect and load from snowflake
    fcdf = snowflake_connection("""select * from contribs_forecast_data""")
    # clean up columns
    fcdf.columns = [i.strip("'").replace("_", " ").title() for i in fcdf.columns]

    fcdf['Stat Year'] = pd.to_datetime(fcdf['Stat Year']).dt.year.astype(str)

    # breakdowns
    breakdown_options = ['All Churches', 'State', 'City', 'Church']
    breakoption = st.segmented_control(
        "Drill Down Level: ", breakdown_options, selection_mode="single", default ="All Churches"
    )
        
    
    if breakoption == 'All Churches':
        report_df = fcdf.replace(0,float('NaN'))
        report_df['Forecast'] = np.where((report_df['Stat Year'].astype(int) < 2024) & (report_df['Forecast'] != 0), 0, report_df['Forecast'])
        report_df['Lower Bound'] = np.where((report_df['Stat Year'].astype(int) < 2024) & (report_df['Lower Bound'] != 0), 0, report_df['Lower Bound'])
        report_df['Upper Bound'] = np.where((report_df['Stat Year'].astype(int) < 2024) & (report_df['Upper Bound'] != 0), 0, report_df['Upper Bound'])
        report_df = report_df.replace(0,float('NaN'))
        
    elif breakoption == 'State' or breakoption == 'City' or breakoption == 'Church':
        state_sel = st.selectbox(
                        "Select a State:",
                        sorted(pd.unique(fcdf['State'].dropna()).tolist())
            )
            
        inter_df = fcdf[fcdf['State'] == state_sel].replace(0,float('NaN'))
    
        if breakoption == 'City' or breakoption == 'Church':
            city_sel = st.selectbox(
                        "Select a City:",
                        sorted(pd.unique(inter_df['City'].dropna()).tolist())
                )
            inter_2_df = inter_df[inter_df['City'] == city_sel].replace(0,float('NaN'))
            
            if breakoption == 'Church':
                church_sel = st.selectbox(
                            "Select a Church:",
                            sorted(pd.unique(inter_2_df['Church'].dropna()).tolist())
                    )
                    
                report_df = inter_2_df[inter_2_df['Church'] == church_sel].replace(0,float('NaN'))

                report_df['Forecast'] = np.where((report_df['Stat Year'].astype(int) < 2024) & (report_df['Forecast'] != 0), 0, report_df['Forecast'])
                report_df['Lower Bound'] = np.where((report_df['Stat Year'].astype(int) < 2024) & (report_df['Lower Bound'] != 0), 0, report_df['Lower Bound'])
                report_df['Upper Bound'] = np.where((report_df['Stat Year'].astype(int) < 2024) & (report_df['Upper Bound'] != 0), 0, report_df['Upper Bound'])
                report_df = report_df.replace(0,float('NaN'))
            
            elif breakoption == 'City':
                report_df = inter_2_df.replace(0,float('NaN'))
                report_df['Forecast'] = np.where((report_df['Stat Year'].astype(int) < 2024) & (report_df['Forecast'] != 0), 0, report_df['Forecast'])
                report_df['Lower Bound'] = np.where((report_df['Stat Year'].astype(int) < 2024) & (report_df['Lower Bound'] != 0), 0, report_df['Lower Bound'])
                report_df['Upper Bound'] = np.where((report_df['Stat Year'].astype(int) < 2024) & (report_df['Upper Bound'] != 0), 0, report_df['Upper Bound'])
                report_df = report_df.replace(0,float('NaN'))
                
        elif breakoption == 'State':
            report_df = inter_df.replace(0,float('NaN'))
            report_df['Forecast'] = np.where((report_df['Stat Year'].astype(int) < 2024) & (report_df['Forecast'] != 0), 0, report_df['Forecast'])
            report_df['Lower Bound'] = np.where((report_df['Stat Year'].astype(int) < 2024) & (report_df['Lower Bound'] != 0), 0, report_df['Lower Bound'])
            report_df['Upper Bound'] = np.where((report_df['Stat Year'].astype(int) < 2024) & (report_df['Upper Bound'] != 0), 0, report_df['Upper Bound'])
            report_df = report_df.replace(0,float('NaN'))

    
    #
    st.subheader('Total Contributions Forecast')

    st.line_chart(
        report_df.groupby(['Stat Year'])[['Total Contrib', 'Forecast', 'Lower Bound', 'Upper Bound']].sum().reset_index().replace(0,float('NaN')),
        x = 'Stat Year',
        y = ['Total Contrib', 'Forecast', 'Lower Bound', 'Upper Bound']
    )
    
else:
    st.subheader('Select an analysis to get started.')
