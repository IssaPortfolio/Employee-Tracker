import tkinter as tk
from tkinter import PhotoImage, ttk, simpledialog, messagebox,scrolledtext,StringVar
import csv
import json
import random


def employee_data_editor():
    """Creates a GUI for managing employee data: loading, saving, editing, and searching employees."""

    # Initialize the JSON data with an empty list of employees
    employee_data = []

    selected_employee_index = None
    def load_json_and_refresh_display():
        try:
            with open('employee_data.json', 'r') as file:
                data = json.load(file)
                employees = data.get("employees", [])
                employee_data.clear()  # Clear the current employee data
                employee_data.extend(employees)  # Replace it with the loaded data
                display_employee_list()
                status_label.config(text="Employee data loaded successfully")
        except FileNotFoundError:
            clear_form()
            clear_display()
            status_label.config(text="File not found: employee_data.json")
        except json.JSONDecodeError:
            clear_form()
            clear_display()
            status_label.config(text="Invalid JSON format")

    def load_json():
        clear_listbox(employee_listbox)
        load_json_and_refresh_display()

    def save_json():
        try:
            with open('employee_data.json', 'r') as file:
                data = json.load(file)
                data["employees"] = employee_data  # Update the "employees" key with the current employee data
            with open('employee_data.json', 'w') as file:
                json.dump(data, file, indent=4)
            status_label.config(text="Employee data saved successfully")
            clear_listbox(employee_listbox)
            load_json_and_refresh_display()
        except FileNotFoundError:
            status_label.config(text="File not found: employee_data.json")
        except Exception as e:
            status_label.config(text=f"Error: {str(e)}")

    def search_by_name():
        name_to_search = role_search_var.get().lower()

        # Find employees matching the name
        matching_employees = [employee for employee in employee_data if name_to_search in employee["name"].lower()]

        # Clear the Listbox
        employee_listbox.delete(0, tk.END)

        # Add all employee names to the Listbox
        for employee in employee_data:
            employee_listbox.insert(tk.END, employee["name"])

        # Move the matching employee names to the top of the Listbox
        for employee in matching_employees:
            employee_listbox.delete(employee_listbox.get(0, tk.END).index(employee["name"]))
            employee_listbox.insert(0, employee["name"])

            # Move the matching employees to the top of the employee_data list
            employee_data.remove(employee)
            employee_data.insert(0, employee)

        # Update the detailed box
        clear_listbox(employee_listbox)
        display_employee_list()

    def delete_entry():
        global selected_employee_index
        clear_listbox(employee_listbox)
        if selected_employee_index is not None:
            employee_data.pop(selected_employee_index)  # Remove the selected employee
            selected_employee_index = None
            clear_form()
            clear_display()
            display_employee_list()
            
            status_label.config(text="Entry deleted")

    def add_employee():
        new_employee = extract_data()
        employee_data.insert(0, new_employee)
        clear_form()
        clear_display()
        display_employee_list()
        status_label.config(text="Employee added")

    def select_employee(event):
        global selected_employee_index
        selected_index = employee_listbox.curselection()
        if selected_index:
            selected_employee_index = selected_index[0]
            selected_employee = employee_data[selected_employee_index]
            populate_form(selected_employee)

    def clear_form():
        for entry in entry_widgets.values():
            entry.delete(0, tk.END)

    def clear_display():
        json_display.delete(1.0, tk.END)

    def populate_form(employee):
        clear_form()
        for key, value in employee.items():
            if key in entry_widgets:
                entry_widgets[key].insert(0, value)

    def extract_data():
        data = {}
        for key, entry in entry_widgets.items():
            data[key] = entry.get()

        # Check if the selected employee index is available
        global selected_employee_index
        selected_employee_index = None
        if selected_employee_index is not None:
            # Update the data for the selected employee
            employee_data[selected_employee_index].update(data)
            selected_employee_index = None  # Reset the selected employee index
        clear_listbox(employee_listbox)
        return data




    
    def clear_listbox(listbox):
        listbox.delete(0, tk.END)

    def display_employee_list(employees=None):
        clear_display()
        employees = employees or employee_data
        for index, employee in enumerate(employees):
            employee_listbox.insert(tk.END, employee["name"])
            json_display.insert(tk.END, f"Employee {index + 1}\n")
            json_display.insert(tk.END, f"Name: {employee['name']}\n")
            json_display.insert(tk.END, f"Role: {employee['role']}\n")
            json_display.insert(tk.END, f"Employee Number: {employee['employee_number']}\n\n")

    app = tk.Tk()
    app.title("Employee Data Editor")

    style = ttk.Style()
    style.theme_use("clam")
    style.configure("TButton", padding=6, relief="flat", background="#FFFDD0")
    style.configure("TLabel", padding=6, background="#FFFDD0", font=("Helvetica", 24))
    style.configure("TFrame", padding=6, background="#FFFDD0")
    style.configure("TEntry", padding=6)
    app.configure(bg="#0089BB")

    entry_widgets = {}
    json_display = scrolledtext.ScrolledText(app, wrap=tk.WORD, width=50, height=10, font=("Courier New", 12))
    json_display.grid(column=3, row=0, rowspan=11, padx=10, pady=10)

    form_fields = [
        ("Employee Number:", "employee_number"),
        ("Name:", "name"),
        ("Role:", "role")
    ]

    for label_text, key in form_fields:
        label = ttk.Label(app, text=label_text)
        label.grid(column=0, row=form_fields.index((label_text, key)), padx=10, pady=5)
        entry = ttk.Entry(app)
        entry.grid(column=1, row=form_fields.index((label_text, key)), padx=10, pady=5)
        entry_widgets[key] = entry


    role_search_var = StringVar()
    role_search_label = ttk.Label(app, text="Search by Name:")
    role_search_label.grid(row=len(form_fields)+3, column=0, padx=10, pady=5, sticky="e")
    role_search_entry = ttk.Entry(app, textvariable=role_search_var)
    role_search_entry.grid(row=len(form_fields)+3, column=1, padx=10, pady=5)
    role_search_button = ttk.Button(app, text="Search", command=search_by_name)
    role_search_button.grid(row=len(form_fields)+4, column=1, padx=10, pady=5)


    load_button = ttk.Button(app, text="Load Employee Data", command=load_json)
    load_button.grid(column=0, row=len(form_fields), columnspan=2, padx=10, pady=10)

    save_button = ttk.Button(app, text="Save Employee Data", command=save_json)
    save_button.grid(column=1, row=len(form_fields), columnspan=2, padx=10, pady=10)

    delete_button = ttk.Button(app, text="Delete Entry", command=delete_entry)
    delete_button.grid(column=0, row=len(form_fields) + 1, columnspan=2, padx=10, pady=10)

    add_button = ttk.Button(app, text="Add Employee", command=add_employee)
    add_button.grid(column=1, row=len(form_fields) + 1, columnspan=2, padx=10, pady=10)

    employee_listbox = tk.Listbox(app)
    employee_listbox.grid(column=2, row=len(form_fields)+2, rowspan=11, padx=10, pady=30)
    employee_listbox.bind("<<ListboxSelect>>", select_employee)

    status_label = ttk.Label(app, text="")
    status_label.grid(column=1, row=len(form_fields) + 4, columnspan=4, padx=10, pady=5)

    app.mainloop()



