def pca_metrics(df):
  import streamlit as st
  from millify import millify



  st.subheader("Giving Metrics")

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



  

  

  pcg, pcb, pce, pcbf = st.columns(4)

  with pcg:
    get_pcg(df)
  with pcb:
    get_pcb(df)
  with get_pce:
    get_pce(df)
  with pcbf:
    get_pcbf(df)
