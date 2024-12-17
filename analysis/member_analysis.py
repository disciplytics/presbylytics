def member_analysis(data):
  import streamlit as st
  st.subheader('Member Count Trends')
  st.bar_chart(
          data.groupby(['Stat Year'])[['Comm', 'Non Comm']].sum(),
          y = ['Comm', 'Non Comm']
        )

  st.subheader('Additions & Losses')
  additions = ['Prof Child', 'Prof Adult', 'Trans Letter', 'Reaffirmation', 'Restored']
  losses = ['Death', 'Trans', 'Removed From Roll', 'Discipline']
  
  for i in losses:
    data[i] = data[i] * -1 
    
  st.bar_chart(
          data.groupby(['Stat Year'])[additions + losses].sum(),
          y = additions + losses,
          stack = False
  )
