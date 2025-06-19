#Database connection details
import mysql.connector
import QR_CODE_SCANNER

conn_obj=mysql.connector.connect(
    host="localhost",
    user="root",
    password="R@jdeep123",
    database="jan_final_project_2025")
cur_obj=conn_obj.cursor()

#Define function data_entry_sql
def data_entry_sql(cust_name,cust_address,ph_no):

    # Build the query with user-provided name using LIKE operator
    sql = "INSERT INTO cust_details (cust_name, cust_address, cust_phone_number) VALUES (%s, %s, %s)"
    data = (cust_name,cust_address,ph_no)

    try:
        cur_obj.execute(sql, data)
        print("NEW CUSTOMER ENTRY SUCCESSFUL.")
        conn_obj.commit()
    except mysql.connector.Error as e:
        print("Error retrieving data from MySQL:", e)
        conn_obj.rollback()

#Define function data_retrieve
def data_retrieve(ph_no):
    query = f"select * from cust_details WHERE cust_phone_number={ph_no}"

    try:
        cur_obj.execute(query)
        result = cur_obj.fetchone()
        conn_obj.commit()
    except mysql.connector.Error as e:
        print("Error retrieving data from MySQL:", e)
        conn_obj.rollback()
    return result

def data_retrieve_from_product_table(p_id):
    query = f"select * from product_table WHERE p_id={p_id}"

    try:
        cur_obj.execute(query)
        result = cur_obj.fetchone()
        conn_obj.commit()
    except mysql.connector.Error as e:
        print("Error retrieving data from MySQL:", e)
        conn_obj.rollback()
    return result
def data_entry_audit_table(total_bill_amount, customer_id, customer_name):
    sql = "INSERT INTO audit_table (total_bill_amount, customer_id, customer_name) VALUES (%s, %s, %s)"
    data = (total_bill_amount, customer_id, customer_name)

    try:
        cur_obj.execute(sql, data)
        print("Bill value noted to database., Billing completed")
        conn_obj.commit()
    except mysql.connector.Error as e:
        print("Error inserting the data to MySQL:", e)
        conn_obj.rollback()
def billing_opreation(result_from_db):
    #print(result_from_db)
    total_bill_amount=0
    while True:
        #p_id=input("Please enter product id->")
        product_details_list=QR_CODE_SCANNER.qr_code_scanner().split("-")
        p_id=int(product_details_list[0])
        product_details_from_db=data_retrieve_from_product_table(p_id)
        print(product_details_from_db)
        p_quantity=int(input("Please enter product quantity->"))
        bill_amount=p_quantity*product_details_from_db[2]
        total_bill_amount=total_bill_amount+bill_amount
        res=input("Please enter S or s to stop the billing, enter any other value to continue->")
        if res=='S' or res=='s':
            break
    print(total_bill_amount)
    data_entry_audit_table(total_bill_amount,result_from_db[0],result_from_db[1])
#main logic starts here
ph_no=input("Please enter phone number-> ")
result_from_db=data_retrieve(ph_no)
#print(result_from_db)
if result_from_db:
    billing_opreation(result_from_db)
else:
    cust_name=input("Please enter customer name->")
    cust_address = input("Please enter customer address->")
    data_entry_sql(cust_name,cust_address,ph_no)
    result_from_db = data_retrieve(ph_no)
    billing_opreation(result_from_db)
conn_obj.close()