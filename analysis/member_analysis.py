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

  st.subheader("Breakdown: Additions & Losses")
  add_col, loss_col = st.columns(2)
  years = data['Stat Year'].unique().tolist()
  year_filter = st.selectbox('Select a Stat Year:', years, index=0)
  break_df = data[data['Stat Year'] == year_filter]

  st.write(f'Selected Year: {year_filter}')
  with add_col:
    st.bar_chart(
      break_df,
      x = additions)
      

  
