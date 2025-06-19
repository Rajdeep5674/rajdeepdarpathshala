import tkinter as tk
from tkinter import messagebox
import mysql.connector

# -------- Database Connection --------
conn_obj = mysql.connector.connect(
    host="localhost",
    user="root",
    password="R@jdeep123",
    database="feb_project_2025"
)
cur_obj = conn_obj.cursor()

# -------- Data Entry Function --------
def data_entry_sql(full_name, address, ph_number, user_name, password):
    sql = "INSERT INTO cust_credentials (full_name, address, phone_number, user_name, password) VALUES (%s, %s, %s, %s, %s)"
    data = (full_name, address, ph_number, user_name, password)
    try:
        cur_obj.execute(sql, data)
        conn_obj.commit()
        return True
    except mysql.connector.Error as e:
        print("Error inserting data to MySQL:", e)
        conn_obj.rollback()
        return False

# -------- Data Retrieval Function --------
def data_retrieve(cust_user_name):
    query = f"SELECT * FROM cust_credentials WHERE user_name = %s"
    try:
        cur_obj.execute(query, (cust_user_name,))
        result = cur_obj.fetchone()
        return result
    except mysql.connector.Error as e:
        print("Error retrieving data:", e)
        return None

# -------- GUI Functions --------
def register_user():
    full_name = entry_full_name.get()
    address = entry_address.get()
    phone = entry_phone.get()
    user = entry_username.get()
    password = entry_password.get()

    if full_name and address and phone and user and password:
        success = data_entry_sql(full_name, address, phone, user, password)
        if success:
            messagebox.showinfo("Success", "Registration Successful!")
            register_window.destroy()
        else:
            messagebox.showerror("Error", "Registration Failed. Try a different username.")
    else:
        messagebox.showwarning("Input Error", "All fields are required.")

def login_user():
    user = login_username.get()
    password = login_password.get()
    result = data_retrieve(user)

    if result:
        if result[-1] == password:
            messagebox.showinfo("Login", "Login Successful!")
        else:
            messagebox.showerror("Login Failed", "Incorrect password.")
    else:
        res = messagebox.askyesno("User Not Found", "User not found. Would you like to register?")
        if res:
            open_register_window()

def open_register_window():
    global register_window
    global entry_full_name, entry_address, entry_phone, entry_username, entry_password

    register_window = tk.Toplevel(root)
    register_window.title("Register New User")
    register_window.geometry("400x400")
    register_window.configure(bg="#e6f2ff")

    tk.Label(register_window, text="Full Name:", bg="#e6f2ff", font=('Arial', 12)).pack(pady=5)
    entry_full_name = tk.Entry(register_window, width=30)
    entry_full_name.pack()

    tk.Label(register_window, text="Address:", bg="#e6f2ff", font=('Arial', 12)).pack(pady=5)
    entry_address = tk.Entry(register_window, width=30)
    entry_address.pack()

    tk.Label(register_window, text="Phone Number:", bg="#e6f2ff", font=('Arial', 12)).pack(pady=5)
    entry_phone = tk.Entry(register_window, width=30)
    entry_phone.pack()

    tk.Label(register_window, text="Username:", bg="#e6f2ff", font=('Arial', 12)).pack(pady=5)
    entry_username = tk.Entry(register_window, width=30)
    entry_username.pack()

    tk.Label(register_window, text="Password:", bg="#e6f2ff", font=('Arial', 12)).pack(pady=5)
    entry_password = tk.Entry(register_window, show="*", width=30)
    entry_password.pack()

    tk.Button(register_window, text="Register", command=register_user, bg="#4da6ff", fg="white", font=('Arial', 12), padx=10, pady=5).pack(pady=20)

# -------- Main Window --------
root = tk.Tk()
root.title("Customer Login System")
root.geometry("400x300")
root.configure(bg="#cce6ff")

tk.Label(root, text="Login", font=('Arial', 16, 'bold'), bg="#cce6ff").pack(pady=10)

tk.Label(root, text="Username:", bg="#cce6ff", font=('Arial', 12)).pack(pady=5)
login_username = tk.Entry(root, width=30)
login_username.pack()

tk.Label(root, text="Password:", bg="#cce6ff", font=('Arial', 12)).pack(pady=5)
login_password = tk.Entry(root, show="*", width=30)
login_password.pack()

tk.Button(root, text="Login", command=login_user, bg="#4da6ff", fg="white", font=('Arial', 12), padx=10, pady=5).pack(pady=10)
tk.Button(root, text="Register", command=open_register_window, bg="#00b386", fg="white", font=('Arial', 12), padx=10, pady=5).pack()

root.mainloop()

# -------- Close connection on exit --------
conn_obj.close()