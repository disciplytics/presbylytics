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
  
  gpc = data.groupby(['Stat Year']).apply(lambda x: x['Total Contrib'] / x['Comm'])#.reset_index(name='Giving Per Capita')
  st.write(gpc)
  st.write('Giving Per Capita')
  st.bar_chart(
            #data.groupby(['Stat Year'])['Per Capita Giving'].sum(),
            gpc,
            y = 'Giving Per Capita'
           # y = 'Per Capita Giving'
          )
  
  bpc_col, epc_col = st.columns(2)
  with bpc_col:
    st.write('Benevolent Disbursements Per Capita: Total Benevolent Disbursements / Comm')
    st.bar_chart(
            data.groupby(['Stat Year'])['Benevolent Disbursements Per Capita'].sum(),
            y = 'Benevolent Disbursements Per Capita'
          )
  with epc_col:
    st.write('Congregational Expenses Per Capita: (Current Expenses + Building Fund) / Comm')
    st.bar_chart(
            data.groupby(['Stat Year'])['Congregational Expenses Per Capita'].sum(),
            y = 'Congregational Expenses Per Capita'
          )