def generate_employee_number():
    """Generates a random 5-digit employee number."""
    return str(random.randint(10000, 99999))

def add_employee(role, employees):
    """
    Adds a new employee to the given role's employee list.

    Args:
    - role: Role of the employee being added.
    - employees: List of employees in the CSV format.

    Prompts the user for employee details and adds them to the employees list.
    """
    name = simpledialog.askstring("Input", f"Enter {role} name:")
    if name is not None:
        if name.isalpha():
            employee_number = generate_employee_number()
            while any(emp[2] == employee_number for emp in employees):
                employee_number = generate_employee_number()

            employees.append((name.lower(), role.lower(), employee_number))
            write_to_csv(employees)
            convert_to_json(employees)  # Automatically convert to JSON after adding
            messagebox.showinfo("Success", f"{name.title()} added successfully to {role.title()}!\nEmployee Number: {employee_number}")
        else:
            messagebox.showerror("Error", "Invalid characters in the employee name! Only letters are allowed.")

def view_employees(role, employees):
    """
    Displays a list of employees for a given role.

    Args:
    - role: Role of the employees being viewed.
    - employees: List of employees in the CSV format.

    Displays the employee details for the chosen role.
    """
    role_employees = [(emp[0], emp[1], emp[2]) for emp in employees if emp[1] == role.lower()]
    counter = len(role_employees)
    if role_employees:
        info = "\n".join([f"Name: {name.title()}\nRole: {role.title()}\nEmployee Number: {emp_num}\n{'-'*20}" for name, role, emp_num in role_employees])
        messagebox.showinfo(f"{role.title()} Employees", f"Total Employees: {counter}\n\n{info}")
    else:
        messagebox.showinfo(f"{role} Employees", f"No {role.title()} employees found!")

