import tkinter as tk
from tkinter import messagebox
import mysql.connector
import QR_CODE_SCANNER

# --- MySQL Connection ---
conn_obj = mysql.connector.connect(
    host="localhost",
    user="root",
    password="R@jdeep123",
    database="mysql_project_segment_nov_2024_final_project"
)
cur_obj = conn_obj.cursor()


# --- MySQL Logic Functions ---
def data_entry_sql(c_name, c_address, cust_ph_no):
    sql = "INSERT INTO cust_details (c_name, c_address, c_phone_number) VALUES (%s, %s, %s)"
    try:
        cur_obj.execute(sql, (c_name, c_address, cust_ph_no))
        conn_obj.commit()
        messagebox.showinfo("Success", "New customer added!")
    except mysql.connector.Error as e:
        conn_obj.rollback()
        messagebox.showerror("Database Error", str(e))


def data_retrieve(cust_ph_no):
    query = f"SELECT * FROM cust_details WHERE c_phone_number='{cust_ph_no}'"
    try:
        cur_obj.execute(query)
        result = cur_obj.fetchone()
        conn_obj.commit()
        return result
    except mysql.connector.Error as e:
        conn_obj.rollback()
        messagebox.showerror("Database Error", str(e))
        return None


def retrive_from_inventory(p_id):
    query = f"SELECT * FROM inventory WHERE p_id={p_id}"
    try:
        cur_obj.execute(query)
        result = cur_obj.fetchone()
        conn_obj.commit()
        return result
    except mysql.connector.Error as e:
        conn_obj.rollback()
        messagebox.showerror("Database Error", str(e))
        return None


def data_entry_analytics_table(c_id, c_name, total_bill_amount):
    sql = "INSERT INTO analytics_table (c_id, c_name, total_bill_amount) VALUES (%s, %s, %s)"
    try:
        cur_obj.execute(sql, (c_id, c_name, total_bill_amount))
        conn_obj.commit()
        messagebox.showinfo("Success", f"Billing done! Total: ₹{total_bill_amount}")
    except mysql.connector.Error as e:
        conn_obj.rollback()
        messagebox.showerror("Database Error", str(e))


# --- GUI Logic ---
def search_customer():
    global current_customer, total_bill
    ph_no = phone_entry.get().strip()
    result = data_retrieve(ph_no)
    total_bill = 0
    bill_listbox.delete(0, tk.END)
    total_label.config(text="Total: ₹0.00")

    if result:
        current_customer = result
        name_display.config(text=f"Welcome {result[1]}")
        billing_frame.pack(pady=10)
    else:
        register_frame.pack(pady=10)


def register_customer():
    c_name = name_entry.get().strip()
    c_address = address_entry.get().strip()
    ph_no = phone_entry.get().strip()
    if c_name and c_address:
        data_entry_sql(c_name, c_address, ph_no)
        register_frame.pack_forget()
        search_customer()
    else:
        messagebox.showwarning("Input Error", "Please fill in all fields.")


def scan_and_add_product():
    global total_bill
    qr_result = QR_CODE_SCANNER.qr_code_scanner()
    print(qr_result)
    try:
        p_id = qr_result.split('-')[0]
        print(p_id)
        product = retrive_from_inventory(int(p_id))
        print(product)
        if not product:
            return

        qty = int(quantity_entry.get())
        subtotal = float(product[2]) * qty
        total_bill += subtotal
        bill_listbox.insert(tk.END, f"{product[1]} (x{qty}) - ₹{subtotal:.2f}")
        total_label.config(text=f"Total: ₹{total_bill:.2f}")
    except Exception as e:
        messagebox.showerror("Error", f"Could not process product.\n{str(e)}")


def finalize_bill():
    if current_customer:
        data_entry_analytics_table(current_customer[0], current_customer[1], total_bill)
        billing_frame.pack_forget()
        reset_ui()


def reset_ui():
    phone_entry.delete(0, tk.END)
    name_display.config(text="")
    name_entry.delete(0, tk.END)
    address_entry.delete(0, tk.END)
    register_frame.pack_forget()


# --- GUI Setup ---
root = tk.Tk()
root.title("Smart Retail QR Billing")
root.geometry("650x700")
root.config(bg="#e8f5e9")

font_header = ("Helvetica", 20, "bold")
font_normal = ("Arial", 12)

current_customer = None
total_bill = 0

# Header
tk.Label(root, text="Smart Retail QR Billing", font=font_header, bg="#a5d6a7", fg="black", pady=10).pack(fill="x")

# Customer Phone Entry
search_frame = tk.Frame(root, bg="#e8f5e9")
search_frame.pack(pady=10)
tk.Label(search_frame, text="Enter Phone Number:", font=font_normal, bg="#e8f5e9").grid(row=0, column=0, padx=5)
phone_entry = tk.Entry(search_frame, font=font_normal)
phone_entry.grid(row=0, column=1, padx=5)
tk.Button(search_frame, text="Search", font=font_normal, command=search_customer, bg="#66bb6a", fg="white").grid(row=0,
                                                                                                                 column=2)

# Display Customer Name
name_display = tk.Label(root, text="", font=("Arial", 14, "bold"), bg="#e8f5e9", fg="green")
name_display.pack()

# Registration Frame
register_frame = tk.Frame(root, bg="#fff3e0", bd=2, relief="ridge")
tk.Label(register_frame, text="Register New Customer", font=("Arial", 14, "bold"), bg="#fff3e0").pack(pady=5)
tk.Label(register_frame, text="Full Name:", bg="#fff3e0").pack()
name_entry = tk.Entry(register_frame)
name_entry.pack(pady=2)
tk.Label(register_frame, text="Address:", bg="#fff3e0").pack()
address_entry = tk.Entry(register_frame)
address_entry.pack(pady=2)
tk.Button(register_frame, text="Register", bg="#fb8c00", fg="white", command=register_customer).pack(pady=5)

# Billing Frame
billing_frame = tk.Frame(root, bg="#e3f2fd", bd=2, relief="ridge")

tk.Label(billing_frame, text="Billing Area", font=("Arial", 14, "bold"), bg="#e3f2fd").pack(pady=5)

quantity_entry = tk.Entry(billing_frame)
quantity_entry.pack()
quantity_entry.insert(0, "Enter Quantity")

tk.Button(billing_frame, text="Scan QR and Add Product", command=scan_and_add_product, bg="#42a5f5", fg="white").pack(
    pady=5)

bill_listbox = tk.Listbox(billing_frame, width=50, font=("Courier", 10))
bill_listbox.pack(pady=5)

total_label = tk.Label(billing_frame, text="Total: ₹0.00", font=("Arial", 12), bg="#e3f2fd")
total_label.pack()

tk.Button(billing_frame, text="Finalize Bill", command=finalize_bill, bg="#2e7d32", fg="white").pack(pady=10)

root.mainloop()

# Close connection
conn_obj.close()
