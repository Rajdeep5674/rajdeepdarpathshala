import mysql.connector
import QR_CODE_SCANNER
import tkinter as tk
from tkinter import messagebox, ttk, simpledialog

# Database Connection
conn_obj = mysql.connector.connect(
    host="localhost",
    user="root",
    password="R@jdeep123",
    database="feb_final_python_2025"
)
cur_obj = conn_obj.cursor()

# --- Database Functions ---
def data_entry_sql(cust_name, cust_address, cust_ph_no):
    sql = "INSERT INTO cust_details (c_name, c_address, c_ph_no) VALUES (%s, %s, %s)"
    data = (cust_name, cust_address, cust_ph_no)
    try:
        cur_obj.execute(sql, data)
        conn_obj.commit()
    except mysql.connector.Error as e:
        messagebox.showerror("Database Error", str(e))
        conn_obj.rollback()

def data_retrieve(cust_ph_no):
    query = f"SELECT * FROM cust_details WHERE c_ph_no={cust_ph_no}"
    try:
        cur_obj.execute(query)
        result = cur_obj.fetchone()
        conn_obj.commit()
        return result
    except mysql.connector.Error as e:
        messagebox.showerror("Database Error", str(e))
        conn_obj.rollback()

def data_retrieve_from_inventory(p_id):
    query = f"SELECT * FROM inventory WHERE p_id={p_id}"
    try:
        cur_obj.execute(query)
        result = cur_obj.fetchone()
        conn_obj.commit()
        return result
    except mysql.connector.Error as e:
        messagebox.showerror("Database Error", str(e))
        conn_obj.rollback()

def data_entry_analytics_table(c_id, c_name, c_address, total_bill_amount):
    sql = "INSERT INTO analytics_table (cust_id, cust_name, cust_address, total_bill_amount) VALUES (%s, %s, %s, %s)"
    data = (c_id, c_name, c_address, total_bill_amount)
    try:
        cur_obj.execute(sql, data)
        conn_obj.commit()
    except mysql.connector.Error as e:
        messagebox.showerror("Analytics Entry Error", str(e))
        conn_obj.rollback()

# --- GUI Billing System ---
class BillingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Supermarket Billing System")
        self.root.geometry("800x600")
        self.total_bill = 0
        self.customer_data = None

        # Customer Info
        tk.Label(root, text="Customer Phone:", font=("Arial", 14)).pack()
        self.ph_entry = tk.Entry(root, font=("Arial", 14))
        self.ph_entry.pack()
        tk.Button(root, text="Search Customer", command=self.search_customer, font=("Arial", 12), bg="blue", fg="white").pack(pady=10)

        # Treeview for Bill
        self.tree = ttk.Treeview(root, columns=("Product", "Price", "Qty", "Total"), show='headings')
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        # Buttons
        tk.Button(root, text="Scan Product", command=self.scan_product, font=("Arial", 12), bg="green", fg="white").pack(pady=5)
        tk.Button(root, text="Finalize Bill", command=self.finalize_bill, font=("Arial", 12), bg="red", fg="white").pack(pady=5)

    def search_customer(self):
        ph_no = self.ph_entry.get()
        if not ph_no.isdigit():
            messagebox.showerror("Error", "Invalid phone number")
            return
        result = data_retrieve(ph_no)
        if result:
            self.customer_data = result
            messagebox.showinfo("Success", f"Welcome back, {result[1]}")
        else:
            name = simpledialog.askstring("New Customer", "Enter Name:")
            address = simpledialog.askstring("New Customer", "Enter Address:")
            data_entry_sql(name, address, ph_no)
            self.customer_data = data_retrieve(ph_no)
            messagebox.showinfo("Registered", f"New customer {name} added!")

    def scan_product(self):
        if not self.customer_data:
            messagebox.showerror("Error", "Search or register customer first")
            return
        try:
            product_info = QR_CODE_SCANNER.qr_code_scanner()
            p_id = int(product_info.split('-')[0])
            product_details = data_retrieve_from_inventory(p_id)
            if not product_details:
                messagebox.showerror("Error", "Product not found")
                return
            quantity = simpledialog.askinteger("Quantity", f"Enter quantity for {product_details[1]}:", minvalue=1)
            total = product_details[2] * quantity
            self.total_bill += total
            self.tree.insert("", "end", values=(product_details[1], product_details[2], quantity, total))
        except Exception as e:
            messagebox.showerror("QR Error", str(e))

    def finalize_bill(self):
        if self.total_bill == 0:
            messagebox.showerror("Empty Bill", "No items billed.")
            return
        data_entry_analytics_table(self.customer_data[0], self.customer_data[1], self.customer_data[2], self.total_bill)
        messagebox.showinfo("Billing Complete", f"Total Bill: ₹{self.total_bill}")
        self.root.quit()

# --- Run the App ---
if __name__ == "__main__":
    root = tk.Tk()
    app = BillingApp(root)
    root.mainloop()
    conn_obj.close()