def search_employee(role, employees):
    """
    Searches for an employee by name within a given role.

    Args:
    - role: Role of the employee being searched.
    - employees: List of employees in the CSV format.

    Prompts the user for a name and displays employee details if found.
    """
    name = simpledialog.askstring("Input", f"Enter {role} name:")
    if name is not None:
        search_result = [(emp[0], emp[1], emp[2]) for emp in employees if name.lower() in emp[0] and emp[1] == role.lower()]
        if search_result:
            info = "\n".join([f"Name: {name.title()}\nRole: {role.title()}\nEmployee Number: {emp_num}\n{'-'*20}" for name, role, emp_num in search_result])
            messagebox.showinfo("Search Result", info)
        else:
            messagebox.showinfo("Search Result", f"No {role.title()} employee with the name '{name.title()}' found!")

def update_employee(role, employees):
    """
    Updates employee information within a given role.

    Args:
    - role: Role of the employee being updated.
    - employees: List of employees in the CSV format.

    Allows the user to update the name or role of an existing employee.
    """
    old_name = simpledialog.askstring("Input", f"Enter current {role} name:")
    if old_name is not None:
        old_name_lower = old_name.lower()
        role_employees = [emp for emp in employees if emp[1] == role.lower()]
        if any(old_name_lower in emp for emp in role_employees):
            # Find the employee with the given name and role
            for i, emp in enumerate(employees):
                if emp[0] == old_name_lower and emp[1] == role.lower():
                    # Ask the user which information to update
                    update_choice = simpledialog.askstring("Input", f"Update name or role for {old_name.title()}?\nEnter 'name' or 'role':")
                    if update_choice is not None:
                        if update_choice.lower() == 'name':
                            new_name = simpledialog.askstring("Input", f"Enter new {role.title()} name:")
                            if new_name is not None:
                                employees[i] = (new_name.lower(), role.lower(), emp[2])
                                write_to_csv(employees)
                                convert_to_json(employees)  # Automatically convert to JSON after updating
                                messagebox.showinfo("Success", f"{old_name.title()} updated to {new_name.title()} successfully!")
                        elif update_choice.lower() == 'role':
                            new_role = simpledialog.askstring("Input", f"Enter new role for {old_name}:")
                            if new_role is not None:
                                employees[i] = (emp[0], new_role.lower(), emp[2])
                                write_to_csv(employees)
                                convert_to_json(employees)  # Automatically convert to JSON after updating
                                messagebox.showinfo("Success", f"Role for {old_name.title()} updated to {new_role.title()} successfully!")
                        else:
                            messagebox.showerror("Error", "Invalid choice. Please enter 'name' or 'role'.")
                    break
        else:
            messagebox.showinfo("Error", f"No {role} employee with the name '{old_name.title()}' found!")

def delete_employee(role, employees):
    """
    Deletes an employee within a given role.

    Args:
    - role: Role of the employee being deleted.
    - employees: List of employees in the CSV format.

    Prompts the user for a name and deletes the employee if found.
    """
    name = simpledialog.askstring("Input", f"Enter {role} name to delete:")
    if name is not None:
        name_lower = name.lower()
        role_employees = [emp for emp in employees if emp[1] == role.lower()]
        if any(name_lower in emp for emp in role_employees):
            employees[:] = [emp for emp in employees if not (name_lower in emp and emp[1] == role.lower())]
            write_to_csv(employees)
            convert_to_json(employees)  # Automatically convert to JSON after deleting
            messagebox.showinfo("Success", f"{name.title()} deleted successfully!")
        else:
            messagebox.showinfo("Error", f"No {role.title()} employee with the name '{name.title()}' found!")

def write_to_csv(employees):
    """
    Writes employee data to a CSV file.

    Args:
    - employees: List of employees in the CSV format.

    Writes the employee details to a CSV file.
    """
    with open('employee_data.csv', 'w', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['Employee Name', 'Role', 'Employee Number'])
        for emp in employees:
            csv_writer.writerow([emp[0], emp[1], emp[2]])

def convert_to_json(employees):
    """
    Converts employee data to JSON format.

    Args:
    - employees: List of employees in the CSV format.

    Converts the employee details to JSON format and saves them to a file.
    """
    json_data = {
        "employees": [
            {"name": emp[0], "role": emp[1], "employee_number": emp[2]} for emp in employees
        ]
    }
    with open('employee_data.json', 'w') as json_file:
        json.dump(json_data, json_file, indent=2)

