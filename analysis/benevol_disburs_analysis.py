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
    # calc giving per capita
    pct_data = data.groupby(['Stat Year'])[['Total Benevolent Disbursements', 'Total All Disbursements']].sum().reset_index()
    pct_data = pct_data.groupby(['Stat Year']).apply(lambda x: x['Total Benevolent Disbursements'] / x['Total All Disbursements']).reset_index(name='Benevol Grand Total %')
    st.write('Total Benevolent Disbursments as Pct of All Disbursments')
    st.bar_chart(
            pct_data,
            y = 'Benevol Grand Total %',
            x = 'Stat Year'
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

