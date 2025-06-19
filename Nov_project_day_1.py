#Database connection details
import mysql.connector

conn_obj=mysql.connector.connect(
    host="localhost",
    user="root",
    password="R@jdeep123",
    database="nov_project_day_1")
cur_obj=conn_obj.cursor()

#Define function data_entry_sql
def data_entry_sql(full_name,address,ph_no,user_id,password):

    # Build the query with user-provided name using LIKE operator
    sql = "INSERT INTO cust_basic_details (full_name,address,ph_no,user_id,password) VALUES (%s, %s, %s, %s, %s)"
    data = (full_name,address,ph_no,user_id,password)

    try:
        cur_obj.execute(sql, data)
        print(full_name,",NEW CUSTOMER ENTRY SUCCESSFUL, NOW YOU CAN LOGIN FROM HOME PAGE.")
        conn_obj.commit()
    except mysql.connector.Error as e:
        print("Error retrieving data from MySQL:", e)
        conn_obj.rollback()

#Define function data_retrieve
def data_retrieve(user_id):
    query = f"select * from cust_basic_details WHERE user_id=\'{user_id}\'"
    try:
        cur_obj.execute(query)
        result = cur_obj.fetchone()
        conn_obj.commit()
    except mysql.connector.Error as e:
        print("Error retrieving data from MySQL:", e)
        conn_obj.rollback()
    if result:
        return result[-1]
    else:
        return 0

print("Welcome to our demo application- Please select below options- ")
response=input("Enter 'show' to open the menu option-  \n Enter 'stop' to close the menu option- ")
while response!='stop':
    user_choice=input("Press 1 for new user login \n Press 2 for existing user login-")
    if user_choice=='1':
        full_name=input("Please enter your full name- ")
        address=input("Please enter your address- ")
        ph_no=input("Please enter your phone number- ")
        user_id=input("Please set your user_id- ")
        password=input("Please set you password- ")
        data_entry_sql(full_name,address,ph_no,user_id,password)
    elif user_choice=='2':
        user_id=input("Please set your user_id- ")
        password=input("Please set you password- ")
        pwd_from_db=data_retrieve(user_id)
        if pwd_from_db!=0:
            if pwd_from_db==password:
                print("YOUR CAN LOGIN NOW....")
                break
            else:
                print("Access dined.Try again...")
        else:
            print("RECORD NOT FOUND IN OUR DATABASE, PLEASE SELECT OPTION 1 TO CONTINUE...")
            continue
    else:
        print("Wrong choice.Try again...")
conn_obj.close()