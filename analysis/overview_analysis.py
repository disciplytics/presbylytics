def overview_analysis(data):
  import streamlit as st
  st.subheader('Metrics Overview \n\n')



  st.subheader('Giving, Disbursements, & Expenses Metrics')
  data['Benevolent Disbursements Per Capita'] = data['Total Benevolent Disbursements'] / data['Comm']
  data['Congregational Expenses Per Capita'] = (data['Current Expenses'] +  data['Building Fund']) / data['Comm']
  
  bpc_col, epc_col = st.columns(2)

  st.write('Giving Per Capita')
  st.bar_chart(
            data.groupby(['Stat Year'])['Per Capita Giving'].sum(),
            y = 'Per Capita Giving'
          )
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
