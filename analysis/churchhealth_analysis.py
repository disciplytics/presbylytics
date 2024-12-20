def churchhealth_analysis(data):
  import streamlit as st
  st.subheader('Church Health')

  st.subheader('Members & Family Health')
  st.write('Deacon and Elder Allocation')
  data['Total Members'] = data['Comm'] + data['Non Comm']


  deacon_members_col, elder_members_col = st.columns(2)
  # calc deacon per member
  dpm = data.groupby(['Stat Year'])[['Deacons', 'Comm', 'Non Comm']].sum().reset_index()
  dpm = dpm.groupby(['Stat Year']).apply(lambda x: x['Deacons'] / (x['Non Comm'] + x['Comm'])).reset_index(name='Deacons Per Member')

  # calc elders per member
  epm = data.groupby(['Stat Year'])[['Ruling Elders', 'Comm', 'Non Comm']].sum().reset_index()
  epm = epm.groupby(['Stat Year']).apply(lambda x: x['Ruling Elders'] / (x['Non Comm'] + x['Comm'])).reset_index(name='Ruling Elders Per Member')
  
  with deacon_members_col:
    st.write('Deacons Per Member: (Comm + Non Comm)')
    st.bar_chart(
            dpm,
            x = 'Stat Year',
            y = 'Deacons Per Member'
          )
    
  with elder_members_col:
    st.write('Ruling Elders Per Member: (Comm + Non Comm)')
    st.bar_chart(
            epm,
            y = 'Ruling Elders Per Member',
            x = 'Stat Year'
          )

  deacon_famunit_col, elder_famunits_col = st.columns(2)
  # calc deacon per member
  dpf = data.groupby(['Stat Year'])[['Deacons', 'Family Units']].sum().reset_index()
  dpf = dpf.groupby(['Stat Year']).apply(lambda x: x['Deacons'] / x['Family Units']).reset_index(name='Deacons Per Family Unit')

  # calc elders per member
  epf = data.groupby(['Stat Year'])[['Ruling Elders', 'Family Units']].sum().reset_index()
  epf = epf.groupby(['Stat Year']).apply(lambda x: x['Ruling Elders'] / x['Family Units']).reset_index(name='Ruling Elders Per Family Unit')
  
  with deacon_famunit_col:
    st.write('Deacons Per Family Unit')
    st.bar_chart(
            dpf,
            x = 'Stat Year',
            y = 'Deacons Per Family Unit'
          )
    
  with elder_famunits_col:
    st.write('Ruling Elders Per Family Unit')
    st.bar_chart(
            epf,
            y = 'Ruling Elders Per Family Unit',
            x = 'Stat Year'
          )

  
  

  st.subheader('Giving, Disbursements, & Expenses Metrics')
  data['Benevolent Disbursements Per Capita'] = data['Total Benevolent Disbursements'] / data['Comm']
  data['Congregational Expenses Per Capita'] = (data['Current Expenses'] +  data['Building Fund']) / data['Comm']

  # calc giving per capita
  gpc = data.groupby(['Stat Year'])[['Total Contrib', 'Comm']].sum().reset_index()
  gpc = gpc.groupby(['Stat Year']).apply(lambda x: x['Total Contrib'] / x['Comm']).reset_index(name='Giving Per Capita')

   # calc Benevolent per capita
  bpc = data.groupby(['Stat Year'])[['Total Benevolent Disbursements', 'Comm']].sum().reset_index()
  bpc = bpc.groupby(['Stat Year']).apply(lambda x: x['Total Benevolent Disbursements'] / x['Comm']).reset_index(name='Benevolent Disbursements Per Capita')

  # calc Congregational per capita
  epc = data.groupby(['Stat Year'])[['Current Expenses', 'Building Fund', 'Comm']].sum().reset_index()
  epc = epc.groupby(['Stat Year']).apply(lambda x: (x['Current Expenses'] + x['Building Fund']) / x['Comm']).reset_index(name='Congregational Expenses Per Capita')
  
  st.write('Giving Per Capita')
  st.bar_chart(
            gpc,
            y = 'Giving Per Capita',
            x = 'Stat Year'
          )
  
  bpc_col, epc_col = st.columns(2)
  with bpc_col:
    st.write('Benevolent Disbursements Per Capita: Total Benevolent Disbursements / Comm')
    st.bar_chart(
            bpc,
            y = 'Benevolent Disbursements Per Capita',
            x = 'Stat Year'
          )
  with epc_col:
    st.write('Congregational Expenses Per Capita: (Current Expenses + Building Fund) / Comm')
    st.bar_chart(
            epc,
            y = 'Congregational Expenses Per Capita',
            x = 'Stat Year'
          )
