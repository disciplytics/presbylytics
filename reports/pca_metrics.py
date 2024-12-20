def pca_metrics(df):
  import streamlit as st
  from millify import millify
  import pandas as pd

  # giving metrics functions
  def get_pcg(df):

    # calc giving per capita
    gpc = df.groupby(['Stat Year'])[['Total Contrib', 'Comm']].sum().reset_index()
    gpc = gpc.groupby(['Stat Year']).apply(lambda x: x['Total Contrib'] / x['Comm']).reset_index(name='Per Capita Giving')
  
    latest_year = gpc["Stat Year"].astype(int).max()
  
    pcg_lastest = millify(gpc[gpc["Stat Year"] == str(latest_year)]["Per Capita Giving"].values, precision=2)
    pcg_2nd_lastest = millify(gpc[gpc["Stat Year"] == str(latest_year-1)]["Per Capita Giving"].values, precision=2)

    st.metric(label = "Per Capita Giving", 
              value = f'{latest_year}: {pcg_lastest}', 
              delta= f'{latest_year-1}: {pcg_2nd_lastest}', 
              delta_color="normal",
             label_visibility="visible", 
              help = "PCG = Total Contrib / Comm")


  def get_pcb(df):
    # calc Benevolent per capita
    bpc = df.groupby(['Stat Year'])[['Total Benevolent Disbursements', 'Comm']].sum().reset_index()
    bpc = bpc.groupby(['Stat Year']).apply(lambda x: x['Total Benevolent Disbursements'] / x['Comm']).reset_index(name='Benevolent Disbursements Per Capita')
  
    latest_year = bpc["Stat Year"].astype(int).max()
  
    bpc_lastest = millify(bpc[bpc["Stat Year"] == str(latest_year)]["Benevolent Disbursements Per Capita"].values, precision=2)
    bpc_2nd_lastest = millify(bpc[bpc["Stat Year"] == str(latest_year-1)]["Benevolent Disbursements Per Capita"].values, precision=2)

    st.metric(label = "Per Capita Benevolent Disbursements", 
              value = f'{latest_year}: {bpc_lastest}', 
              delta= f'{latest_year-1}: {bpc_2nd_lastest}', 
              delta_color="normal",
             label_visibility="visible", 
              help = "Benevolent Disbursements Per Capita = Total Benevolent Disbursements / Comm")

  def get_pce(df):
    # calc expenses per capita
    epe = df.groupby(['Stat Year'])[['Current Expenses',  'Comm']].sum().reset_index()
    epe = epe.groupby(['Stat Year']).apply(lambda x: x['Current Expenses'] / x['Comm']).reset_index(name='Congregational Expenses Per Capita')
  
    latest_year = epe["Stat Year"].astype(int).max()
  
    epe_lastest = millify(epe[epe["Stat Year"] == str(latest_year)]["Congregational Expenses Per Capita"].values, precision=2)
    epe_2nd_lastest = millify(epe[epe["Stat Year"] == str(latest_year-1)]["Congregational Expenses Per Capita"].values, precision=2)

    st.metric(label = "Per Capita Expenses", 
              value = f'{latest_year}: {epe_lastest}', 
              delta= f'{latest_year-1}: {epe_2nd_lastest}', 
              delta_color="normal",
             label_visibility="visible", 
              help = "Congregational Expenses Per Capita = Current Expenses / Comm")

  def get_pcbf(df):
    # calc builing fund per capita
    pcbf = df.groupby(['Stat Year'])[['Building Fund', 'Comm']].sum().reset_index()
    pcbf = pcbf.groupby(['Stat Year']).apply(lambda x: x['Building Fund'] / x['Comm']).reset_index(name='Building Fund Per Capita')
  
    latest_year = pcbf["Stat Year"].astype(int).max()
  
    pcbf_lastest = millify(pcbf[pcbf["Stat Year"] == str(latest_year)]["Building Fund Per Capita"].values, precision=2)
    pcbf_2nd_lastest = millify(pcbf[pcbf["Stat Year"] == str(latest_year-1)]["Building Fund Per Capita"].values, precision=2)

    st.metric(label = "Per Capita Building Fund", 
              value = f'{latest_year}: {pcbf_lastest}', 
              delta= f'{latest_year-1}: {pcbf_2nd_lastest}', 
              delta_color="normal",
             label_visibility="visible", 
              help = "Building Fund Per Capita = Building Fund / Comm")


  def get_cpm(df):

    # calc Comm rate
    cpm = df.groupby(['Stat Year'])[['Non Comm', 'Comm']].sum().reset_index()
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

  def get_mpfu(df):

    # calc members per family units
    mpfu = df.groupby(['Stat Year'])[['Non Comm', 'Comm', 'Family Units']].sum().reset_index()
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

  def get_dpm(df):

    # calc deacons per members
    dpm = df.groupby(['Stat Year'])[['Non Comm', 'Comm', 'Deacons']].sum().reset_index()
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

  def get_epm(df):

    # calc elders per members
    epm = df.groupby(['Stat Year'])[['Non Comm', 'Comm', 'Ruling Elders']].sum().reset_index()
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
    


  st.subheader("Giving Metrics")
  pcg, pcb, pce, pcbf = st.columns(4)

  with pcg:
    get_pcg(df)
  with pcb:
    get_pcb(df)
  with pce:
    get_pce(df)
  with pcbf:
    get_pcbf(df)


  

  st.subheader("Member Metrics")
  cpm, mpfu, dpm, epm = st.columns(4)

  with cpm:
    get_cpm(df)
  with mpfu:
    get_mpfu(df)
  with dpm:
    get_dpm(df)
  with epm:
    get_epm(df)



  giving_tab, members_tab = st.tabs(["Giving", "Members"])
  max_year = df["Stat Year"].astype(int).max()

  with giving_tab:
    st.write(f'Per Capita Giving: {max_year}')
    state_sel = st.selectbox('Select A State to See Cities: ', pd.Series(pd.unique(df['State'])).sort_values())
    
    # calc giving per capita
    gpcst = df[df['Stat Year'] == str(max_year)].groupby(['State'])[['Total Contrib', 'Comm']].sum().reset_index()
    gpcst = gpcst.groupby(['State']).apply(lambda x: x['Total Contrib'] / x['Comm']).reset_index(name='Per Capita Giving')

    st.bar_chart(
      gpcst, x = 'State', y = 'Per Capita Giving', horizontal = False)

    
    if state_sel:
      city_col, church_col = st.columns(2)
      # calc giving per capita
      gpcc = df[(df['Stat Year'] == str(max_year)) & (df['State'] == state_sel)].groupby(['City'])[['Total Contrib', 'Comm']].sum().reset_index()
      gpcc = gpcc.groupby(['City']).apply(lambda x: x['Total Contrib'] / x['Comm']).reset_index(name='Per Capita Giving')
  
      city_col.bar_chart(
        gpcc, x = 'City', y = 'Per Capita Giving', horizontal = True)

      gpch = df[(df['Stat Year'] == str(max_year)) & (df['State'] == state_sel)].groupby(['Church'])[['Total Contrib', 'Comm']].sum().reset_index()
      gpch = gpch.groupby(['Church']).apply(lambda x: x['Total Contrib'] / x['Comm']).reset_index(name='Per Capita Giving')
  
      church_col.bar_chart(
        gpch, x = 'Church', y = 'Per Capita Giving', horizontal = True)



  with members_tab:
    st.write(f'Deacons Per Member: {max_year}')
    state_sel_mem = st.selectbox('Select a State to See Cities: ', pd.Series(pd.unique(df['State'])).sort_values())
    
    # calc deacons per members
    dpm = df[df['Stat Year'] == str(max_year)].groupby(['State'])[['Non Comm', 'Comm', 'Deacons']].sum().reset_index()
    dpm['Total'] = dpm['Non Comm'] + dpm['Comm']
    dpm = dpm.groupby(['State']).apply(lambda x: x['Deacons'] / x['Total']).reset_index(name='Deacons Per Members')

    st.bar_chart(
      dpm, x = 'State', y = 'Deacons Per Members', horizontal = False)

    
    if state_sel_mem:
      city_col, church_col = st.columns(2)
      # calc dpm
      dpmc = df[(df['Stat Year'] == str(max_year)) & (df['State'] == state_sel_mem)].groupby(['City'])[['Non Comm', 'Comm', 'Deacons']].sum().reset_index()
      dpmc['Total'] = dpmc['Non Comm'] + dpmc['Comm']
      dpmc = dpmc.groupby(['City']).apply(lambda x: x['Deacons'] / x['Total']).reset_index(name='Deacons Per Members')
  
      city_col.bar_chart(
        dpmc, x = 'City', y = 'Per Capita Giving', horizontal = True)

      # calc deacons per members
      dpmch = df[(df['Stat Year'] == str(max_year)) & (df['State'] == state_sel_mem)].groupby(['Church'])[['Non Comm', 'Comm', 'Deacons']].sum().reset_index()
      dpmch['Total'] = dpmc['Non Comm'] + dpmc['Comm']
      dpmch = dpmch.groupby(['Church']).apply(lambda x: x['Deacons'] / x['Total']).reset_index(name='Deacons Per Members')
  
      church_col.bar_chart(
        dpmch, x = 'Church', y = 'Deacons Per Members', horizontal = True)
    
  
