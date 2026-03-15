import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

# Student Data Storage # 

students = []


# Student Functions # 

def add_student_data(name, dob, marks):
    students.append({"name": name, "dob": dob, "marks": marks})

def update_student_data(index, name, dob, marks):
    students[index] = {"name": name, "dob": dob, "marks": marks}

def delete_student_data(index):
    del students[index]


# Display & Utility # 

def display_students():
    for row in tree.get_children():
        tree.delete(row)
    for idx, student in enumerate(students):
        tree.insert("", "end", text=str(idx), values=(student["name"], student["dob"], student["marks"]))

def clear_entries():
    name_entry.delete(0, tk.END)
    dob_entry.delete(0, tk.END)
    marks_entry.delete(0, tk.END)


# Treeview Selection Handler # 

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

# GUI Student Management Buttons # 

def add_student():
    name = name_entry.get()
    dob = dob_entry.get()
    try:
        marks = float(marks_entry.get())
    except ValueError:
        messagebox.showerror("Invalid Input", "Marks must be a number.")
        return
    if name and dob:
        add_student_data(name, dob, marks)
        messagebox.showinfo("Success", "Student added.")
        clear_entries()
        display_students()
    else:
        messagebox.showwarning("Missing Data", "Enter all fields.")

def update_student():
    selected = tree.focus()
    if not selected:
        messagebox.showwarning("Select Student", "Select a student to update.")
        return
    index = int(tree.item(selected, "text"))
    name = name_entry.get()
    dob = dob_entry.get()
    try:
        marks = float(marks_entry.get())
    except ValueError:
        messagebox.showerror("Invalid Input", "Marks must be a number.")
        return
    if name and dob:
        update_student_data(index, name, dob, marks)
        messagebox.showinfo("Success", "Student updated.")
        clear_entries()
        display_students()
    else:
        messagebox.showwarning("Missing Data", "Enter all fields.")

def delete_student():
    selected = tree.focus()
    if not selected:
        messagebox.showwarning("Select Student", "Select a student to delete.")
        return
    index = int(tree.item(selected, "text"))
    delete_student_data(index)
    messagebox.showinfo("Success", "Student deleted.")
    clear_entries()
    display_students()

def sort_students(by):
    if by == "name":
        students.sort(key=lambda x: x["name"])
    else:
        students.sort(key=lambda x: x["marks"], reverse=True)
    display_students()

# ------------------------- # 
# Chatbot Functions # 
# ------------------------- # 
def chatbot_response(msg):
    msg = msg.lower()
    # HELP
    if "help" in msg:
        return ( "I can help with:\n"
                "- add student <name> <dob> <marks>\n"
                "- update student <index> <name> <dob> <marks>\n"
                "- delete student <index>\n"
                "- show students\n"
                "- sort by name\n"
                "- sort by marks" )
    # ADD STUDENT
    if msg.startswith("add student"):
        try:
            _, _, name, dob, marks = msg.split()
            add_student_data(name, dob, float(marks))
            display_students()
            return f"Added student {name}."
        except:
            return "Format: add student <name> <dob> <marks>"
    # UPDATE STUDENT
    if msg.startswith("update student"):
        parts = msg.split()
        if len(parts) == 6:
            _, _, idx, name, dob, marks = parts
            try:
                idx = int(idx)
                update_student_data(idx, name, dob, float(marks))
                display_students()
                return f"Updated student {idx}."
            except:
                return "Index or marks invalid."
        else:
            return "Format: update student <index> <name> <dob> <marks>"
    # DELETE STUDENT
    if msg.startswith("delete student"):
        parts = msg.split()
        if len(parts) == 3:
            try:
                idx = int(parts[2])
                delete_student_data(idx)
                display_students()
                return f"Deleted student {idx}."
            except:
                return "Invalid student index."
        else:
            return "Format: delete student <index>"
    # SHOW STUDENTS
    if "show students" in msg:
        display_students()
        return "Displaying all students."
    # SORT
    if "sort by name" in msg:
        sort_students("name")
        return "Students sorted by name."
    if "sort by marks" in msg:
        sort_students("marks")
        return "Students sorted by marks."
    return "Sorry, I did not understand. Type 'help'."

def send_message():
    user_msg = chat_entry.get()
    chat_box.config(state="normal")
    chat_box.insert(tk.END, f"You: {user_msg}\n")
    bot_reply = chatbot_response(user_msg)
    chat_box.insert(tk.END, f"Bot: {bot_reply}\n\n")
    chat_box.config(state="disabled")
    chat_entry.delete(0, tk.END)


# MAIN GUI # 
 
root = tk.Tk()
root.title("Student Performance Manager + Chatbot")
root.geometry("900x600")
root.resizable(False, False)

# --- Student Input Fields --- 
tk.Label(root, text="Name:").place(x=20, y=20)
name_entry = tk.Entry(root, width=30)
name_entry.place(x=100, y=20)

tk.Label(root, text="DOB (YYYY-MM-DD):").place(x=20, y=60)
dob_entry = tk.Entry(root, width=30)
dob_entry.place(x=150, y=60)

tk.Label(root, text="Marks:").place(x=20, y=100)
marks_entry = tk.Entry(root, width=30)
marks_entry.place(x=100, y=100)

# Buttons
tk.Button(root, text="Add", width=12, command=add_student).place(x=350, y=20)
tk.Button(root, text="Update", width=12, command=update_student).place(x=350, y=60)
tk.Button(root, text="Delete", width=12, command=delete_student).place(x=350, y=100)
tk.Button(root, text="Sort Name", width=12, command=lambda: sort_students("name")).place(x=350, y=140)
tk.Button(root, text="Sort Marks", width=12, command=lambda: sort_students("marks")).place(x=350, y=180)

# --- Treeview --- 
columns = ("Name", "Date of Birth", "Marks")
tree = ttk.Treeview(root, columns=columns, show="headings")
for col in columns:
    tree.heading(col, text=col)
tree.place(x=20, y=240, width=500, height=330)
tree.bind("<<TreeviewSelect>>", on_tree_select)

# --- Chatbot UI --- 
chat_box = tk.Text(root, width=40, height=10)
chat_box.place(x=550, y=20)
chat_entry = tk.Entry(root, width=30)
chat_entry.place(x=550, y=200)
tk.Button(root, text="Send", command=send_message).place(x=750, y=200)

root.mainloop()