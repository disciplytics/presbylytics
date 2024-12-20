def pca_metrics(df):
  import streamlit as st
  from millify import millify



  st.subheader("Giving Metrics")

  # calc giving per capita
  gpc = df.groupby(['Stat Year'])[['Total Contrib', 'Comm']].sum().reset_index()
  gpc = gpc.groupby(['Stat Year']).apply(lambda x: x['Total Contrib'] / x['Comm']).reset_index(name='Per Capita Giving')
  gpc = gpc.sort_values(by = 'Stat Year', ascending=True)

  latest_year = gpc["Stat Year"].astype(int).max()

  pcg_lastest = millify(gpc[gpc["Stat Year"] == str(latest_year)]["Per Capita Giving"].values)
  pcg_2nd_lastest = millify(gpc[gpc["Stat Year"] == str(latest_year-1)]["Per Capita Giving"].values)
  
  st.write(f'{pcg_lastest} and {str(latest_year)}')
  st.write(f'{pcg_2nd_lastest} and {str(latest_year-1)}')

  
  
