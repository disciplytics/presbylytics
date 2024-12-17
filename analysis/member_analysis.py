def member_analysis():
  from streamlit import subheader, bar_chart
  subheader('Member Count Trends')
  bar_chart(
          filtered_df.groupby(['Stat Year'])[['Comm', 'Non Comm']].sum(),
          y = ['Comm', 'Non Comm']
        )
