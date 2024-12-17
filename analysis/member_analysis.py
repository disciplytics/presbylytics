def member_analysis(data):
  from streamlit import subheader, bar_chart
  subheader('Member Count Trends')
  bar_chart(
          data.groupby(['Stat Year'])[['Comm', 'Non Comm']].sum(),
          y = ['Comm', 'Non Comm']
        )

  subheader('Additions & Losses')
  additions = ['Prof Child', 'Prof Adult', 'Trans Letter', 'Reaffirmation', 'Restored']
  losses = ['Death', 'Trans', 'Removed From Roll', 'Discipline']
  
  for i in losses:
    data[i] = data[i] * -1 
    
  bar_chart(
          data.groupby(['Stat Year'])[additions + losses].sum(),
          y = additions + losses,
          stack = 'True'
  )

  #bar_chart(
  #        data.groupby(['Stat Year'])[losses].sum(),
  #        y = losses
  #)
