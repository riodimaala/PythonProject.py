from tkinter import *
from tkinter import messagebox, ttk
import json

# Setup
window = Tk()
window.title("Health Routine Planner")
window.geometry("900x700")
window.config(bg="#4d8f86")
icon = PhotoImage(file="./logo.png")
window.iconphoto(False, icon)

# HEADER
header_label = Label(window,
                     text="Smart Health Tracker:\nBMI Calculator with Routine Planner",
                     font=('Arial', 30, 'bold'),
                     bg='lightblue',
                     justify=CENTER)
header_label.pack(pady=(10, 10))

# USER PROFILE FRAME
profile_frame_width = 400
profile_frame = Frame(window, bg='lightblue', bd=1, relief='solid', width=profile_frame_width)
profile_frame.pack(pady=(0, 15))
profile_frame.pack_propagate(False)

profile_label = Label(profile_frame,
                      text='USER PROFILE',
                      font=('Arial', 18, 'bold'),
                      bg='lightblue')
profile_label.grid(row=0, column=0, columnspan=2, sticky=W, padx=10, pady=8)

# Name
name_label = Label(profile_frame, text='Name:', font=('Arial', 14), bg='lightblue')
name_label.grid(row=1, column=0, sticky=E, padx=(10, 5), pady=5)
entry_name = Entry(profile_frame, font=('Arial', 14), bg='#f2f2f2', width=30)
entry_name.grid(row=1, column=1, padx=(0, 10), pady=5)

# Age
age_label = Label(profile_frame, text='Age:', font=('Arial', 14), bg='lightblue')
age_label.grid(row=2, column=0, sticky=E, padx=(10, 5), pady=5)
entry_age = Entry(profile_frame, font=('Arial', 14), bg='#f2f2f2', width=30)
entry_age.grid(row=2, column=1, padx=(0, 10), pady=5)

# Gender
gender_label = Label(profile_frame, text='Gender:', font=('Arial', 14), bg='lightblue')
gender_label.grid(row=3, column=0, sticky=E, padx=(10, 5), pady=5)
gender_combo = ttk.Combobox(profile_frame, values=["Male", "Female"], font=('Arial', 11), width=28, state="readonly")
gender_combo.grid(row=3, column=1, padx=(0, 14), pady=5)
gender_combo.current(1)

