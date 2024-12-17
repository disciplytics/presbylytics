def congregational_ops_analysis(data):
  import streamlit as st
  st.subheader('Congregational Ops. Trends')

  exp_col, bf_col = st.columns(2)

  with exp_col:
    st.write('Current Expenses')
    st.bar_chart(
            data.groupby(['Stat Year'])['Current Expenses'].sum(),
            y = 'Current Expenses'
          )
  with bf_col:
    st.write('Building Fund')
    st.bar_chart(
            data.groupby(['Stat Year'])['Building Fund'].sum(),
            y = 'Building Fund'
          )
