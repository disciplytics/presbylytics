def member_analysis(data):
  from streamlit import subheader, bar_chart
  subheader('Member Count Trends')
  bar_chart(
          data.groupby(['Stat Year'])[['Comm', 'Non Comm']].sum(),
          y = ['Comm', 'Non Comm']
        )

  subheader('Additions & Losses')
  bar_chart(
          data.groupby(['Stat Year'])[['Prof Child',	'Prof Adult']].sum(),
          y = ['Prof Child',	'Prof Adult']
  )
