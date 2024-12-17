def overview_analysis(data):
  import streamlit as st
  st.subheader('Metrics Overview')

  st.subheader('Members & Family Metrics')
  data['Total Members'] = data['Comm'] + data['Non Comm']

  total_mem_col, fus_col = st.columns(2)
  with total_mem_col:
    st.write('Total Members: (Comm + Non Comm)')
    st.bar_chart(
            data.groupby(['Stat Year'])['Total Members'].sum(),
            y = 'Total Members'
          )
  with fus_col:
    st.write('Family Units')
    st.bar_chart(
            data.groupby(['Stat Year'])['Family Units'].sum(),
            y = 'Family Units'
          )
  

  st.subheader('Giving, Disbursements, & Expenses Metrics')
  data['Benevolent Disbursements Per Capita'] = data['Total Benevolent Disbursements'] / data['Comm']
  data['Congregational Expenses Per Capita'] = (data['Current Expenses'] +  data['Building Fund']) / data['Comm']

  # calc giving per capita
  gpc = data.groupby(['Stat Year'])[['Total Contrib', 'Comm']].sum().reset_index()
  gpc = gpc.groupby(['Stat Year']).apply(lambda x: x['Total Contrib'] / x['Comm']).reset_index(name='Giving Per Capita')

   # calc Benevolent per capita
  bpc = data.groupby(['Stat Year'])[['Total Benevolent Disbursements', 'Comm']].sum().reset_index()
  bpc = bpc.groupby(['Stat Year']).apply(lambda x: x['Total Benevolent Disbursements'] / x['Comm']).reset_index(name='Benevolent Disbursements Per Capita')

  # calc Congregational per capita
  epc = data.groupby(['Stat Year'])[['Current Expenses', 'Building Fund', 'Comm']].sum().reset_index()
  epc = epc.groupby(['Stat Year']).apply(lambda x: (x['Current Expenses'] + x['Building Fund']) / x['Comm']).reset_index(name='Congregational Expenses Per Capita')
  
  st.write('Giving Per Capita')
  st.bar_chart(
            gpc,
            y = 'Giving Per Capita',
            x = 'Stat Year'
          )
  
  bpc_col, epc_col = st.columns(2)
  with bpc_col:
    st.write('Benevolent Disbursements Per Capita: Total Benevolent Disbursements / Comm')
    st.bar_chart(
            bpc,
            y = 'Benevolent Disbursements Per Capita',
            x = 'Stat Year'
          )
  with epc_col:
    st.write('Congregational Expenses Per Capita: (Current Expenses + Building Fund) / Comm')
    st.bar_chart(
            epc,
            y = 'Congregational Expenses Per Capita',
            x = 'Stat Year'
          )
