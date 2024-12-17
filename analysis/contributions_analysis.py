def contributions_analysis(data):
  import streamlit as st
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
