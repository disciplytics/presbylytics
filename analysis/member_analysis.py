def member_analysis(data):
  from streamlit import subheader, bar_chart
  subheader('Member Count Trends')
  bar_chart(
          data.groupby(['Stat Year'])[['Comm', 'Non Comm']].sum(),
          y = ['Comm', 'Non Comm']
        )
