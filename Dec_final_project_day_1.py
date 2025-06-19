#Database connection details
import mysql.connector

conn_obj=mysql.connector.connect(
    host="localhost",
    user="root",
    password="R@jdeep123",
    database="python_mysql_final_project_day_1")
cur_obj=conn_obj.cursor()

#Define function data_entry_sql
def data_entry_sql(cust_name,cust_address,cust_ph_no,cust_user_id,cust_password):

    # Build the query with user-provided name using LIKE operator
    sql = "INSERT INTO customer_details (cust_full_name, cust_address, cust_phone_number, cust_user_name, cust_password) VALUES (%s, %s, %s, %s, %s)"
    data = (cust_name,cust_address,cust_ph_no,cust_user_id,cust_password)

    try:
        cur_obj.execute(sql, data)
        print("Customer details entry successful...")
        conn_obj.commit()
    except mysql.connector.Error as e:
        print("Error retrieving data from MySQL:", e)
        conn_obj.rollback()

#Define function data_retrieve
def data_retrieve(cust_user_id):
    query = f"select * from customer_details WHERE cust_user_name=\'{cust_user_id}\'"
    #print(query)

    try:
        cur_obj.execute(query)
        result = cur_obj.fetchone()
        conn_obj.commit()
    except mysql.connector.Error as e:
        print("Error retrieving data from MySQL:", e)
        conn_obj.rollback()
    #print(result)
    return result

def new_account_creation():
    cust_name = input("Please enter your full name-> ")
    cust_address = input("Please enter your full address-> ")
    cust_ph_no = input("Please enter your phone number-> ")
    cust_user_id = input("Please enter your user id-> ")
    cust_password = input("Please enter your password-> ")
    data_entry_sql(cust_name, cust_address, cust_ph_no, cust_user_id, cust_password)

cust_choice=input("PLease select 1 to create your account\nPlease select 2 to login to your account-> ")
if cust_choice=='1':
    new_account_creation()
elif cust_choice=='2':
    cust_user_id=input("Please enter your user id-> ")
    cust_password=input("Please enter your password-> ")
    retust_from_db=data_retrieve(cust_user_id)
    if retust_from_db:
        if cust_password==retust_from_db[-1]:
            print("Login successful")
        else:
            print("Login failed.")
        pass # userid already exist in the table
    else:
        print("Hope you are new user, please create your account...")
        new_account_creation()
else:
    print("wrong choice, pls try again...")
conn_obj.close()