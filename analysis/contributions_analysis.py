def contributions_analysis(data):
  import streamlit as st
  st.subheader('Contribution Trends')

  st.write('Total Church Income')
  st.bar_chart(
            data.groupby(['Stat Year'])['Total Church Income'].sum(),
            y = 'Total Church Income'
          )

  st.write('Giving Per Capita Trends')
  st.bar_chart(
            data.groupby(['Stat Year'])['Per Capita Giving'].sum(),
            y = 'Per Capita Giving'
          )
  
  st.write('Contributions Breakdown')
  st.bar_chart(
            data.groupby(['Stat Year'])[['Tithes Offerings', 'Special Causes', 'Building Fund Offering', 'Other Contrib', 'Other Income']].sum(),
            y = ['Tithes Offerings', 'Special Causes', 'Building Fund Offering', 'Other Contrib', 'Other Income']
          )