def read_csv_data():
    """
    Reads employee data from a CSV file.

    Returns:
    - List of employees in the CSV format.

    Reads the employee details from a CSV file.
    """
    try:
        with open('employee_data.csv', 'r', newline='', encoding='utf-8') as csvfile:
            csv_reader = csv.reader(csvfile)
            next(csv_reader)  # Skip the header row
            return [tuple(row) for row in csv_reader]
    except FileNotFoundError:
        return []

def generate_role_window(role, employees):
    """
    Generates a window for managing employees of a specific role.

    Args:
    - role: Role of the employees being managed.
    - employees: List of employees in the CSV format.

    Creates a window to manage employees based on the specified role.
    """
    role_window = tk.Toplevel(root)
    role_window.title(f"{role} Window")
    role_window.geometry("500x500")

    add_button = ttk.Button(role_window, text=f"Add {role} Employee", command=lambda: add_employee(role, employees))
    view_button = ttk.Button(role_window, text=f"View {role} Employees", command=lambda: view_employees(role, employees))
    search_button = ttk.Button(role_window, text=f"Search {role} Employee", command=lambda: search_employee(role, employees))
    update_button = ttk.Button(role_window, text=f"Update {role} Employee", command=lambda: update_employee(role, employees))
    delete_button = ttk.Button(role_window, text=f"Delete {role} Employee", command=lambda: delete_employee(role, employees))

    add_button.pack(fill=tk.BOTH, padx=10, pady=5)
    view_button.pack(fill=tk.BOTH, padx=10, pady=5)
    search_button.pack(fill=tk.BOTH, padx=10, pady=5)
    update_button.pack(fill=tk.BOTH, padx=10, pady=5)
    delete_button.pack(fill=tk.BOTH, padx=10, pady=5)

root = tk.Tk()
root.title("Main Window")
root.geometry("800x800")

style = ttk.Style()
style.theme_use("clam")
style.configure("TButton", padding=6, relief="flat", background="#FFFDD0")
style.configure("TLabel", padding=6, background="#FFFDD0", font=("Helvetica", 24))
style.configure("TFrame", padding=6, background="#FFFDD0")
style.configure("TEntry", padding=6)
root.configure(bg="#0089BB")

image_1 = PhotoImage(file="./images/GD_new.png")
image_2 = PhotoImage(file="./images/SD_new.png")
image_3 = PhotoImage(file="./images/J_new.png")
image_4 = PhotoImage(file="./images/HR_new.png")
image_5 = PhotoImage(file="./images/MK_new.png")
image_6 = PhotoImage(file="./images/manage.png")

def on_button_click(role):
    """
    Callback function when a role button is clicked.

    Args:
    - role: Role associated with the button clicked.

    Generates a new window for the specific role's employees.
    """

    employees = read_csv_data()
    generate_role_window(role, employees)

label_title = ttk.Label(root, text="Employee Tracker")

button_GD = ttk.Button(root, image=image_1, command=lambda: on_button_click("Graphic Design"), text="Graphic Design", compound=tk.TOP)
button_SD = ttk.Button(root, image=image_2, command=lambda: on_button_click("Software Developers"), text="Software Developers", compound=tk.TOP)
button_J = ttk.Button(root, image=image_3, command=lambda: on_button_click("Janitorial"), text="Janitorial", compound=tk.TOP)
button_HR = ttk.Button(root, image=image_4, command=lambda: on_button_click("Human Resources"), text="Human Resources", compound=tk.TOP)
button_MK = ttk.Button(root, image=image_5, command=lambda: on_button_click("Marketing"), text="Marketing", compound=tk.TOP)
button_M = ttk.Button(root, image=image_6, command=employee_data_editor, text="Manage All", compound=tk.TOP)

label_title.grid(row=0, column=1, padx=10, pady=10)
button_GD.grid(row=1, column=0, padx=10, pady=10)
button_SD.grid(row=1, column=1, padx=10, pady=10)
button_J.grid(row=1, column=2, padx=10, pady=10)
button_HR.grid(row=2, column=0, padx=10, pady=10)
button_MK.grid(row=2, column=1, padx=10, pady=10)
button_M.grid(row=2, column=2, padx=10, pady=10)

# Automatically convert to JSON when the application starts
convert_to_json(read_csv_data())

root.mainloop()
