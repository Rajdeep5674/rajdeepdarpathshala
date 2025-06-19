import mysql.connector

conn_obj=mysql.connector.connect(
    host="localhost",
    user="root",
    password="R@jdeep123",
    database="final_project_dec_2024")
cur_obj=conn_obj.cursor()
print("testing")
print("another testing")
#Define function data_entry_sql
def data_entry_sql(ph_no,name,address):
    sql = "INSERT INTO cust_basic_details (c_name, c_address, c_phone_number) VALUES (%s, %s, %s)"
    data = (name,address,ph_no)

    try:
        cur_obj.execute(sql, data)
        print("NEW CUSTOMER ENTRY SUCCESSFUL.")
        conn_obj.commit()
    except mysql.connector.Error as e:
        print("Error inserting data to MySQL:", e)
        conn_obj.rollback()

#Define function data_retrieve
def data_retrieve(ph_no):
    query = f"select * from cust_basic_details WHERE c_phone_number={ph_no}"

    try:
        cur_obj.execute(query)
        result = cur_obj.fetchone()
        conn_obj.commit()
    except mysql.connector.Error as e:
        print("Error retrieving data from MySQL:", e)
        conn_obj.rollback()

    return result

def inventory_search(p_id):
    query = f"select * from inventory WHERE p_id={p_id}"
    try:
        cur_obj.execute(query)
        result = cur_obj.fetchone()
        conn_obj.commit()
    except mysql.connector.Error as e:
        print("Error retrieving data from MySQL:", e)
        conn_obj.rollback()

    return result

def audit_table_entry(c_id, c_name, total_bill_amount):
    sql = "INSERT INTO audit (c_id, c_name, total_bill_amount) VALUES (%s, %s, %s)"
    data = (c_id, c_name, total_bill_amount)

    try:
        cur_obj.execute(sql, data)
        print("NEW BILL ENTRY SUCCESSFUL.")
        conn_obj.commit()
    except mysql.connector.Error as e:
        print("Error inserting data to MySQL:", e)
        conn_obj.rollback()
def billing_mechanism(result_from_db):
    total_bill_amount = 0
    while True:
        p_id = input("Please enter product id->")
        p_quantity = int(input("Plese enter product quantity-> "))
        result_from_inventory = inventory_search(p_id)
        bill_amount = float(result_from_inventory[2]) * p_quantity
        total_bill_amount = total_bill_amount + bill_amount
        res = input("Do you want to stop the billing ? enter s otherwise enter c to continue-> ")
        if res == 's' or res == 'S':
            break
        elif res == 'c' or res == 'C':
            continue
        else:
            print("wrong choice")
    print(total_bill_amount)
    audit_table_entry(result_from_db[0], result_from_db[1], total_bill_amount)
#main logic
ph_no=input("Please enter customer phone number-> ")
result_from_db=data_retrieve(ph_no)
if result_from_db:
    billing_mechanism(result_from_db)
else:
    name=input("Please enter customer name-> ")
    address=input("Please enter customer address-> ")
    data_entry_sql(ph_no,name,address)
    result_from_db = data_retrieve(ph_no)
    billing_mechanism(result_from_db)
#print(result_from_db)
conn_obj.close()