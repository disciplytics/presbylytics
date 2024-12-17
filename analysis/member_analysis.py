def member_analysis():
  st.subheader('Member Count Trends')
  st.bar_chart(
          filtered_df.groupby(['Stat Year'])[['Comm', 'Non Comm']].sum(),
          y = ['Comm', 'Non Comm']
        )
