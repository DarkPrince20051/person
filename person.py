import tkinter as tk
from tkinter import messagebox, ttk
import json

# Set the file name as a variable
DATA_FILE = "person_data.json"

people = []
START = "\n=========== Person Management System ===========\n\n\nEnter 1 to Add Person, \nEnter 2 to Display People \nEnter 3 to Search a Person by Name \nEnter 4 to Delete Selected Person \nEnter 5 to Quit Application \n"

person_combobox = None

def save_data():
    try:
        with open(DATA_FILE, 'w') as file:
            json.dump(people, file, indent=2)
    except Exception as e:
        messagebox.showerror("Error", f"Error saving data: {str(e)}")

def load_data():
    try:
        with open(DATA_FILE, 'r') as file:
            data = json.load(file)
            people.extend(data)
    except FileNotFoundError:
        pass
    except Exception as e:
        messagebox.showerror("Error", f"Error loading data: {str(e)}")

def add_person():
    name = entry_name.get()
    birthdate = entry_birthdate.get()
    birthplace = entry_birthplace.get()
    oib = entry_oib.get()
    search_name = entry_search.get()  # Include the search name

    if name and birthdate and birthplace and oib:
        people.append({
            'name': name,
            'birthdate': birthdate,
            'birthplace': birthplace,
            'oib': oib,
            'search_name': search_name  # Include the search name in the data
        })
        save_data()
        messagebox.showinfo("Success", "Person added successfully!")
        clear_entries()
    else:
        messagebox.showwarning("Error", "Please fill in all fields.")

def list_people():
    quantity = len(people)
    names = [person['name'] for person in people]

    global person_combobox

    if quantity:
        selected_person = tk.StringVar(root)
        selected_person.set(names[0])

        if person_combobox:
            person_combobox.destroy()

        person_combobox = ttk.Combobox(root, textvariable=selected_person, values=names, state="readonly")
        person_combobox.grid(row=8, column=0, columnspan=2, padx=5, pady=5)

        def display_person_details(event):
            selected_index = names.index(person_combobox.get())
            selected_person = people[selected_index]
            print_person_info(selected_person)

        person_combobox.bind("<<ComboboxSelected>>", display_person_details)

        print(f'\nList of people that you have in your collection: \n{names}. \nIn total, you have {quantity} {"person" if quantity == 1 else "people"}.')
        print("Quantity:", quantity)
        print("People list:", people)
    else:
        print('There are no people in your collection.')
        messagebox.showinfo("People in Collection", 'There are no people in your collection.')

def print_person_info(person):
    messagebox.showinfo("Person Information", f'Name: {person["name"]},\nBirthdate: {person["birthdate"]},\nBirthplace: {person["birthplace"]},\nOIB: {person["oib"]},\nSearch Name: {person["search_name"]}.')

def find_name():
    search_name = entry_search.get()
    for person in people:
        if person['search_name'] == search_name:
            print_person_info(person)
            return
    messagebox.showinfo("Person Not Found", 'Requested name was not found in the collection.')

def clear_entries():
    entry_name.delete(0, tk.END)
    entry_birthdate.delete(0, tk.END)
    entry_birthplace.delete(0, tk.END)
    entry_oib.delete(0, tk.END)
    entry_search.delete(0, tk.END)
    entry_name.focus_set()

def reset_entries():
    clear_entries()
    if person_combobox:
        person_combobox.destroy()

def clear_list():
    global people
    people = []
    save_data()
    if person_combobox:
        person_combobox.destroy()
    messagebox.showinfo("List Cleared", "The person list has been cleared.")

def delete_selected_person():
    answer = messagebox.askyesno("Delete Person", "Are you sure you want to delete the selected person?")
    if answer:
        selected_person_name = entry_search.get()
        for i, person in enumerate(people):
            if person['search_name'] == selected_person_name:
                del people[i]
                save_data()
                messagebox.showinfo("Person Deleted", f'The person "{selected_person_name}" has been deleted.')
                list_people()
                return
        messagebox.showinfo("No Match", 'No person matches the entered name.')

def exit_application():
    answer = messagebox.askyesno("Exit", "Do you want to save and exit?")
    if answer:
        save_data()
        root.destroy()

root = tk.Tk()
root.title("Person Management System")
root.resizable(False, False)

# Set the window in the center of the screen
window_width = 400
window_height = 460
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x_coordinate = (screen_width - window_width) // 2
y_coordinate = (screen_height - window_height) // 2
root.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")

# Set the background color to light blue
root.configure(bg='lightblue')

label_name = tk.Label(root, text="Name:")
label_birthdate = tk.Label(root, text="Birthdate:")
label_birthplace = tk.Label(root, text="Birthplace:")
label_oib = tk.Label(root, text="OIB:")
label_search = tk.Label(root, text="Search Name:")

entry_name = tk.Entry(root)
entry_birthdate = tk.Entry(root)
entry_birthplace = tk.Entry(root)
entry_oib = tk.Entry(root)
entry_search = tk.Entry(root)

button_add = tk.Button(root, text="Add Person", command=add_person)
button_list = tk.Button(root, text="List People", command=list_people)
button_search = tk.Button(root, text="Search Name", command=find_name)
button_reset = tk.Button(root, text="Reset Entries", command=reset_entries)
button_clear_list = tk.Button(root, text="Clear List", command=clear_list)
button_delete_selected_person = tk.Button(root, text="Delete Selected Person", command=delete_selected_person)
button_exit = tk.Button(root, text="Exit", command=exit_application)

label_name.grid(row=0, column=0, padx=5, pady=5, sticky=tk.E)
label_birthdate.grid(row=1, column=0, padx=5, pady=5, sticky=tk.E)
label_birthplace.grid(row=2, column=0, padx=5, pady=5, sticky=tk.E)
label_oib.grid(row=3, column=0, padx=5, pady=5, sticky=tk.E)
label_search.grid(row=4, column=0, padx=5, pady=5, sticky=tk.E)

entry_name.grid(row=0, column=1, padx=5, pady=5)
entry_birthdate.grid(row=1, column=1, padx=5, pady=5)
entry_birthplace.grid(row=2, column=1, padx=5, pady=5)
entry_oib.grid(row=3, column=1, padx=5, pady=5)
entry_search.grid(row=4, column=1, padx=5, pady=5)

button_add.grid(row=5, column=0, columnspan=2, pady=10)
button_list.grid(row=6, column=0, columnspan=2, pady=10)
button_search.grid(row=7, column=0, columnspan=2, pady=10)
button_reset.grid(row=9, column=0, pady=10, padx=(10, 0))
button_clear_list.grid(row=9, column=1, pady=10, padx=(0, 10))
button_delete_selected_person.grid(row=10, column=0, columnspan=2, pady=10)
button_exit.grid(row=11, column=0, columnspan=2, pady=10)

load_data()
root.protocol("WM_DELETE_WINDOW", exit_application)
root.mainloop()