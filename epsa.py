

import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

# List to store student data
students = []

# Function to add a student
def add_student():
    name = name_entry.get()
    dob = dob_entry.get()
    try:
        marks = float(marks_entry.get())
    except ValueError:
        messagebox.showerror("Invalid Input", "Marks should be a number.")
        return

    if name and dob:
        students.append({"name": name, "dob": dob, "marks": marks})
        messagebox.showinfo("Success", "Student added successfully.")
        clear_entries()
        display_students()
    else:
        messagebox.showwarning("Missing Data", "Please enter all fields.")

# Function to update a student
def update_student():
    selected = tree.focus()
    if not selected:
        messagebox.showwarning("Select Student", "Please select a student to update.")
        return

    index = int(tree.item(selected, "text"))
    name = name_entry.get()
    dob = dob_entry.get()
    try:
        marks = float(marks_entry.get())
    except ValueError:
        messagebox.showerror("Invalid Input", "Marks should be a number.")
        return

    if name and dob:
        students[index] = {"name": name, "dob": dob, "marks": marks}
        messagebox.showinfo("Success", "Student updated successfully.")
        clear_entries()
        display_students()
    else:
        messagebox.showwarning("Missing Data", "Please enter all fields.")

# Function to delete a student
def delete_student():
    selected = tree.focus()
    if not selected:
        messagebox.showwarning("Select Student", "Please select a student to delete.")
        return

    index = int(tree.item(selected, "text"))
    del students[index]
    messagebox.showinfo("Success", "Student deleted successfully.")
    clear_entries()
    display_students()

# Function to sort students
def sort_students(by):
    if by == "name":
        students.sort(key=lambda x: x["name"])
    elif by == "marks":
        students.sort(key=lambda x: x["marks"], reverse=True)
    display_students()

# Function to display students
def display_students():
    for row in tree.get_children():
        tree.delete(row)
    for idx, student in enumerate(students):
        tree.insert("", "end", text=str(idx), values=(student["name"], student["dob"], student["marks"]))

# Function to clear entry fields
def clear_entries():
    name_entry.delete(0, tk.END)
    dob_entry.delete(0, tk.END)
    marks_entry.delete(0, tk.END)

# Function to populate fields when selecting from treeview
def on_tree_select(event):
    selected = tree.focus()
    if selected:
        index = int(tree.item(selected, "text"))
        student = students[index]
        name_entry.delete(0, tk.END)
        name_entry.insert(0, student["name"])
        dob_entry.delete(0, tk.END)
        dob_entry.insert(0, student["dob"])
        marks_entry.delete(0, tk.END)
        marks_entry.insert(0, student["marks"])

# GUI Setup
root = tk.Tk()
root.title("Student Performance Manager by Epsa")
root.geometry("700x500")
root.resizable(False, False)

# Labels and Entries
tk.Label(root, text="Name:").place(x=20, y=20)
name_entry = tk.Entry(root, width=30)
name_entry.place(x=100, y=20)

tk.Label(root, text="Date of Birth (YYYY-MM-DD):").place(x=20, y=60)
dob_entry = tk.Entry(root, width=30)
dob_entry.place(x=220, y=60)

tk.Label(root, text="Marks:").place(x=20, y=100)
marks_entry = tk.Entry(root, width=30)
marks_entry.place(x=100, y=100)

# Buttons
tk.Button(root, text="Add", width=12, command=add_student).place(x=500, y=20)
tk.Button(root, text="Update", width=12, command=update_student).place(x=500, y=60)
tk.Button(root, text="Delete", width=12, command=delete_student).place(x=500, y=100)
tk.Button(root, text="Sort by Name", width=12, command=lambda: sort_students("name")).place(x=500, y=140)
tk.Button(root, text="Sort by Marks", width=12, command=lambda: sort_students("marks")).place(x=500, y=180)

# Treeview for displaying students
columns = ("Name", "Date of Birth", "Marks")
tree = ttk.Treeview(root, columns=columns, show="headings")
for col in columns:
    tree.heading(col, text=col)
tree.place(x=20, y=220, width=650, height=250)
tree.bind("<<TreeviewSelect>>", on_tree_select)

root.mainloop()