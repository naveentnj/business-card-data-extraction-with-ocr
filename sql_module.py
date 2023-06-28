import mysql.connector
import pandas as pd
import creds

mydb = mysql.connector.connect(
  host="localhost",
  user=creds.bz_db_username,
  password=creds.bz_db_password,
  database="business_card_data",
  auth_plugin='mysql_native_password'
)

mycursor = mydb.cursor()

insert_sql = "INSERT INTO customers (name, address,number) VALUES (%s, %s, %s)"
#val =  return_data()

def add(val):
    j = 10
    for i in range(len(val)):
        j += 1
        #print(val[i])
        val[i] = list(val[i])
        val[i].append(j)
    
    mycursor.executemany(insert_sql, val)

    mydb.commit()

    row_count = mycursor.rowcount

    insert_id = mycursor.lastrowid

    return [row_count, insert_id]

def view(rows):
    mycursor.execute("SELECT * FROM customers")
    result = mycursor.fetchall()
    df = pd.DataFrame(result, columns=['name', 'address', 'number'])
    return df