# --- Load Backup JSON ---
def load_backup_json():
    try:
        with open("routine_backup.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"weekly": {}, "monthly": {}, "profile": {}}

def save_backup_json(data):
    with open("routine_backup.json", "w") as f:
        json.dump(data, f, indent=4)

backup_data = load_backup_json()
if "profile" not in backup_data:
    backup_data["profile"] = {"name": "", "age": "", "gender": "", "height": "", "weight": "", "bmi": ""}

# BMI CALCULATOR FRAME
bmi_frame = Frame(window, bg='lightblue')
bmi_frame.pack()

bmi_label = Label(bmi_frame, text="BMI CALCULATOR", font=('Arial', 18, 'bold'), bg='lightblue')
bmi_label.pack(pady=5)

height_label = Label(bmi_frame, text="HEIGHT (cm)", font=('Arial', 14, 'underline'), bg='lightblue')
height_label.pack()
entry_height = Entry(bmi_frame, font=('Arial', 14), bg='#f2f2f2', width=10, justify=CENTER)
entry_height.pack(pady=2)

weight_label = Label(bmi_frame, text="WEIGHT (kg)", font=('Arial', 14, 'underline'), bg='lightblue')
weight_label.pack()
entry_weight = Entry(bmi_frame, font=('Arial', 14), bg='#f2f2f2', width=10, justify=CENTER)
entry_weight.pack(padx=1, pady=7)

def calculate_bmi():
    try:
        height_cm = float(entry_height.get())
        weight = float(entry_weight.get())
        if height_cm <= 0 or weight <= 0:
            messagebox.showerror("Input Error", "Height and Weight must be greater than zero.")
            return
        height_m = height_cm / 100
        bmi = weight / (height_m * height_m)

        if bmi < 18.5:
            category = "YOU ARE UNDERWEIGHT"
            color = "orange"
        elif bmi < 25:
            category = "YOU HAVE A NORMAL WEIGHT"
            color = "green"
        elif bmi < 30:
            category = "YOU ARE OVERWEIGHT"
            color = "red"
        else:
            category = "YOU ARE OBESE"
            color = "yellow"

        bmi_result.config(text=f"{bmi:.2f} - {category}", fg=color)

# Save profile + BMI data into JSON
        backup_data["profile"]["name"] = entry_name.get()
        backup_data["profile"]["age"] = entry_age.get()
        backup_data["profile"]["gender"] = gender_combo.get()
        backup_data["profile"]["height"] = entry_height.get()
        backup_data["profile"]["weight"] = entry_weight.get()
        backup_data["profile"]["bmi"] = f"{bmi:.2f} - {category}"
        save_backup_json(backup_data)

    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numbers for height and weight.")

calc_button = Button(bmi_frame, text="Calculate BMI", font=('Arial', 15, 'bold'), bg='#20bef7', command=calculate_bmi)
calc_button.pack(pady=8)

result_frame = Frame(bmi_frame, bg='#4d8f86')
result_frame.pack()
result_label = Label(result_frame, text="Your BMI is:", font=('Arial', 18), bg='#4d8f86')
result_label.pack(side=LEFT)
bmi_result = Label(result_frame, text="0.00", font=('Arial', 18, 'bold'), bg='#4d8f86')
bmi_result.pack(side=LEFT)

#HELPER TO SAVE PROFILE
def save_profile_info():
    backup_data["profile"]["name"] = entry_name.get()
    backup_data["profile"]["age"] = entry_age.get()
    backup_data["profile"]["gender"] = gender_combo.get()
    backup_data["profile"]["height"] = entry_height.get()
    backup_data["profile"]["weight"] = entry_weight.get()
    backup_data["profile"]["bmi"] = bmi_result.cget("text")

def open_routine_plan_window():
    save_profile_info()   # ✅ save profile first
    clear_window()
    routine_var = StringVar(value="weekly")

def show_weekly_routine():
    save_profile_info()   # ✅ save profile first
    clear_window()

def show_monthly_routine(week_index=0):
        save_profile_info()  # ✅ save profile first
        clear_window()

def clear_window():
        for widget in window.winfo_children():
            widget.destroy()

# --- Routine Plan Selection UI ---
def open_routine_plan_window():
    clear_window()
    routine_var = StringVar(value="weekly")

    box_frame = Frame(window, bg="lightblue", bd=1, relief="solid")
    box_frame.place(x=580, y=95, width=400, height=120)

    Label(window, text="Choose Your Routine Plan", font=("Arial", 30, "bold"), bg="light blue").pack(pady=30)
    Radiobutton(window, text="Weekly Routine Planner", font=("Arial", 15), variable=routine_var, value="weekly",
                bg="lightblue").pack()
    Radiobutton(window, text="Monthly Routine Planner", font=("Arial", 15), variable=routine_var, value="monthly",
                bg="lightblue").pack()

    def continue_to_routine():
        if routine_var.get() == "weekly":
            show_weekly_routine()
        else:
            show_monthly_routine(0)

    Button(window, text="Continue", font=("Arial", 15), bg="green", command=continue_to_routine).pack(pady=50)

next_button = Button(window, text='Next', font=('Arial', 15, 'bold'), bg='green', command=open_routine_plan_window)
next_button.place(x=1200, y=640)

# --- Weekly Routine UI ---
def show_weekly_routine():
    clear_window()
    Label(window, text="Personalized Weekly Health Plan", font=("Arial", 30, "bold"), bg="lightblue").pack(pady=10)

    table_frame = Frame(window, bg="lightblue", bd=1, relief="solid")
    table_frame.pack(padx=30, pady=10)

    headers = ["Day", "Sleep (hrs)", "Exercise (mins)", "Note"]
    for col, text in enumerate(headers):
        Label(table_frame, text=text, font=("Arial", 15, "bold"), bg="lightblue", width=15).grid(row=0, column=col)

    row_widgets = {}
    for r, (day, values) in enumerate(backup_data["weekly"].items(), start=1):
        Label(table_frame, text=day, font=("Arial", 15), bg="lightblue").grid(row=r, column=0)
        Label(table_frame, text=values["sleep"], font=("Arial", 15), bg="lightblue").grid(row=r, column=1)
        Label(table_frame, text=values["exercise"], font=("Arial", 15), bg="lightblue").grid(row=r, column=2)

        note_entry = Entry(table_frame, width=10)
        note_entry.insert(0, values["note"])
        note_entry.grid(row=r, column=3)

        row_widgets[day] = note_entry

    def save_weekly():
        for day in row_widgets:
            backup_data["weekly"][day]["note"] = row_widgets[day].get()
        save_backup_json(backup_data)  # ✅ wag nang tawagin ang save_profile_info dito
        messagebox.showinfo("Saved", "Weekly routine saved!")
#BUTTON SAVE WEEKLY
    Button(window, text="Save Routine", font=("Arial", 15), bg="#4CAF50", fg="white", command=save_weekly).place(x=1200,
                                                                                                                 y=500)
    Button(window, text="← Back", font=("Arial", 15), bg="Red", command=open_routine_plan_window).place(x=230, y=500)

# --- Monthly Routine UI ---
def show_monthly_routine(week_index=0):
    clear_window()
    Label(window, text="Personalized Monthly Health Plan", font=("Arial", 30, "bold"), bg="lightblue").pack(pady=10)

    table_frame = Frame(window, bg="lightblue", bd=1, relief="solid")
    table_frame.pack(padx=30, pady=10)

    headers = ["Day", "Sleep (hrs)", "Exercise (mins)", "Note"]
    for col, text in enumerate(headers):
        Label(table_frame, text=text, font=("Arial", 15, "bold"), bg="lightblue", width=15).grid(row=0, column=col)

    row_widgets = {}
    start_day = week_index * 7 + 1
    end_day = min(start_day + 6, 30)
    row_index = 1

    Label(table_frame, text=f"Week {week_index + 1}", font=("Arial", 15, "bold"), bg="lightblue").grid(row=row_index,
                                                                                                       column=0,
                                                                                                       columnspan=4,
                                                                                                       sticky="w")
    row_index += 1

    for day in range(start_day, end_day + 1):
        values = backup_data["monthly"][f"Day {day}"]
        Label(table_frame, text=f"Day {day}", font=("Arial", 15), bg="lightblue").grid(row=row_index, column=0)
        Label(table_frame, text=values["sleep"], font=("Arial", 15), bg="lightblue").grid(row=row_index, column=1)
        Label(table_frame, text=values["exercise"], font=("Arial", 15), bg="lightblue").grid(row=row_index, column=2)

        note_entry = Entry(table_frame, width=10)
        note_entry.insert(0, values["note"])
        note_entry.grid(row=row_index, column=3)

        row_widgets[f"Day {day}"] = note_entry
        row_index += 1

    def save_monthly():
        for day in row_widgets:
            backup_data["monthly"][day]["note"] = row_widgets[day].get()
        save_backup_json(backup_data)  # ✅ wag nang tawagin ang save_profile_info dito
        messagebox.showinfo("Saved", "Monthly routine saved!")
#BUTTON MONTHLY
    Button(window, text="Save Routine", font=("Arial", 15), bg="#4CAF50", fg="white", command=save_monthly).place(x=700,
                                                                                                                  y=500)
    if week_index > 0:
        Button(window, text="← Previous", font=("Arial", 15), bg="#2196F3", fg="white",
               command=lambda: show_monthly_routine(week_index - 1)).place(x=1070, y=500)

    if end_day < 30:
        Button(window, text="Next →", font=("Arial", 15), bg="#2196F3", fg="white",
               command=lambda: show_monthly_routine(week_index + 1)).place(x=1200, y=500)

    Button(window, text="← Back", font=("Arial", 15), bg="Red", command=open_routine_plan_window).place(x=230, y=500)

# --- Loader to restore profile info ---
def load_profile_info():
    if "profile" in backup_data:
        entry_name.delete(0, END)
        entry_name.insert(0, backup_data["profile"].get("name", ""))

        entry_age.delete(0, END)
        entry_age.insert(0, backup_data["profile"].get("age", ""))

        gender_combo.set(backup_data["profile"].get("gender", "Male"))

        entry_height.delete(0, END)
        entry_height.insert(0, backup_data["profile"].get("height", ""))

        entry_weight.delete(0, END)
        entry_weight.insert(0, backup_data["profile"].get("weight", ""))

        bmi_result.config(text=backup_data["profile"].get("bmi", "0.00"))

# --- Start App ---
def show_profile_ui():
    load_profile_info()  # ✅ load saved profile info on startup


show_profile_ui()
window.mainloop()