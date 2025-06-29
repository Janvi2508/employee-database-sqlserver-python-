import tkinter as tk
from tkinter import messagebox, ttk, filedialog
import pyodbc
import pandas as pd

# SQL Server config
server_ip = '20.192.43.161'
server = 'companydbserver.database.windows.net'
database = 'CompanyDB'
username = 'Janvi_sharma'
password = 'Mukul@2530'
driver = '{ODBC Driver 17 for SQL Server}'

# Global data holder
df_data = pd.DataFrame()

def fetch_data():
    global df_data
    try:
        conn_str = (
            f'DRIVER={driver};'
            f'SERVER={server};'
            f'DATABASE={database};'
            f'UID={username};'
            f'PWD={password}'
        )
        conn = pyodbc.connect(conn_str)

        query = "SELECT TOP 5 * FROM Employees"
        df_data = pd.read_sql(query, conn)
        conn.close()

        update_treeview(df_data)
        update_department_filter()
        status_label.config(text=f"✅ Connected to SQL Server at IP: {server_ip}", fg="green")

    except Exception as e:
        messagebox.showerror("Connection Error", f"❌ Failed to connect:\n{e}")
        status_label.config(text="❌ Connection failed.", fg="red")

def update_treeview(df):
    for row in tree.get_children():
        tree.delete(row)
    for _, row in df.iterrows():
        tree.insert("", "end", values=list(row))

def update_department_filter():
    departments = sorted(df_data['Department'].dropna().unique())
    department_menu['menu'].delete(0, 'end')
    department_var.set("All Departments")
    department_menu['menu'].add_command(label="All Departments", command=lambda: filter_by_department("All Departments"))
    for dept in departments:
        department_menu['menu'].add_command(label=dept, command=lambda d=dept: filter_by_department(d))

def filter_by_department(department):
    if department == "All Departments":
        update_treeview(df_data)
    else:
        filtered = df_data[df_data['Department'] == department]
        update_treeview(filtered)

def export_csv():
    if df_data.empty:
        messagebox.showinfo("No Data", "Please fetch data first.")
        return
    file = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
    if file:
        df_data.to_csv(file, index=False)
        messagebox.showinfo("Exported", f"Data exported to {file}")

def open_add_employee_popup():
    def submit_new_employee():
        name = name_entry.get().strip()
        age = age_entry.get().strip()
        dept = dept_entry.get().strip()
        salary = salary_entry.get().strip()
        if not name or not age or not dept or not salary:
            messagebox.showwarning("Missing Data", "Please fill all fields.")
            return
        try:
            conn_str = (
                f'DRIVER={driver};'
                f'SERVER={server};'
                f'DATABASE={database};'
                f'UID={username};'
                f'PWD={password}'
            )
            conn = pyodbc.connect(conn_str)
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO Employees (Name, Age, Department, Salary) VALUES (?, ?, ?, ?)",
                name, int(age), dept, float(salary)
            )
            conn.commit()
            conn.close()
            popup.destroy()
            fetch_data()
            messagebox.showinfo("Success", "New employee added.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add employee:\n{e}")

    popup = tk.Toplevel(root)
    popup.title("Add New Employee")
    popup.geometry("300x250")

    tk.Label(popup, text="Name:").pack(pady=5)
    name_entry = tk.Entry(popup)
    name_entry.pack()

    tk.Label(popup, text="Age:").pack(pady=5)
    age_entry = tk.Entry(popup)
    age_entry.pack()

    tk.Label(popup, text="Department:").pack(pady=5)
    dept_entry = tk.Entry(popup)
    dept_entry.pack()

    tk.Label(popup, text="Salary:").pack(pady=5)
    salary_entry = tk.Entry(popup)
    salary_entry.pack()

    tk.Button(popup, text="Submit", command=submit_new_employee, bg="#28A745", fg="white").pack(pady=10)

# Main window
root = tk.Tk()
root.title("Employee Database Viewer")
root.geometry("800x600")

frame = tk.Frame(root)
frame.pack(pady=10)

tk.Button(frame, text="Connect & Fetch Employees", command=fetch_data, bg="#0078D7", fg="white", font=("Segoe UI", 10, "bold"), padx=10, pady=5).pack(side="left", padx=5)

tk.Button(frame, text="Export to CSV", command=export_csv, bg="#4CAF50", fg="white", font=("Segoe UI", 10, "bold"), padx=10, pady=5).pack(side="left", padx=5)

tk.Button(frame, text="Add Employee", command=open_add_employee_popup, bg="#F0AD4E", fg="black", font=("Segoe UI", 10, "bold"), padx=10, pady=5).pack(side="left", padx=5)

filter_frame = tk.Frame(root)
filter_frame.pack(pady=5)

department_var = tk.StringVar()
department_var.set("All Departments")
department_menu = tk.OptionMenu(filter_frame, department_var, "All Departments")
department_menu.pack()

status_label = tk.Label(root, text="Not connected", fg="gray")
status_label.pack(pady=5)

cols = ("ID", "Name", "Age", "Department", "Salary")
tree = ttk.Treeview(root, columns=cols, show="headings")
for col in cols:
    tree.heading(col, text=col)
    tree.column(col, anchor="center", width=120)
tree.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

root.mainloop()
