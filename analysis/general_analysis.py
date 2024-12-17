def general_analysis(data):
  import streamlit as st
  st.subheader('General Trends')

  bapt_col, off_col = st.columns(2)
  with bapt_col:
    st.write('Baptisms')
    st.bar_chart(
            data.groupby(['Stat Year'])[['Adult Bapt', 'Infant Bapt']].sum(),
            y = ['Adult Bapt', 'Infant Bapt']
          )
  with off_col:
    st.write('Officers')
    st.bar_chart(
            data.groupby(['Stat Year'])[['Ruling Elders', 'Deacons']].sum(),
            y = ['Ruling Elders', 'Deacons']
          )

  sun_att_col, smal_att_col = st.columns(2)
  with sun_att_col:
    st.write('Sunday Morning Attendance')
    st.bar_chart(
            data.groupby(['Stat Year'])[['Est Morn Attend', 'Sunday School Attend']].sum(),
            y = ['Est Morn Attend', 'Sunday School Attend']
          )
  with smal_att_col:
    st.write('Small Group Attendance')
    st.bar_chart(
            data.groupby(['Stat Year'])['Small Group Attend'].sum(),
            y = 'Small Group Attend'
          )

  st.subheader('School Enrollment')
  st.write('Key: P=Presch, K=Kindergarten, E=Elem, M=Middle, H=HighSch')
  st.bar_chart(
    data, y = 'Grades Included', x = 'Total Enrollment', horizontal = True, stack = False)








