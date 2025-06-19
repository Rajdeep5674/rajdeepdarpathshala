import mysql.connector
import QR_CODE_SCANNER
import tkinter as tk
from tkinter import messagebox, simpledialog
from tkinter import ttk

# Database connection
conn_obj = mysql.connector.connect(
    host="localhost",
    user="root",
    password="R@jdeep123",
    database="jan_final_project_2025"
)
cur_obj = conn_obj.cursor()

# Backend Functions
def data_entry_sql(cust_name, cust_address, ph_no):
    sql = "INSERT INTO cust_details (cust_name, cust_address, cust_phone_number) VALUES (%s, %s, %s)"
    data = (cust_name, cust_address, ph_no)
    try:
        cur_obj.execute(sql, data)
        conn_obj.commit()
    except mysql.connector.Error as e:
        messagebox.showerror("Database Error", str(e))
        conn_obj.rollback()

def data_retrieve(ph_no):
    query = f"SELECT * FROM cust_details WHERE cust_phone_number={ph_no}"
    try:
        cur_obj.execute(query)
        result = cur_obj.fetchone()
        conn_obj.commit()
        return result
    except mysql.connector.Error as e:
        messagebox.showerror("Database Error", str(e))
        conn_obj.rollback()
        return None

def data_retrieve_from_product_table(p_id):
    query = f"SELECT * FROM product_table WHERE p_id={p_id}"
    try:
        cur_obj.execute(query)
        result = cur_obj.fetchone()
        conn_obj.commit()
        return result
    except mysql.connector.Error as e:
        messagebox.showerror("Database Error", str(e))
        conn_obj.rollback()
        return None

def data_entry_audit_table(total_bill_amount, customer_id, customer_name):
    sql = "INSERT INTO audit_table (total_bill_amount, customer_id, customer_name) VALUES (%s, %s, %s)"
    data = (total_bill_amount, customer_id, customer_name)
    try:
        cur_obj.execute(sql, data)
        conn_obj.commit()
        messagebox.showinfo("Billing Complete", "Billing completed and saved.")
    except mysql.connector.Error as e:
        messagebox.showerror("Database Error", str(e))
        conn_obj.rollback()

# Tkinter GUI
class SupermarketApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Supermarket Billing System")
        self.geometry("800x600")
        self.configure(bg="#f0f4f7")

        self.total_bill_amount = 0
        self.customer_data = None

        self.create_widgets()

    def create_widgets(self):
        # Title
        tk.Label(self, text="Supermarket Billing System", font=("Arial", 24, "bold"), bg="#f0f4f7", fg="#333").pack(pady=20)

        # Phone Number Entry
        frame = tk.Frame(self, bg="#f0f4f7")
        frame.pack()

        tk.Label(frame, text="Enter Phone Number:", font=("Arial", 14), bg="#f0f4f7").grid(row=0, column=0, padx=10)
        self.phone_entry = tk.Entry(frame, font=("Arial", 14))
        self.phone_entry.grid(row=0, column=1)

        tk.Button(frame, text="Search", command=self.search_customer, bg="#4CAF50", fg="white", font=("Arial", 12)).grid(row=0, column=2, padx=10)

        # Billing Area
        self.bill_text = tk.Text(self, height=20, width=90, bg="white", fg="black", font=("Courier", 12))
        self.bill_text.pack(pady=20)

        # Finalize Button
        tk.Button(self, text="Finalize Bill", command=self.finalize_billing, bg="#2196F3", fg="white", font=("Arial", 14, "bold")).pack()

    def search_customer(self):
        ph_no = self.phone_entry.get()
        if not ph_no.isdigit():
            messagebox.showwarning("Invalid Input", "Phone number must be numeric.")
            return

        self.customer_data = data_retrieve(ph_no)
        if not self.customer_data:
            # New Customer
            cust_name = simpledialog.askstring("New Customer", "Enter customer name:")
            cust_address = simpledialog.askstring("New Customer", "Enter customer address:")
            data_entry_sql(cust_name, cust_address, ph_no)
            self.customer_data = data_retrieve(ph_no)

        # Start billing
        self.start_billing()

    def start_billing(self):
        while True:
            qr_data = QR_CODE_SCANNER.qr_code_scanner()
            product_info = qr_data.split("-")
            p_id = int(product_info[0])
            product_data = data_retrieve_from_product_table(p_id)

            if not product_data:
                messagebox.showerror("Product Error", f"No product found for ID: {p_id}")
                return

            quantity = simpledialog.askinteger("Quantity", f"Enter quantity for {product_data[1]}:")
            bill = quantity * product_data[2]
            self.total_bill_amount += bill

            # Display in billing area
            self.bill_text.insert(tk.END, f"{product_data[1]} - ₹{product_data[2]} x {quantity} = ₹{bill}\n")

            stop = messagebox.askyesno("Continue?", "Do you want to scan more products?")
            if not stop:
                break

    def finalize_billing(self):
        if self.total_bill_amount == 0:
            messagebox.showwarning("No Items", "No products added to the bill.")
            return
        data_entry_audit_table(self.total_bill_amount, self.customer_data[0], self.customer_data[1])
        self.bill_text.insert(tk.END, f"\nTOTAL BILL: ₹{self.total_bill_amount}\n")
        self.total_bill_amount = 0

# Run the App
if __name__ == "__main__":
    app = SupermarketApp()
    app.mainloop()
    conn_obj.close()