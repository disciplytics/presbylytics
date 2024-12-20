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

    'Benevolent Disbursements Per Capita: Total Benevolent Disbursements / Comm'

    # calc Benevolent per capita
    bpc = df.groupby(['Stat Year'])[['Total Benevolent Disbursements', 'Comm']].sum().reset_index()
    bpc = bpc.groupby(['Stat Year']).apply(lambda x: x['Total Benevolent Disbursements'] / x['Comm']).reset_index(name='Benevolent Disbursements Per Capita')
  
    latest_year = bpc["Stat Year"].astype(int).max()
  
    bpc_lastest = millify(bpc[bpc["Stat Year"] == str(latest_year)]["Benevolent Disbursements Per Capita"].values, precision=2)
    bpc_2nd_lastest = millify(bpc[bpc["Stat Year"] == str(latest_year-1)]["Benevolent Disbursements Per Capita"].values, precision=2)

    st.metric(label = "Per Capita Giving", 
              value = f'{latest_year}: {bpc_lastest}', 
              delta= f'{latest_year-1}: {bpc_2nd_lastest}', 
              delta_color="normal",
             label_visibility="visible", 
              help = "Benevolent Disbursements Per Capita = Total Benevolent Disbursements / Comm")

  

  pcg, pcb, pcc = st.columns(3)

  with pcg:
    get_pcg(df)
  with pcb:
    get_pcb(df)
    
