import streamlit as st
import pandas as pd
from utils.utils import snowflake_connection
from analysis.member_analysis import member_analysis
from analysis.general_analysis import general_analysis
from analysis.contributions_analysis import contributions_analysis
from analysis.benevol_disburs_analysis import benevol_disburs_analysis
from analysis.congregational_ops_analysis import congregational_ops_analysis
from analysis.churchhealth_analysis import churchhealth_analysis


def deep_dive_report(df):
  options = ["All Churches", "Single Church"]
  selection = st.segmented_control(
        "Drilldown Levels", options, selection_mode="single", default ="All Churches"
    )
    
  if selection == "All Churches":
    # create filters
    st.sidebar.subheader("Filtering Options For A Deep Dive")
    st.sidebar.write("Select A State")
            
    state_sel = st.sidebar.multiselect(
                'Select Church State:', 
                pd.Series(pd.unique(df['State'])).sort_values(),
                pd.Series(pd.unique(df['State'])).sort_values()
              )
            
    if len(state_sel) == 1:
      filtered_df = df[df['State'].isin(state_sel)]
      
      city_sel = st.sidebar.multiselect(
                'Select Church City:', 
                pd.Series(pd.unique(filtered_df['City'])).sort_values(),
                pd.Series(pd.unique(filtered_df['City'])).sort_values()
              )
            
      filtered_df = filtered_df[filtered_df['City'].isin(city_sel)]
      
      church_sel = st.sidebar.multiselect(
                'Select Church Name:',
                pd.Series(pd.unique(filtered_df['Church'])).sort_values(),
                pd.Series(pd.unique(filtered_df['Church'])).sort_values()
              )
            
      filtered_df = filtered_df[filtered_df['Church'].isin(church_sel)]
    else:
      filtered_df = df.copy()
      tab_list = ['Church Health', 'Member Data', 'General Data', 'Contributions Data', 'Benevolent Disbursements Data', 'Conregation Ops']
      ch_tab, member_tab, general_tab, contrib_tab, benevol_tab, cong_ops_tab = st.tabs(tab_list)
            
      # analyses
      with ch_tab:
        churchhealth_analysis(filtered_df)
      with member_tab:
        member_analysis(filtered_df)
      with general_tab:
        general_analysis(filtered_df)
      with contrib_tab:
        contributions_analysis(filtered_df)
      with benevol_tab:
        benevol_disburs_analysis(filtered_df)
      with cong_ops_tab:
        congregational_ops_analysis(filtered_df)
    
  elif selection == "Single Church":
    # create filters
    st.sidebar.subheader("Filtering Options For A Single Church")
    st.sidebar.write("Select A State")
            
    state_sel = st.sidebar.selectbox(
                'Select Church State:', 
                pd.Series(pd.unique(df['State'])).sort_values(),
              )
            
    if state_sel:
      filtered_df = df[df['State'] == state_sel]
                    
      city_sel = st.sidebar.selectbox(
                'Select Church City:', 
                pd.Series(pd.unique(filtered_df['City'])).sort_values(),
              )
            
      filtered_df = filtered_df[filtered_df['City'] == city_sel]
            
      if city_sel:
        church_sel = st.sidebar.selectbox(
                        'Select Church Name:',
                        pd.Series(pd.unique(filtered_df['Church'])).sort_values()
                      )
                    
        filtered_df = filtered_df[filtered_df['Church'] == church_sel]
                    
            
        tab_list = ['Church Health', 'Member Data', 'General Data', 'Contributions Data', 'Benevolent Disbursements Data', 'Conregation Ops']
        ch_tab, member_tab, general_tab, contrib_tab, benevol_tab, cong_ops_tab = st.tabs(tab_list)
                    
        # analyses
        try:
          with ch_tab:
            churchhealth_analysis(filtered_df)
          with member_tab:
            member_analysis(filtered_df)
          with general_tab:
            general_analysis(filtered_df)
          with contrib_tab:
            contributions_analysis(filtered_df)
          with benevol_tab:
            benevol_disburs_analysis(filtered_df)
          with cong_ops_tab:
            congregational_ops_analysis(filtered_df)        
        except:
          st.write('Church has bad data. Select another option.')
