# Util functions for the app

def snowflake_connection(sql):
  # connect and load from snowflake
  from streamlit import connection
  conn = connection("snowflake")
  return conn.query(sql, ttl=0)
