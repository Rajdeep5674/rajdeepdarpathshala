#Database connection details
import mysql.connector

conn_obj=mysql.connector.connect(
    host="localhost",
    user="root",
    password="R@jdeep123",
    database="feb_project_2025")
cur_obj=conn_obj.cursor()

#Define function data_entry_sql
def data_entry_sql(full_name,address,ph_number,user_name,password):

    # Build the query with user-provided name using LIKE operator
    sql = "INSERT INTO cust_credentials (full_name, address, phone_number, user_name, password) VALUES (%s, %s, %s, %s, %s)"
    data = (full_name,address,ph_number,user_name,password)

    try:
        cur_obj.execute(sql, data)
        print("New user registration successful.")
        conn_obj.commit()
    except mysql.connector.Error as e:
        print("Error inserting data to MySQL:", e)
        conn_obj.rollback()

#Define function data_retrieve
def data_retrieve(cust_user_name):
    query = f"select * from cust_credentials WHERE user_name=\'{cust_user_name}\'"
    #print(query)
    try:
        cur_obj.execute(query)
        result = cur_obj.fetchone()
        conn_obj.commit()
    except mysql.connector.Error as e:
        print("Error retrieving data from MySQL:", e)
        conn_obj.rollback()
    return result
def registration():
    full_name=input("Please enter your full name-> ")
    address = input("Please enter your full address-> ")
    ph_number = input("Please enter your phone number -> ")
    user_name = input("Please enter your user name->")
    password= input("Please enter your password-> ")
    data_entry_sql(full_name,address,ph_number,user_name,password)
#main logic
res=input("option 1 -> New user registration\nopetion 2 -> Existing user login\n type here-> ")
if res=='1':
    registration()
elif res=='2':
    cust_user_name = input("Please enter your user name->")
    cust_password= input("Please enter your password-> ")
    result_from_db=data_retrieve(cust_user_name)
    if result_from_db:
        if result_from_db[-1]==cust_password:
            print("login success")
        else:
            print("access denined")
    else:
        print("user is new, you need to register yourself first")
        registration()
else:
    print("wrong choice...")
conn_obj.close()