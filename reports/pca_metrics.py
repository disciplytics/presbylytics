def pca_metrics(df):
  import streamlit as st
  from millify import millify



  st.subheader("Giving Metrics")

  # calc giving per capita
  gpc = df.groupby(['Stat Year'])[['Total Contrib', 'Comm']].sum().reset_index()
  gpc = gpc.groupby(['Stat Year']).apply(lambda x: x['Total Contrib'] / x['Comm']).reset_index(name='Per Capita Giving')
  gpc = gpc.sort_values(by = 'Stat Year', ascending=False)

  st.write(f'{gpc["Per Capita Giving"].loc[0]} and {gpc["Stat Year"].loc[0]}')


  
  
