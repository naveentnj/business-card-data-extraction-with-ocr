import mysql.connector
import pandas as pd
import creds

mydb = mysql.connector.connect(
  host="localhost",
  user=creds.bz_db_username,
  password=creds.bz_db_password,
  database="business_card_data",
  auth_plugin="mysql_native_password"
)

mycursor = mydb.cursor()

insert_sql = r"""INSERT INTO business_card_data (website_url, email, pin_code, phone_numbers, 
            address, card_holder_details, businesscard_photo) VALUES (%s, %s, %s, %s, %s, %s, %s)"""
#val =  return_data()

def add(val):
    
    mycursor.execute(insert_sql, val)

    mydb.commit()


def getRowsID():
    mycursor.execute("SELECT id FROM business_card_data")
    rows = mycursor.fetchall()
    return rows

def fetchRow(id):
    mycursor.execute("SELECT * FROM business_card_data WHERE id ="+str(id))
    row = mycursor.fetchone()
    return row

def fetchRecordImage(id):
     mycursor.execute("SELECT businesscard_photo FROM business_card_data WHERE id ="+str(id))
     rowImage = mycursor.fetchone()
     return rowImage


