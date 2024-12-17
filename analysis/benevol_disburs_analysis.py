def benevol_disburs_analysis(data):
  import streamlit as st
  st.subheader('Benevolent Disbursments Trends')

  total_col, pct_col = st.columns(2)

  with total_col:
    st.write('Total Benevolent Disbursments')
    st.bar_chart(
            data.groupby(['Stat Year'])['Total Benevolent Disbursements'].sum(),
            y = 'Total Benevolent Disbursements'
          )
  with pct_col:
    st.write('Total Benevolent Disbursments as Pct of All Disbursments')
    st.bar_chart(
            data.groupby(['Stat Year'])['Benevol Grand Total'].sum(),
            y = 'Benevol Grand Total'
          )
    
  gam = ['Administration', 'Discipleship Min', 'Mission To Namerica', 
          'Mission To The World', 'Covenant College', 'Covenant Seminary', 'Ridge Haven',
          'Reformed University Ministries', 'Pca Office Building', 'Other']

  st.write('General Assembly Ministries')
  st.bar_chart(
            data.groupby(['Stat Year'])[gam].sum(),
            y = gam
          )

  pm = ['Presbytery Operation', 'Christian Education', 'Home Missions', 'International Missions', 'Other Presbytery Min']

  st.write('Presbytery Ministries')
  st.bar_chart(
            data.groupby(['Stat Year'])[pm].sum(),
            y = pm
          )

  cm = ['Local Ministries', 'Mercy Ministires', 'Pca International Missions', 'Pca Home Mission', 'Nonpca Mission', 'Pca Schools', 'Nonpca Schools']

  st.write('Congregational Ministries')
  st.bar_chart(
            data.groupby(['Stat Year'])[cm].sum(),
            y = cm
          )

