import psycopg2



def connect_to_psql_db(db_name):
  """
  Connect to an already established PostgreSQL server named 'db_name'.
  """
  print(f"Connecting to database '{db_name}'... ", end="")
  try:
    conn = psycopg2.connect(dbname=db_name)
    print("SUCCESS")

    return conn

  except:
    print("FAIL")



def add_case_to_db(conn,case_num,date,facility,dept):
  """
  Add a record to the database.
  """
  print(f"Adding case {case_num} to database... ",end="")
  try:
    # open cursor to perform database operations
    cur = conn.cursor()

    # add a record to the database
    cur.execute("""
      INSERT INTO cases (case_num, case_date, facility, dept)
      VALUES (%s, %s, %s, %s);
      """,
      (case_num, date, facility, dept))
  
    conn.commit()
    cur.close()

    print("SUCCESS")
    
  except:
    print("FAIL")
  




