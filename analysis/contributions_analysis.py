def contributions_analysis(data):
  import streamlit as st
  from millify import millify
  import pandas as pd

  # giving metrics functions
  def get_pcg(data):
    
    # calc giving per capita
    gpc = data.groupby(['Stat Year'])[['Total Contrib', 'Comm']].sum().reset_index()
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
  
  
  def get_pcb(data):
    # calc Benevolent per capita
    bpc = data.groupby(['Stat Year'])[['Total Benevolent Disbursements', 'Comm']].sum().reset_index()
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
  
  def get_pce(data):
    # calc expenses per capita
    epe = data.groupby(['Stat Year'])[['Current Expenses',  'Comm']].sum().reset_index()
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
  
  def get_pcbf(data):
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

  st.subheader("Contribution Metrics")
  pcg, pcb = st.columns(2)
  pce, pcbf = st.columns(2)
      
  with pcg:
    get_pcg(data)
  with pcb:
    get_pcb(data)
  with pce:
    get_pce(data)
  with pcbf:
    get_pcbf(data)

  
  st.bar_chart(
          gpcst, x = 'State', y = 'Per Capita Giving', horizontal = True)

  
  st.subheader('Contribution Trends')

  st.write('Total Church Income')
  st.bar_chart(
            data.groupby(['Stat Year'])['Total Church Income'].sum(),
            y = 'Total Church Income'
          )

  st.write('Giving Per Capita Trends')
  # calc giving per capita
  gpc = data.groupby(['Stat Year'])[['Total Contrib', 'Comm']].sum().reset_index()
  gpc = gpc.groupby(['Stat Year']).apply(lambda x: x['Total Contrib'] / x['Comm']).reset_index(name='Giving Per Capita')
  st.bar_chart(
            gpc,
            y = 'Giving Per Capita',
            x = 'Stat Year'
          )
  
  st.write('Contributions Breakdown')
  st.bar_chart(
            data.groupby(['Stat Year'])[['Tithes Offerings', 'Special Causes', 'Building Fund Offering', 'Other Contrib', 'Other Income']].sum(),
            y = ['Tithes Offerings', 'Special Causes', 'Building Fund Offering', 'Other Contrib', 'Other Income']
          )
