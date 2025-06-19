import mysql.connector
import QR_CODE_SCANNER

conn_obj=mysql.connector.connect(
    host="localhost",
    user="root",
    password="R@jdeep123",
    database="mysql_project_segment_nov_2024_final_project")
cur_obj=conn_obj.cursor()

#Define function data_entry_sql
def data_entry_sql(c_name,c_address,cust_ph_no):

    sql = "INSERT INTO cust_details (c_name, c_address, c_phone_number) VALUES (%s, %s, %s)"
    data = (c_name,c_address,cust_ph_no)

    try:
        cur_obj.execute(sql, data)
        print("New customer entry successful...")
        conn_obj.commit()
    except mysql.connector.Error as e:
        print("Error retrieving data from MySQL:", e)
        conn_obj.rollback()

#Define function data_retrieve
def data_retrieve(cust_ph_no):
    query = f"select * from cust_details WHERE c_phone_number=\'{cust_ph_no}\'"

    try:
        cur_obj.execute(query)
        result = cur_obj.fetchone()
        conn_obj.commit()
    except mysql.connector.Error as e:
        print("Error retrieving data from MySQL:", e)
        conn_obj.rollback()
    return result

def retrive_from_inventory(p_id_from_cachier):
    query = f"select * from inventory WHERE p_id={p_id_from_cachier}"

    try:
        cur_obj.execute(query)
        result = cur_obj.fetchone()
        conn_obj.commit()
    except mysql.connector.Error as e:
        print("Error retrieving data from MySQL:", e)
        conn_obj.rollback()
    return result

def data_entry_analytics_table(c_id,c_name,total_bill_amount):

    sql = "INSERT INTO analytics_table (c_id, c_name, total_bill_amount) VALUES (%s, %s, %s)"
    data = (c_id,c_name,total_bill_amount)

    try:
        cur_obj.execute(sql, data)
        print("Sale data entry successful...")
        conn_obj.commit()
    except mysql.connector.Error as e:
        print("Error retrieving data from MySQL:", e)
        conn_obj.rollback()

cust_ph_no=input("Please enter your phone number- ")
result_from_db=data_retrieve(cust_ph_no)
if result_from_db:
    total_bill_amount=0
    while True:
        #p_id_from_cashier=int(input("Please enter product id- "))
        ouput_from_qr_code_scanner=QR_CODE_SCANNER.qr_code_scanner()
        p_id_from_cashier=ouput_from_qr_code_scanner.split('-')[0]
        print(ouput_from_qr_code_scanner)
        details_from_inventory=retrive_from_inventory(p_id_from_cashier)
        product_price=details_from_inventory[2]
        P_quantity_from_cashier=int(input("Please enter the quantity value- "))
        bill_amount=product_price*P_quantity_from_cashier
        response=input("Please enter C or c to go to next item-> ").lower()
        total_bill_amount=total_bill_amount+bill_amount
        if response!='c':
            break
    print(total_bill_amount)
    data_entry_analytics_table(result_from_db[0],result_from_db[1],total_bill_amount)
else:
    c_name=input("Please enter customer full name- ")
    c_address=input("Please enter customer address- ")
    data_entry_sql(c_name,c_address,cust_ph_no)
conn_obj.close()