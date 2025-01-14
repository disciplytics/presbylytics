def member_analysis(data):
  import streamlit as st
  from millify import millify
  import pandas as pd

  def get_cpm(data):
  
      # calc Comm rate
      cpm = data.groupby(['Stat Year'])[['Non Comm', 'Comm']].sum().reset_index()
      cpm['Total'] = cpm['Non Comm'] + cpm['Comm']
      cpm = cpm.groupby(['Stat Year']).apply(lambda x: x['Comm'] / x['Total']).reset_index(name='Comm Per Members')
    
      latest_year = cpm["Stat Year"].astype(int).max()
    
      cpm_lastest = millify(cpm[cpm["Stat Year"] == str(latest_year)]["Comm Per Members"].values, precision=2)
      cpm_2nd_lastest = millify(cpm[cpm["Stat Year"] == str(latest_year-1)]["Comm Per Members"].values, precision=2)
  
      st.metric(label = "Comm Per Members", 
                value = f'{latest_year}: {cpm_lastest}', 
                delta= f'{latest_year-1}: {cpm_2nd_lastest}', 
                delta_color="normal",
               label_visibility="visible", 
                help = "Comm / (Comm + NonComm)")
  
    def get_mpfu(data):
  
      # calc members per family units
      mpfu = data.groupby(['Stat Year'])[['Non Comm', 'Comm', 'Family Units']].sum().reset_index()
      mpfu['Total'] = mpfu['Non Comm'] + mpfu['Comm']
      mpfu = mpfu.groupby(['Stat Year']).apply(lambda x: x['Total'] / x['Family Units']).reset_index(name='Family Unit Size')
    
      latest_year = mpfu["Stat Year"].astype(int).max()
    
      mpfu_lastest = millify(mpfu[mpfu["Stat Year"] == str(latest_year)]["Family Unit Size"].values, precision=2)
      mpfu_2nd_lastest = millify(mpfu[mpfu["Stat Year"] == str(latest_year-1)]["Family Unit Size"].values, precision=2)
  
      st.metric(label = "Family Unit Size", 
                value = f'{latest_year}: {mpfu_lastest}', 
                delta= f'{latest_year-1}: {mpfu_2nd_lastest}', 
                delta_color="normal",
               label_visibility="visible", 
                help = "Family Units / Total Members")
  
    def get_dpm(data):
  
      # calc deacons per members
      dpm = data.groupby(['Stat Year'])[['Non Comm', 'Comm', 'Deacons']].sum().reset_index()
      dpm['Total'] = dpm['Non Comm'] + dpm['Comm']
      dpm = dpm.groupby(['Stat Year']).apply(lambda x: x['Deacons'] / x['Total']).reset_index(name='Deacons Per Members')
    
      latest_year = dpm["Stat Year"].astype(int).max()
    
      dpm_lastest = millify(dpm[dpm["Stat Year"] == str(latest_year)]["Deacons Per Members"].values*100, precision=2)
      dpm_2nd_lastest = millify(dpm[dpm["Stat Year"] == str(latest_year-1)]["Deacons Per Members"].values*100, precision=2)
  
      st.metric(label = "Deacons Per 100 Members", 
                value = f'{latest_year}: {dpm_lastest}', 
                delta= f'{latest_year-1}: {dpm_2nd_lastest}', 
                delta_color="normal",
               label_visibility="visible", 
                help = "Deacons / Total Members")
  
    def get_epm(data):
  
      # calc elders per members
      epm = data.groupby(['Stat Year'])[['Non Comm', 'Comm', 'Ruling Elders']].sum().reset_index()
      epm['Total'] = epm['Non Comm'] + epm['Comm']
      epm = epm.groupby(['Stat Year']).apply(lambda x: x['Ruling Elders'] / x['Total']).reset_index(name='Ruling Elders Per Members')
    
      latest_year = epm["Stat Year"].astype(int).max()
    
      epm_lastest = millify(epm[epm["Stat Year"] == str(latest_year)]["Ruling Elders Per Members"].values*100, precision=2)
      epm_2nd_lastest = millify(epm[epm["Stat Year"] == str(latest_year-1)]["Ruling Elders Per Members"].values*100, precision=2)
  
      st.metric(label = "Ruling Elders Per 100 Members", 
                value = f'{latest_year}: {epm_lastest}', 
                delta= f'{latest_year-1}: {epm_2nd_lastest}', 
                delta_color="normal",
               label_visibility="visible", 
                help = "Ruling Elders / Total Members")

    st.subheader("Member Metrics")
  
    cpm, mpfu = st.columns(2)
    dpm, epm = st.columns(2)
  
    with cpm:
      get_cpm(data)
    with mpfu:
      get_mpfu(data)
    with dpm:
      get_dpm(data)
    with epm:
      get_epm(data)

  st.subheader('Member Count Trends')
  st.bar_chart(
          data.groupby(['Stat Year'])[['Comm', 'Non Comm']].sum(),
          y = ['Comm', 'Non Comm']
        )

  st.subheader('Additions & Losses')
  additions = ['Prof Child', 'Prof Adult', 'Trans Letter', 'Reaffirmation', 'Restored']
  losses = ['Death', 'Trans', 'Removed From Roll', 'Discipline']
  
  for i in losses:
    data[i] = data[i] * -1 
    
  st.bar_chart(
          data.groupby(['Stat Year'])[additions + losses].sum(),
          y = additions + losses,
          stack = False
  )
