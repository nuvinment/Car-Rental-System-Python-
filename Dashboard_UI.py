import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
from tkcalendar import DateEntry
from PIL.ImageOps import expand
import sqlite3
from datetime import datetime
import session


def car_management():
    new_window = tk.Toplevel()
    new_window.geometry(f"{width}x{height}+{left}+{top}")
    new_window.title("Car Management")
    new_window.resizable(False, False)
    new_window.iconbitmap("Logo.ico")

    # Load the background image
    try:
        bg_image = Image.open("function_bg.jpg")  # Replace with your actual image path
        bg_image = bg_image.resize((width, height), Image.LANCZOS)  # Resize to fit the window
        bg_photo = ImageTk.PhotoImage(bg_image)

        # Create a label to hold the background image
        bg_label = tk.Label(new_window, image=bg_photo)
        bg_label.image = bg_photo  # Keep a reference to avoid garbage collection
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)  # Fill the entire window
    except Exception as e:
        print(f"Error loading background image: {e}")

    # Title label
    title_label = tk.Label(new_window, text="Car Management", font=("Arial", 18, "bold"))
    title_label.pack(pady=20)

    # Detail frame
    detail_frame = tk.LabelFrame(new_window, text="Enter Details", font=("Arial", 15), bg="lightgrey")
    detail_frame.place(x=20, y=80, width=420, height=600)

    # Data frame
    data_frame = tk.Frame(new_window, bd=12, bg="lightgrey")
    data_frame.place(x=475, y=90, width=700, height=575)

    # Add other widgets to detail_frame and data_frame as needed

    #=======Variables==========
    car_id = tk.StringVar()
    car_make = tk.StringVar()
    car_model = tk.StringVar()
    year_manufactured = tk.StringVar()  # New variable
    car_number = tk.StringVar()
    car_milage = tk.StringVar()
    charge_per_day = tk.StringVar()
    car_availability = tk.StringVar()
    car_color = tk.StringVar()  # New variable

    search_by = tk.StringVar()

    #=======Entry Fields=======#

    carid_lbl = tk.Label(detail_frame, text="Car ID", font=('Arial', 12), bg="lightgrey")
    carid_lbl.grid(row=0, column=0, padx=2, pady=2)

    carid_ent = tk.Entry(detail_frame, bd=3, font=('arial', 12), textvariable=car_id)
    carid_ent.grid(row=0, column=1, padx=2, pady=2)

    carmake_lbl = tk.Label(detail_frame, text="Car Make", font=('Arial', 12), bg="lightgrey")
    carmake_lbl.grid(row=1, column=0, padx=2, pady=2)

    carmake_ent = tk.Entry(detail_frame, bd=3, font=('arial', 12), textvariable=car_make)
    carmake_ent.grid(row=1, column=1, padx=2, pady=2)

    carmodel_lbl = tk.Label(detail_frame, text="Car Model", font=('Arial', 12), bg="lightgrey")
    carmodel_lbl.grid(row=2, column=0, padx=2, pady=2)

    carmodel_ent = tk.Entry(detail_frame, bd=3, font=('arial', 12), textvariable=car_model)
    carmodel_ent.grid(row=2, column=1, padx=2, pady=2)

    year_manufactured_lbl = tk.Label(detail_frame, text="Year Manufactured", font=('Arial', 12), bg="lightgrey")
    year_manufactured_lbl.grid(row=3, column=0, padx=2, pady=2)

    year_manufactured_ent = tk.Entry(detail_frame, bd=3, font=('arial', 12), textvariable=year_manufactured)
    year_manufactured_ent.grid(row=3, column=1, padx=2, pady=2)

    car_color_lbl = tk.Label(detail_frame, text="Car Color", font=('Arial', 12), bg="lightgrey")
    car_color_lbl.grid(row=4, column=0, padx=2, pady=2)

    car_color_ent = tk.Entry(detail_frame, bd=3, font=('arial', 12), textvariable=car_color)
    car_color_ent.grid(row=4, column=1, padx=2, pady=2)

    carnumber_lbl = tk.Label(detail_frame, text="Car Number", font=('Arial', 12), bg="lightgrey")
    carnumber_lbl.grid(row=5, column=0, padx=2, pady=2)

    carnumber_ent = tk.Entry(detail_frame, bd=3, font=('arial', 12), textvariable=car_number)
    carnumber_ent.grid(row=5, column=1, padx=2, pady=2)

    carmilage_lbl = tk.Label(detail_frame, text="Car Milage", font=('Arial', 12), bg="lightgrey")
    carmilage_lbl.grid(row=6, column=0, padx=2, pady=2)

    carmilage_ent = tk.Entry(detail_frame, bd=3, font=('arial', 12), textvariable=car_milage)
    carmilage_ent.grid(row=6, column=1, padx=2, pady=2)

    carcharge_lbl = tk.Label(detail_frame, text="Charge Per Day", font=('Arial', 12), bg="lightgrey")
    carcharge_lbl.grid(row=7, column=0, padx=2, pady=2)

    carcharge_ent = tk.Entry(detail_frame, bd=3, font=('arial', 12), textvariable=charge_per_day)
    carcharge_ent.grid(row=7, column=1, padx=2, pady=2)

    car_availability_lbl = tk.Label(detail_frame, text="Car Availability", font=('Arial', 12), bg="lightgrey")
    car_availability_lbl.grid(row=8, column=0, padx=2, pady=2)

    car_availability_ent = ttk.Combobox(detail_frame, font=('arial', 12), textvariable=car_availability)
    car_availability_ent['values'] = ('Yes', 'No')
    car_availability_ent.grid(row=8, column=1, padx=2, pady=2)

    #====Functions DB=======

    def car_fetch_data():
        conn = sqlite3.connect("database.db")  # Connect to SQLite database
        curr = conn.cursor()
        curr.execute("SELECT * FROM car")
        rows = curr.fetchall()

        if len(rows) > 0:
            car_table.delete(*car_table.get_children())  # Clear existing data
            for row in rows:
                car_table.insert("", "end", values=row)  # Insert fetched data into Treeview

        conn.close()  # Close the connection

    def car_add_func():
        if car_id.get() == "" or car_make.get() == "" or car_model.get() == "" or car_number.get() == "" or car_milage.get() == "" or charge_per_day.get() == "" or car_availability.get() == "" or year_manufactured.get() == "" or car_color.get() == "":
            messagebox.showerror("Error!", "Please fill all the fields!", parent=new_window)

        else:
            try:
                conn = sqlite3.connect("database.db")  # Connect to SQLite database
                curr = conn.cursor()

                # Insert data into SQLite table
                curr.execute("INSERT INTO car VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                             (car_id.get(), car_make.get(), car_model.get(), year_manufactured.get(), car_number.get(),
                              car_milage.get(), charge_per_day.get(), car_availability.get(), car_color.get()))

                conn.commit()  # Commit the transaction
                car_fetch_data()  # Update the UI by fetching the new data

            except sqlite3.IntegrityError:
                messagebox.showerror("Error", "Car ID already exists!", parent=new_window)
            except sqlite3.Error as e:
                messagebox.showerror("Database Error", f"Error occurred: {e}", parent=new_window)
            finally:
                conn.close()  # Ensure connection is always closed

    def get_cursor(event):  # this function will fetch data of selected row.
        cursor_row = car_table.focus()
        content = car_table.item(cursor_row)
        row = content['values']
        car_id.set(row[0])
        car_make.set(row[1])
        car_model.set(row[2])
        year_manufactured.set(row[3])  # Set the new field
        car_number.set(row[4])
        car_milage.set(row[5])
        charge_per_day.set(row[6])
        car_availability.set(row[7])
        car_color.set(row[8])  # Set the new field

    def clear():  # this function will clear the entry boxes
        car_id.set("")
        car_make.set("")
        car_model.set("")
        year_manufactured.set("")  # Clear the new field
        car_number.set("")
        car_milage.set("")
        charge_per_day.set("")
        car_availability.set("")
        car_color.set("")  # Clear the new field

    def car_update_func():
        """This function will update data according to user"""

        if car_id.get() == "":
            messagebox.showerror("Error!", "Car ID is required for updating!", parent=new_window)
            return

        try:
            conn = sqlite3.connect("database.db")  # Connect to SQLite database
            curr = conn.cursor()

            # Update query for SQLite
            curr.execute("""
                            UPDATE car
                            SET car_make = ?, car_model = ?, year_manufactured = ?, car_number = ?, car_milage = ?, charge_per_day = ?, car_availability = ?, car_color = ?
                            WHERE car_id = ?
                        """, (car_make.get(), car_model.get(), year_manufactured.get(), car_number.get(),
                              car_milage.get(), charge_per_day.get(), car_availability.get(), car_color.get(), car_id.get()))

            conn.commit()  # Commit the transaction

            car_fetch_data()  # Fetch updated data to refresh the UI
            clear()  # Clear the input fields
            messagebox.showinfo("Success", "Record updated successfully!", parent=new_window)

        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Error occurred: {e}", parent=new_window)

        finally:
            conn.close()  # Ensure the connection is closed

    def car_delete_func():
        """This function will delete a car record based on car_id"""

        if car_id.get() == "":
            messagebox.showerror("Error!", "Car ID is required for deletion!",
                                 parent=root)  # Ensure message box is inside the window
            return

        # Ask for confirmation before deleting
        confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this record?", parent=new_window)
        if not confirm:
            return  # If user selects 'No', do nothing

        try:
            conn = sqlite3.connect("database.db")  # Connect to SQLite database
            curr = conn.cursor()

            # Execute delete query
            curr.execute("DELETE FROM car WHERE car_id = ?", (car_id.get(),))

            conn.commit()  # Commit the transaction

            car_fetch_data()  # Refresh the UI after deletion
            clear()  # Clear the input fields
            messagebox.showinfo("Success", "Record deleted successfully!", parent=new_window)  # Success message

        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Error occurred: {e}", parent=new_window)  # Error message

        finally:
            conn.close()  # Ensure the connection is closed

    def car_search_func():
        """Search for a car by its ID or Make"""
        search_query = search_by.get().strip()  # Get the search input and remove extra spaces

        if search_query == "":
            messagebox.showerror("Error!", "Please enter a Car ID or Car Model to search!", parent=new_window)
            return

        try:
            conn = sqlite3.connect("database.db")  # Connect to the database
            curr = conn.cursor()

            # Search query: Check if the input is numeric (assume it's an ID), otherwise, search by name
            if search_query.isdigit():
                curr.execute("SELECT * FROM car WHERE car_id = ?", (search_query,))
            else:
                curr.execute("SELECT * FROM car WHERE car_model LIKE ?", ('%' + search_query + '%',))

            rows = curr.fetchall()

            # Clear existing data in the table
            car_table.delete(*car_table.get_children())

            # Display search results
            if rows:
                for row in rows:
                    car_table.insert("", tk.END, values=row)
            else:
                messagebox.showinfo("No Results", "No matching records found!", parent=new_window)

            conn.close()

        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Error occurred: {e}", parent=new_window)

    #=======Buttons=========

    btn_frame = tk.Frame(detail_frame, bg="lightblue", bd=1, relief=tk.GROOVE)
    btn_frame.place(x=18, y=350, width=340, height=120)  # Adjusted y position for new fields

    add_btn = tk.Button(btn_frame, bg='lightgreen', text="Add", font=('arial', 12), width=17, command=car_add_func)
    add_btn.grid(row=0, column=0, padx=2, pady=2)

    update_btn = tk.Button(btn_frame, bg='lightyellow', text="Update", font=('arial', 12), width=17, command=car_update_func)
    update_btn.grid(row=0, column=1, padx=3, pady=2)

    delete_btn = tk.Button(btn_frame, bg='orange', text="Delete", font=('arial', 12), width=17, command=car_delete_func)
    delete_btn.grid(row=1, column=0, padx=2, pady=2)

    clear_btn = tk.Button(btn_frame, bg='lightgrey', text="Clear", font=('arial', 12), width=17, command=clear)
    clear_btn.grid(row=1, column=1, padx=3, pady=2)

    back_btn = tk.Button(btn_frame, text="Back", font=("Arial", 12, "bold"), bg="#ff4500", fg="white",width=10,command=new_window.destroy)
    back_btn.grid(row=2, column=0, columnspan=2, padx=3, pady=2)  # Span across both columns

    #======Search=========

    search_frame = tk.Frame(data_frame, bg='lightblue', bd=1, relief=tk.GROOVE)
    search_frame.pack(side=tk.TOP, fill=tk.X)

    search_lbl = tk.Label(search_frame, text="Search (id/model)", bg='lightgrey', font=('arial', 12))
    search_lbl.grid(row=0, column=0, padx=12, pady=2)

    search_in = tk.Entry(search_frame, font=("Arial", 14), textvariable=search_by)
    search_in.grid(row=0, column=1, padx=12, pady=2)

    search_btn = tk.Button(search_frame, bg='lightgreen', text="Search", font=('arial', 12), width=10, command=car_search_func)
    search_btn.grid(row=0, column=2, padx=12, pady=2)

    showall_btn = tk.Button(search_frame, bg='lightgreen', text="Show All", font=('arial', 12), width=10, command=car_fetch_data)
    showall_btn.grid(row=0, column=3, padx=12, pady=2)

    #====Database Frame=======

    main_frame = tk.Frame(data_frame, bg="lightgrey", bd=2, relief=tk.GROOVE)
    main_frame.pack(fill=tk.BOTH, expand=True)

    y_scroll = tk.Scrollbar(main_frame, orient=tk.VERTICAL)
    x_scroll = tk.Scrollbar(main_frame, orient=tk.HORIZONTAL)

    car_table = ttk.Treeview(main_frame, columns=("Car ID", "Car Make", "Car Model", "Year Manufactured", "Car Number", "Car Milage", "Charge Per Day", "Car Availability", "Car Color"), yscrollcommand=y_scroll.set, xscrollcommand=x_scroll.set)

    y_scroll.config(command=car_table.yview)
    x_scroll.config(command=car_table.xview)

    y_scroll.pack(side=tk.RIGHT, fill=tk.Y)
    x_scroll.pack(side=tk.BOTTOM, fill=tk.X)

    car_table.heading("Car ID", text="Car ID")
    car_table.heading("Car Make", text="Car Make")
    car_table.heading("Car Model", text="Car Model")
    car_table.heading("Year Manufactured", text="Year Manufactured")
    car_table.heading("Car Number", text="Car Number")
    car_table.heading("Car Milage", text="Car Milage")
    car_table.heading("Charge Per Day", text="Charge Per Day")
    car_table.heading("Car Availability", text="Car Availability")
    car_table.heading("Car Color", text="Car Color")

    car_table['show'] = 'headings'

    car_table.column("Car ID", width=100)
    car_table.column("Car Make", width=100)
    car_table.column("Car Model", width=100)
    car_table.column("Year Manufactured", width=150)
    car_table.column("Car Number", width=100)
    car_table.column("Car Milage", width=100)
    car_table.column("Charge Per Day", width=100)
    car_table.column("Car Availability", width=100)
    car_table.column("Car Color", width=100)

    car_table.pack(fill=tk.BOTH, expand=True)
    car_fetch_data()
    car_table.bind("<ButtonRelease-1>", get_cursor)

    footer_frame = tk.Frame(new_window, bg="#4682b4", pady=10)
    footer_frame.pack(side=tk.BOTTOM, fill=tk.X)

    footer_label = tk.Label(
        footer_frame,
        text="© 2025 Car Rental System - Nuvin Amarasinghe",
        font=("Arial", 10, "italic"),
        fg="white",
        bg="#4682b4"
    )
    footer_label.pack()


def customer_management():
    new_window = tk.Toplevel(root)
    new_window.geometry(f"{width}x{height}+{left}+{top}")
    new_window.title("Customer Management")
    new_window.resizable(False, False)

    new_window.iconbitmap("Logo.ico")

    # Load the background image
    try:
        bg_image = Image.open("function_bg.jpg")  # Replace with your actual image path
        bg_image = bg_image.resize((width, height), Image.LANCZOS)  # Resize to fit the window
        bg_photo = ImageTk.PhotoImage(bg_image)

        # Create a label to hold the background image
        bg_label = tk.Label(new_window, image=bg_photo)
        bg_label.image = bg_photo  # Keep a reference to avoid garbage collection
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)  # Fill the entire window
    except Exception as e:
        print(f"Error loading background image: {e}")

    title_label = tk.Label(new_window, text="User Management", font=("Arial", 18, "bold"))
    title_label.pack(pady=20)


    detail_frame = tk.LabelFrame(new_window, text="Enter Details", font=("Arial", 15), bg="lightgrey")
    detail_frame.place(x=20, y=80, width=420, height=600)

    data_frame = tk.Frame(new_window, bd=12, bg="lightgrey")
    data_frame.place(x=475, y=90, width=700, height=575)

    # Variables
    user_id = tk.StringVar()
    username = tk.StringVar()
    password = tk.StringVar()
    full_name = tk.StringVar()
    user_email = tk.StringVar()
    user_phone_no = tk.StringVar()
    nic_no = tk.StringVar()
    search_by = tk.StringVar()

    # Entry Fields
    labels = ["User ID", "Username", "Password", "Full Name", "Email", "Phone No", "NIC No"]
    variables = [user_id, username, password, full_name, user_email, user_phone_no, nic_no]

    for i, (label_text, var) in enumerate(zip(labels, variables)):
        label = tk.Label(detail_frame, text=label_text, font=('Arial', 12), bg="lightgrey")
        label.grid(row=i, column=0, padx=2, pady=2)
        entry = tk.Entry(detail_frame, bd=3, font=('Arial', 12), textvariable=var)
        entry.grid(row=i, column=1, padx=2, pady=2)

    # Database Functions
    def user_fetch_data():
        conn = sqlite3.connect("database.db")
        curr = conn.cursor()
        curr.execute("SELECT * FROM users")
        rows = curr.fetchall()
        if rows:
            user_table.delete(*user_table.get_children())
            for row in rows:
                user_table.insert("", "end", values=row)
        conn.close()

    def user_add_func():
        if any(var.get() == "" for var in variables):
            messagebox.showerror("Error!", "Please fill all the fields!", parent=new_window)
        else:
            try:
                conn = sqlite3.connect("database.db")
                curr = conn.cursor()
                curr.execute("INSERT INTO users VALUES (?, ?, ?, ?, ?, ?, ?)",
                             (user_id.get(), username.get(), password.get(), full_name.get(),
                              user_email.get(), user_phone_no.get(), nic_no.get()))
                conn.commit()
                user_fetch_data()
            except sqlite3.IntegrityError:
                messagebox.showerror("Error", "User ID already exists!", parent=new_window)
            finally:
                conn.close()

    def get_cursor(event):
        cursor_row = user_table.focus()
        content = user_table.item(cursor_row)
        row = content['values']
        for var, value in zip(variables, row):
            var.set(value)

    def clear():
        for var in variables:
            var.set("")

    def user_update_func():
        if user_id.get() == "":
            messagebox.showerror("Error!", "User ID is required for updating!", parent=new_window)
            return
        try:
            conn = sqlite3.connect("database.db")
            curr = conn.cursor()
            curr.execute("""
                UPDATE users
                SET username = ?, password = ?, full_name = ?, user_email = ?, user_phone_no = ?, nic_no = ?
                WHERE user_id = ?
            """, (username.get(), password.get(), full_name.get(), user_email.get(), user_phone_no.get(), nic_no.get(), user_id.get()))
            conn.commit()
            user_fetch_data()
            clear()
            messagebox.showinfo("Success", "Record updated successfully!", parent=new_window)
        finally:
            conn.close()

    def user_delete_func():
        if user_id.get() == "":
            messagebox.showerror("Error!", "User ID is required for deletion!", parent=new_window)
            return
        confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this record?", parent=new_window)
        if confirm:
            try:
                conn = sqlite3.connect("database.db")
                curr = conn.cursor()
                curr.execute("DELETE FROM users WHERE user_id = ?", (user_id.get(),))
                conn.commit()
                user_fetch_data()
                clear()
                messagebox.showinfo("Success", "Record deleted successfully!", parent=new_window)
            finally:
                conn.close()

    def user_search_func():
        search_query = search_by.get().strip()
        if search_query == "":
            messagebox.showerror("Error!", "Please enter a User ID or Username to search!", parent=new_window)
            return
        try:
            conn = sqlite3.connect("database.db")
            curr = conn.cursor()
            curr.execute("SELECT * FROM users WHERE user_id = ? OR username LIKE ?", (search_query, '%' + search_query + '%'))
            rows = curr.fetchall()
            user_table.delete(*user_table.get_children())
            for row in rows:
                user_table.insert("", tk.END, values=row)
            conn.close()
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Error occurred: {e}", parent=new_window)

    # Buttons
    btn_frame = tk.Frame(detail_frame, bg="lightblue", bd=1, relief=tk.GROOVE)
    btn_frame.place(x=18, y=390, width=340, height=120)

    add_btn = tk.Button(btn_frame, bg='lightgreen', text="Add", font=('arial', 12), width=17, command=user_add_func)
    add_btn.grid(row=0, column=0, padx=2, pady=2)

    update_btn = tk.Button(btn_frame, bg='lightyellow', text="Update", font=('arial', 12), width=17,command=user_update_func)
    update_btn.grid(row=0, column=1, padx=3, pady=2)

    delete_btn = tk.Button(btn_frame, bg='orange', text="Delete", font=('arial', 12), width=17, command=user_delete_func)
    delete_btn.grid(row=1, column=0, padx=2, pady=2)

    clear_btn = tk.Button(btn_frame, bg='lightgrey', text="Clear", font=('arial', 12), width=17, command=clear)
    clear_btn.grid(row=1, column=1, padx=3, pady=2)

    back_btn = tk.Button(btn_frame, text="Back", font=("Arial", 12, "bold"), bg="#ff4500", fg="white",width=10,command=new_window.destroy)
    back_btn.grid(row=2, column=0, columnspan=2, padx=3, pady=2)  # Span across both columns

    # Search and Table
    search_frame = tk.Frame(data_frame, bg='lightblue', bd=1, relief=tk.GROOVE)
    search_frame.pack(side=tk.TOP, fill=tk.X)

    search_lbl =  tk.Label(search_frame,text="Search (id/username)",bg='lightgrey',font=('arial',12))
    search_lbl.grid(row=0,column=0,padx=12,pady=2)


    tk.Entry(search_frame, font=("Arial", 14), textvariable=search_by).grid(row=0, column=1, padx=12, pady=2)
    tk.Button(search_frame, text="Search", font=('arial', 12), width=10,bg="lightgreen", command=user_search_func).grid(row=0, column=2, padx=12, pady=2)
    showall_btn = tk.Button(search_frame, bg='lightgreen', text="Show All", font=('arial', 12), width=10,command=user_fetch_data)
    showall_btn.grid(row=0, column=3, padx=12, pady=2)
    user_table = ttk.Treeview(data_frame, columns=labels, show='headings')
    for col in labels:
        user_table.heading(col, text=col)
        user_table.column(col, width=100)
    user_table.pack(fill=tk.BOTH, expand=True)
    user_table.bind("<ButtonRelease-1>", get_cursor)
    user_fetch_data()

    footer_frame = tk.Frame(new_window, bg="#4682b4", pady=10)
    footer_frame.pack(side=tk.BOTTOM, fill=tk.X)

    footer_label = tk.Label(
        footer_frame,
        text="© 2025 Car Rental System - Nuvin Amarasinghe",
        font=("Arial", 10, "italic"),
        fg="white",
        bg="#4682b4"
    )
    footer_label.pack()



def rental():
    new_window = tk.Toplevel(root)
    new_window.geometry(f"{width}x{height}+{left}+{top}")
    new_window.title("Rental Management")
    new_window.resizable(False, False)

    new_window.iconbitmap("Logo.ico")

    # Load the background image
    try:
        bg_image = Image.open("function_bg.jpg")  # Replace with your actual image path
        bg_image = bg_image.resize((width, height), Image.LANCZOS)  # Resize to fit the window
        bg_photo = ImageTk.PhotoImage(bg_image)

        # Create a label to hold the background image
        bg_label = tk.Label(new_window, image=bg_photo)
        bg_label.image = bg_photo  # Keep a reference to avoid garbage collection
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)  # Fill the entire window
    except Exception as e:
        print(f"Error loading background image: {e}")

    title_label = tk.Label(new_window, text="Rental Management", font=("Arial", 18, "bold"))
    title_label.pack(pady=20)

    detail_frame = tk.LabelFrame(new_window, text="Enter Details", font=("Arial", 15), bg="lightgrey")
    detail_frame.place(x=20, y=80, width=420, height=650)

    data_frame = tk.Frame(new_window, bd=12, bg="lightgrey")
    data_frame.place(x=475, y=80, width=700, height=580)


    # Variables
    rental_id = tk.StringVar()
    car_id = tk.StringVar()
    user_id = tk.StringVar()
    rental_date = tk.StringVar()
    return_date = tk.StringVar()
    day_count = tk.StringVar()
    rental_fee = tk.StringVar()
    payment_status = tk.StringVar()
    paid_amount = tk.StringVar()
    amount_to_be_payed = tk.StringVar()

    search_by = tk.StringVar()


    def update_day_count(*args):
        try:
            rental_date_value = rental_date.get()
            return_date_value = return_date.get()

            if rental_date_value and return_date_value:
                rental_date_obj = datetime.strptime(rental_date_value, "%Y-%m-%d")
                return_date_obj = datetime.strptime(return_date_value, "%Y-%m-%d")
                day_difference = (return_date_obj - rental_date_obj).days

                # Update the day count variable
                day_count.set(day_difference if day_difference >= 0 else 0)  # Ensure non-negative day count
            else:
                day_count.set("")  # Clear if either date is empty
        except ValueError:
            day_count.set("")  # Clear if there's a value error

    rentalid_lbl = tk.Label(detail_frame, text="Rental Id", font=('Arial', 12), bg="lightgrey")
    rentalid_lbl.grid(row=0, column=0, padx=2, pady=2)

    rentalid_ent = tk.Entry(detail_frame, bd=3, font=('arial', 12), textvariable=rental_id)
    rentalid_ent.grid(row=0, column=1, padx=2, pady=2)

    carid_lbl = tk.Label(detail_frame, text="Car Id", font=('Arial', 12), bg="lightgrey")
    carid_lbl.grid(row=1, column=0, padx=2, pady=2)

    car_id_combo = ttk.Combobox(detail_frame, font=('Arial', 12), textvariable=car_id)
    car_id_combo.grid(row=1, column=1, padx=2, pady=2)

    userid_lbl = tk.Label(detail_frame, text="User Id", font=('Arial', 12), bg="lightgrey")
    userid_lbl.grid(row=2, column=0, padx=2, pady=2)

    userid_ent = tk.Entry(detail_frame, bd=3, font=('arial', 12), textvariable=user_id)
    userid_ent.grid(row=2, column=1, padx=2, pady=2)

    # Rental Date Label and Entry
    rentaldate_lbl = tk.Label(detail_frame, text="Rental Date", font=('Arial', 12), bg="lightgrey")
    rentaldate_lbl.grid(row=3, column=0, padx=2, pady=2)

    rental_date_entry = DateEntry(detail_frame, font=("Arial", 12), textvariable=rental_date, date_pattern="yyyy-mm-dd",
                                  width=18)
    rental_date_entry.grid(row=3, column=1, padx=2, pady=2)
    rental_date.trace_add("write", update_day_count)  # Bind update function

    # Return Date Label and Entry
    return_date_lbl = tk.Label(detail_frame, text="Return Date", font=('Arial', 12), bg="lightgrey")
    return_date_lbl.grid(row=4, column=0, padx=2, pady=2)

    return_date_entry = DateEntry(detail_frame, font=("Arial", 12), textvariable=return_date, date_pattern="yyyy-mm-dd",
                                  width=18)
    return_date_entry.grid(row=4, column=1, padx=2, pady=2)
    return_date.trace_add("write", update_day_count)  # Bind update function

    # Day Count Label and Entry
    daycount_lbl = tk.Label(detail_frame, text="Day Count", font=('Arial', 12), bg="lightgrey")
    daycount_lbl.grid(row=5, column=0, padx=2, pady=2)

    daycount_ent = tk.Entry(detail_frame, bd=3, font=('arial', 12), textvariable=day_count)
    daycount_ent.grid(row=5, column=1, padx=2, pady=2)


    daycount_lbl = tk.Label(detail_frame, text="Day Count", font=('Arial', 12), bg="lightgrey")
    daycount_lbl.grid(row=5, column=0, padx=2, pady=2)

    daycount_ent = tk.Entry(detail_frame, bd=3, font=('arial', 12), textvariable=day_count)
    daycount_ent.grid(row=5, column=1, padx=2, pady=2)

    rentalfee_lbl = tk.Label(detail_frame, text="Rental Fee", font=('Arial', 12), bg="lightgrey")
    rentalfee_lbl.grid(row=6, column=0, padx=2, pady=2)

    rentalfee_ent = tk.Entry(detail_frame, bd=3, font=('arial', 12), textvariable=rental_fee)
    rentalfee_ent.grid(row=6, column=1, padx=2, pady=2)

    paidamount_lbl = tk.Label(detail_frame, text="Paid Amount", font=('Arial', 12), bg="lightgrey")
    paidamount_lbl.grid(row=7, column=0, padx=2, pady=2)

    paidamount_ent = tk.Entry(detail_frame, bd=3, font=('arial', 12), textvariable=paid_amount)
    paidamount_ent.grid(row=7, column=1, padx=2, pady=2)

    payment_status_lbl = tk.Label(detail_frame, text="Payment Status", font=('Arial', 12), bg="lightgrey")
    payment_status_lbl.grid(row=8, column=0, padx=2, pady=2)

    payment_status_ent = ttk.Combobox(detail_frame, font=('arial', 12), textvariable=payment_status)
    payment_status_ent['values'] = ('Done', 'Not Done')
    payment_status_ent.grid(row=8, column=1, padx=2, pady=2)

    amount_tobe_payed_lbl = tk.Label(detail_frame, text="Amount To be Payed", font=('Arial', 12), bg="lightgrey")
    amount_tobe_payed_lbl.grid(row=9, column=0, padx=2, pady=2)

    amount_tobe_payed_ent = tk.Entry(detail_frame, bd=3, font=('arial', 12), textvariable=amount_to_be_payed)
    amount_tobe_payed_ent.grid(row=9, column=1, padx=2, pady=2)



    def load_car_ids():
        conn = sqlite3.connect("database.db")
        curr = conn.cursor()
        curr.execute("SELECT car_id FROM car WHERE car_availability ='Yes'")
        car_ids = [row[0] for row in curr.fetchall()]
        car_id_combo["values"] = car_ids
        conn.close()


    def update_rental_fee(*args):
        if car_id.get() and day_count.get().isdigit():
            conn = sqlite3.connect("database.db")
            curr = conn.cursor()
            curr.execute("SELECT charge_per_day FROM car WHERE car_id=?", (car_id.get(),))
            charge = curr.fetchone()
            if charge:
                rental_fee.set(int(charge[0]) * int(day_count.get()))
            conn.close()

    def update_amount_to_be_paid(*args):
        if rental_fee.get().isdigit() and paid_amount.get().isdigit():
            amount_to_be_payed.set(int(rental_fee.get()) - int(paid_amount.get()))

    car_id.trace("w", update_rental_fee)
    day_count.trace("w", update_rental_fee)
    rental_fee.trace("w", update_amount_to_be_paid)
    paid_amount.trace("w", update_amount_to_be_paid)

    load_car_ids()

    # Database Functions
    def rental_fetch_data():
        conn = sqlite3.connect("database.db")
        curr = conn.cursor()
        curr.execute("SELECT * FROM rental")
        rows = curr.fetchall()
        rental_table.delete(*rental_table.get_children())
        for row in rows:
            rental_table.insert("", "end", values=row)
        conn.close()

    variables = [rental_id, car_id, user_id, rental_date, return_date, day_count, rental_fee, paid_amount, amount_to_be_payed,
                 payment_status]

    def rental_add_func():
        if any(not var.get() for var in variables[:-1]):
            messagebox.showerror("Error!", "Please fill all required fields!", parent=new_window)
            return
        try:
            conn = sqlite3.connect("database.db")
            curr = conn.cursor()
            curr.execute("INSERT INTO rental VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                         (rental_id.get(), car_id.get(), user_id.get(), rental_date.get(), return_date.get(), day_count.get(), rental_fee.get(), paid_amount.get(), payment_status.get(), amount_to_be_payed.get()))
            curr.execute("UPDATE car SET car_availability = 'No' WHERE car_id = ?", (car_id.get()))
            conn.commit()
            rental_fetch_data()
            load_car_ids()
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Rental ID already exists!", parent=new_window)
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Error occurred: {e}", parent=new_window)
        finally:
            conn.close()

    def get_cursor(event): #this function will fetch data of selected row.
        cursor_row = rental_table.focus()
        content = rental_table.item(cursor_row)
        row = content['values']
        rental_id.set(row[0])
        car_id.set(row[1])
        user_id.set(row[2])
        rental_date.set(row[3])
        return_date.set(row[4])
        day_count.set(row[5])
        rental_fee.set(row[6])
        paid_amount.set(row[7])
        payment_status.set(row[8])
        amount_to_be_payed.set(row[9])

    def clear():# this function will clear the entry boxes
        rental_id.set("")
        car_id.set("")
        user_id.set("")
        rental_date.set("")
        return_date.set("")
        day_count.set("")
        rental_fee.set("")
        paid_amount.set("")
        payment_status.set("")
        amount_to_be_payed.set("")

    def rental_update_func():
        """This function will update data according to user"""

        if rental_id.get() == "":
            messagebox.showerror("Error!", "Rental ID is required for updating!", parent=new_window)
            return

        try:
            conn = sqlite3.connect("database.db")  # Connect to SQLite database
            curr = conn.cursor()

            # Update query for SQLite
            curr.execute("""
                            UPDATE rental
                            SET car_id = ?, user_id = ?, rental_date = ?, return_date = ?, day_count = ?, rental_fee = ?, paid_amount = ?, payment_status = ?, amount_tobe_payed = ?
                            WHERE rental_id = ?
                        """, (car_id.get(), user_id.get(), rental_date.get(), return_date.get(), day_count.get(),
                              rental_fee.get(), paid_amount.get(), payment_status.get(), amount_to_be_payed.get(),rental_id.get()))
            curr.execute("UPDATE car SET car_availability = 'No' WHERE car_id = ?", (car_id.get()))
            conn.commit()  # Commit the transaction

            rental_fetch_data()  # Fetch updated data to refresh the UI
            clear()  # Clear the input fields
            load_car_ids()
            messagebox.showinfo("Success", "Record updated successfully!", parent=new_window)

        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Error occurred: {e}", parent=new_window)

        finally:
            conn.close()  # Ensure the connection is closed

    def rental_delete_func():
        """This function will delete a car record based on car_id"""

        if rental_id.get() == "":
            messagebox.showerror("Error!", "Rental ID is required for deletion!",
                                 parent=new_window)  # Ensure message box is inside the window
            return

        # Ask for confirmation before deleting
        confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this record?",
                                      parent=new_window)
        if not confirm:
            return  # If user selects 'No', do nothing

        try:
            conn = sqlite3.connect("database.db")  # Connect to SQLite database
            curr = conn.cursor()

            # Execute delete query
            curr.execute("SELECT car_id FROM rental WHERE rental_id = ?", (rental_id.get(),))
            car_id = curr.fetchone()

            if car_id:
                curr.execute("DELETE FROM rental WHERE rental_id = ?", (rental_id.get(),))
                curr.execute("UPDATE car SET car_availability = 'Yes' WHERE car_id = ?", (car_id[0],))

            conn.commit()
            # Commit the transaction
            load_car_ids()
            rental_fetch_data()  # Refresh the UI after deletion
            clear()  # Clear the input fields
            messagebox.showinfo("Success", "Record deleted successfully!", parent=new_window)  # Success message

        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Error occurred: {e}", parent=new_window)  # Error message

        finally:
            conn.close()  # Ensure the connection is closed

    def rental_search_func():
        """Search for a car by its ID or Make"""
        search_query = search_by.get().strip()  # Get the search input and remove extra spaces

        if search_query == "":
            messagebox.showerror("Error!", "Please enter a Rental Id to !", parent=new_window)
            return

        try:
            conn = sqlite3.connect("database.db")  # Connect to the database
            curr = conn.cursor()

            # Search query: Check if the input is numeric (assume it's an ID), otherwise, search by name
            if search_query.isdigit():
                curr.execute("SELECT * FROM rental WHERE rental_id = ?", (search_query,))


            rows = curr.fetchall()

            # Clear existing data in the table
            rental_table.delete(*rental_table.get_children())

            # Display search results
            if rows:
                for row in rows:
                    rental_table.insert("", tk.END, values=row)
            else:
                messagebox.showinfo("No Results", "No matching records found!", parent=new_window)

            conn.close()

        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Error occurred: {e}", parent=new_window)

    #=====Buttons====
    # Buttons
    btn_frame = tk.Frame(detail_frame, bg="lightblue", bd=1, relief=tk.GROOVE)
    btn_frame.place(x=18, y=390, width=340, height=120)

    btn_frame = tk.Frame(detail_frame, bg="lightblue", bd=1, relief=tk.GROOVE)
    btn_frame.place(x=18, y=390, width=340, height=120)

    add_btn = tk.Button(btn_frame, bg='lightgreen', text="Add", font=('arial', 12), width=17, command=rental_add_func)
    add_btn.grid(row=0, column=0, padx=2, pady=2)

    update_btn = tk.Button(btn_frame, bg='lightyellow', text="Update", font=('arial', 12), width=17, command=rental_update_func)
    update_btn.grid(row=0, column=1, padx=3, pady=2)

    delete_btn = tk.Button(btn_frame, bg='orange', text="Delete", font=('arial', 12), width=17, command=rental_delete_func)
    delete_btn.grid(row=1, column=0, padx=2, pady=2)

    clear_btn = tk.Button(btn_frame, bg='lightgrey', text="Clear", font=('arial', 12), width=17, command=clear)
    clear_btn.grid(row=1, column=1, padx=3, pady=2)

    back_btn = tk.Button(btn_frame, text="Back", font=("Arial", 12, "bold"), bg="#ff4500", fg="white",width=10,command=new_window.destroy)
    back_btn.grid(row=2, column=0, columnspan=2, padx=3, pady=2)  # Span across both columns

    #=====search====
    search_frame = tk.Frame(data_frame,bg='lightblue',bd=1,relief=tk.GROOVE)
    search_frame.pack(side=tk.TOP,fill=tk.X)

    search_lbl =  tk.Label(search_frame,text="Search",bg='lightgrey',font=('arial',12))
    search_lbl.grid(row=0,column=0,padx=12,pady=2)

    search_in =  tk.Entry(search_frame, font=("Arial", 14), textvariable=search_by)
    search_in.grid(row=0, column=1, padx=12, pady=2)

    search_btn = tk.Button(search_frame,bg='lightgreen',text="Search",font=('arial',12),width=10,command=rental_search_func)
    search_btn.grid(row=0,column=2,padx=12,pady=2)

    showall_btn = tk.Button(search_frame,bg='lightgreen',text="Show All",font=('arial',12),width=10,command=rental_fetch_data)
    showall_btn.grid(row=0,column=3,padx=12,pady=2)

    #Database Frame+====
    main_frame = tk.Frame(data_frame,bg="lightgrey",bd=2,relief=tk.GROOVE)
    main_frame.pack(fill=tk.BOTH,expand=True)

    y_scroll = tk.Scrollbar(main_frame,orient=tk.VERTICAL)
    x_scroll = tk.Scrollbar(main_frame,orient=tk.HORIZONTAL)

    rental_table = ttk.Treeview(main_frame,columns=("Rental Id","Car Id","User Id","Rental Date","Return Date","Day Count","Rental Fee","Paid Amount","Payment Status","Amount to be Payed"),yscrollcommand=y_scroll.set,xscrollcommand =x_scroll.set)

    y_scroll.config(command=rental_table.yview)
    x_scroll.config(command=rental_table.xview)

    y_scroll.pack(side=tk.RIGHT,fill=tk.Y)
    x_scroll.pack(side=tk.BOTTOM,fill=tk.X)

    rental_table.heading("Rental Id",text="Rental Id")
    rental_table.heading("Car Id", text="Car Id")
    rental_table.heading("User Id", text="User Id")
    rental_table.heading("Rental Date", text="Rental Date")
    rental_table.heading("Return Date", text="Return Date")
    rental_table.heading("Day Count", text="Day Count")
    rental_table.heading("Rental Fee", text="Rental Fee")
    rental_table.heading("Paid Amount", text="Paid Amount")
    rental_table.heading("Payment Status", text="Payment Status")
    rental_table.heading("Amount to be Payed", text="Amount to be Payed")

    rental_table['show'] = 'headings'

    rental_table.column("Rental Id", width=100)
    rental_table.column("Car Id", width=100)
    rental_table.column("User Id", width=100)
    rental_table.column("Rental Date", width=100)
    rental_table.column("Return Date", width=100)
    rental_table.column("Day Count", width=100)
    rental_table.column("Rental Fee", width=100)
    rental_table.column("Paid Amount", width=100)
    rental_table.column("Payment Status", width=100)
    rental_table.column("Amount to be Payed", width=100)



    rental_table.pack(fill=tk.BOTH,expand=True)
    rental_fetch_data()
    rental_table.bind("<ButtonRelease-1>",get_cursor)

    footer_frame = tk.Frame(new_window, bg="#4682b4", pady=10)
    footer_frame.pack(side=tk.BOTTOM, fill=tk.X)

    footer_label = tk.Label(
        footer_frame,
        text="© 2025 Car Rental System - Nuvin Amarasinghe",
        font=("Arial", 10, "italic"),
        fg="white",
        bg="#4682b4"
    )
    footer_label.pack()



def return_car():
    new_window = tk.Toplevel(root)
    new_window.geometry(f"{width}x{height}+{left}+{top}")
    new_window.title("Return")
    new_window.resizable(False, False)
    new_window.iconbitmap("Logo.ico")

    # Load the background image
    try:
        bg_image = Image.open("function_bg.jpg")  # Replace with your actual image path
        bg_image = bg_image.resize((width, height), Image.LANCZOS)  # Resize to fit the window
        bg_photo = ImageTk.PhotoImage(bg_image)

        # Create a label to hold the background image
        bg_label = tk.Label(new_window, image=bg_photo)
        bg_label.image = bg_photo  # Keep a reference to avoid garbage collection
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)  # Fill the entire window
    except Exception as e:
        print(f"Error loading background image: {e}")

    title_label = tk.Label(new_window, text="Return Management", font=("Arial", 18, "bold"))
    title_label.pack(pady=20)


    detail_frame = tk.LabelFrame(new_window, text="Enter Details", font=("Arial", 15), bg="lightgrey")
    detail_frame.place(x=20, y=80, width=420, height=600)


    data_frame = tk.Frame(new_window,bd=12,bg="lightgrey")
    data_frame.place(x=475,y=90,width=700,height=575)


    # =======Variables=====
    return_id = tk.StringVar()
    rental_id = tk.StringVar()
    rental_date = tk.StringVar()
    return_date_str = tk.StringVar()  # Renamed to avoid conflict
    overdue_days = tk.StringVar()
    amount_tobe_payed = tk.StringVar()
    day_count = tk.StringVar()  # Not appear in db

    search_by = tk.StringVar()

    # Database Connection
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    # Fetch rental IDs
    cursor.execute("SELECT rental_id FROM rental WHERE payment_status = 'Not Done'")
    rental_ids = [str(row[0]) for row in cursor.fetchall()]

    conn.close()

    # =====Entry Fields=======

    returnid_lbl = tk.Label(detail_frame, text="Return Id", font=('Arial', 12), bg="lightgrey")
    returnid_lbl.grid(row=0, column=0, padx=2, pady=2)

    returnid_ent = tk.Entry(detail_frame, font=('Arial', 12), textvariable=return_id)
    returnid_ent.grid(row=0, column=1, padx=2, pady=2)

    rentalid_lbl = tk.Label(detail_frame, text="Rental Id", font=('Arial', 12), bg="lightgrey")
    rentalid_lbl.grid(row=1, column=0, padx=2, pady=2)

    rentalid_combo = ttk.Combobox(detail_frame, values=rental_ids, font=('Arial', 12), textvariable=rental_id,
                                  state="readonly")
    rentalid_combo.grid(row=1, column=1, padx=2, pady=2)

    rental_date_lbl = tk.Label(detail_frame, text="Rental Date", font=('Arial', 12), bg="lightgrey")
    rental_date_lbl.grid(row=2, column=0, padx=2, pady=2)

    rental_date_entry = DateEntry(detail_frame, font=("Arial", 12), textvariable=rental_date, date_pattern="yyyy-mm-dd",
                                  width=18, state="readonly")  # Set to readonly
    rental_date_entry.grid(row=2, column=1, padx=2, pady=2)

    returned_date_lbl = tk.Label(detail_frame, text="Returned Date", font=('Arial', 12), bg="lightgrey")
    returned_date_lbl.grid(row=3, column=0, padx=2, pady=2)

    returned_date_entry = DateEntry(detail_frame, font=("Arial", 12), textvariable=return_date_str,
                                    date_pattern="yyyy-mm-dd", width=18)
    returned_date_entry.grid(row=3, column=1, padx=2, pady=2)

    overdue_days_lbl = tk.Label(detail_frame, text="Overdue Days", font=('Arial', 12), bg="lightgrey")
    overdue_days_lbl.grid(row=4, column=0, padx=2, pady=2)

    overdue_days_ent = tk.Entry(detail_frame, bd=3, font=('Arial', 12), textvariable=overdue_days, state="readonly")
    overdue_days_ent.grid(row=4, column=1, padx=2, pady=2)

    amount_tobe_payed_lbl = tk.Label(detail_frame, text="Amount to be Paid", font=('Arial', 12), bg="lightgrey")
    amount_tobe_payed_lbl.grid(row=5, column=0, padx=2, pady=2)

    amount_tobe_payed_ent = tk.Entry(detail_frame, bd=3, font=('Arial', 12), textvariable=amount_tobe_payed,state="readonly")
    amount_tobe_payed_ent.grid(row=5, column=1, padx=2, pady=2)

    # Function to update rental date
    def update_rental_info(event):
        rental_id_value = rental_id.get()

        if rental_id_value:
            conn = sqlite3.connect("database.db")
            cursor = conn.cursor()

            # Fetch rental details
            cursor.execute("SELECT rental_date FROM rental WHERE rental_id=?", (rental_id_value,))
            result = cursor.fetchone()
            conn.close()

            if result:
                rental_date_str_value = result[0]
                rental_date.set(rental_date_str_value)  # Set the rental date in the entry

                # Clear the return date and day count when a new rental ID is selected
                return_date_str.set("")
                day_count.set("")

    # Function to calculate day count
    def update_day_count(*args):
        try:
            rental_date_value = rental_date.get()
            return_date_value = return_date_str.get()
            rental_id_value = rental_id.get()

            if rental_date_value and return_date_value and rental_id_value:
                rental_date_obj = datetime.strptime(rental_date_value, "%Y-%m-%d")
                return_date_obj = datetime.strptime(return_date_value, "%Y-%m-%d")

                # Calculate the actual rental duration
                day_difference = (return_date_obj - rental_date_obj).days
                day_count.set(day_difference if day_difference >= 0 else 0)

                # Fetch expected return duration from database
                conn = sqlite3.connect("database.db")
                cursor = conn.cursor()
                cursor.execute("SELECT day_count FROM rental WHERE rental_id=?", (rental_id_value,))
                result = cursor.fetchone()
                conn.close()

                if result:
                    expected_rental_days = result[0]  # Expected rental days from DB
                    overdue = max(0, day_difference - expected_rental_days)  # Ensure non-negative overdue days
                    overdue_days.set(overdue)
                else:
                    overdue_days.set("")

            else:
                day_count.set("")
                overdue_days.set("")

        except ValueError:
            day_count.set("")
            overdue_days.set("")

    def calculate_amount_to_be_paid(*args):
        try:
            rental_id_value = rental_id.get()
            overdue_days_value = overdue_days.get()

            if rental_id_value and overdue_days_value:
                conn = sqlite3.connect("database.db")
                cursor = conn.cursor()

                # Fetch rental amount from database
                cursor.execute("SELECT amount_tobe_payed FROM rental WHERE rental_id=?", (rental_id_value,))
                result = cursor.fetchone()
                conn.close()

                if result:
                    base_amount = int(result[0])  # Convert from string to integer
                    overdue_fee = int(overdue_days_value) * 1000  # Overdue fine calculation
                    total_amount = base_amount + overdue_fee  # Final amount calculation

                    amount_tobe_payed.set(str(total_amount))  # Convert back to string for Tkinter
                else:
                    amount_tobe_payed.set("")

            else:
                amount_tobe_payed.set("")

        except ValueError:
            amount_tobe_payed.set("")

    # Function to update rental date and calculate overdue days





    # Bind the update function to rental_id selection
    rentalid_combo.bind("<<ComboboxSelected>>", update_rental_info)

    # Bind the update_day_count function to the return date entry
    returned_date_entry.bind("<<DateEntrySelected>>", update_day_count)

    overdue_days.trace_add("write", calculate_amount_to_be_paid)


    def return_fetch_data():
        conn = sqlite3.connect("database.db")  # Connect to SQLite database
        curr = conn.cursor()
        curr.execute("SELECT * FROM return")
        rows = curr.fetchall()

        if len(rows) > 0:
            return_table.delete(*return_table.get_children())  # Clear existing data
            for row in rows:
                return_table.insert("", "end", values=row)  # Insert fetched data into Treeview

    def return_add_func():
        if (return_id.get() == "" or rental_id.get() == "" or rental_date.get() == "" or
                return_date_str.get() == "" or amount_tobe_payed.get() == ""):
            messagebox.showerror("Error!", "Please fill all the fields!", parent=new_window)
        else:
            try:
                conn = sqlite3.connect("database.db")  # Connect to SQLite database
                curr = conn.cursor()

                # Insert data into the return table
                curr.execute(
                    "INSERT INTO return (return_id, rental_id, rental_date, returned_date, overdue_days, amount_tobe_payed) VALUES (?, ?, ?, ?, ?, ?)",
                    (return_id.get(), rental_id.get(), rental_date.get(), return_date_str.get(), overdue_days.get(),
                     float(amount_tobe_payed.get())))  # Ensure numeric value if needed

                # Update the payment_status in the rental table
                curr.execute(
                    "UPDATE rental SET payment_status = ? WHERE rental_id = ?",
                    ("Done", rental_id.get())
                )

                curr.execute("UPDATE rental SET paid_amount = ? WHERE rental_id = ?",
                             (amount_tobe_payed.get(), rental_id.get()))
                curr.execute("UPDATE rental SET amount_tobe_payed = ? WHERE rental_id = ?", (0, rental_id.get()))

                # Fetch the car_id associated with the rental_id
                curr.execute("SELECT car_id FROM rental WHERE rental_id = ?", (rental_id.get(),))
                car_id_row = curr.fetchone()
                if car_id_row:
                    car_id = car_id_row[0]
                    # Update car availability to "Yes"
                    curr.execute("UPDATE car SET car_availability = 'Yes' WHERE car_id = ?", (car_id,))

                conn.commit()  # Commit the transaction
                return_fetch_data()  # Update the UI by fetching new data
                messagebox.showinfo("Success", "Return record added successfully!", parent=new_window)

            except sqlite3.Error as e:
                messagebox.showerror("Database Error", f"An error occurred: {e}", parent=new_window)

            finally:
                conn.close()  # Ensure the connection is closed properly
    def get_cursor(event): #this function will fetch data of selected row.
        cursor_row = return_table.focus()
        content = return_table.item(cursor_row)
        row = content['values']
        return_id.set(row[0])
        rental_id.set(row[1])
        rental_date.set(row[2])
        return_date_str.set(row[3])
        overdue_days.set(row[4])
        amount_tobe_payed.set(row[5])


    def clear():# this function will clear the entry boxes
        return_id.set("")
        rental_id.set("")
        rental_date.set("")
        return_date_str.set("")
        overdue_days.set("")
        amount_tobe_payed.set("")

    def return_update_func():
        """This function will update data according to user"""

        if return_id.get() == "":
            messagebox.showerror("Error!", "Return ID is required for updating!", parent=new_window)
            return

        try:
            conn = sqlite3.connect("database.db")  # Connect to SQLite database
            curr = conn.cursor()

            # Update query for SQLite
            curr.execute("""
                             UPDATE return
                             SET rental_id = ?, rental_date = ?, returned_date = ?, overdue_days = ?, amount_tobe_payed = ?
                             WHERE return_id = ?
                         """, (rental_id.get(), rental_date.get(), return_date_str.get(), overdue_days.get(),
                               amount_tobe_payed.get(), return_id.get()))

            conn.commit()  # Commit the transaction

            return_fetch_data()  # Fetch updated data to refresh the UI
            clear()  # Clear the input fields
            messagebox.showinfo("Success", "Record updated successfully!", parent=new_window)

        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Error occurred: {e}", parent=new_window)

        finally:
            conn.close()  # Ensure the connection is closed

    def return_delete_func():
        """This function will delete a car record based on car_id"""

        if return_id.get() == "":
            messagebox.showerror("Error!", "Return ID is required for deletion!", parent=root)
            return

        # Ask for confirmation before deleting
        confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this record?",
                                      parent=new_window)
        if not confirm:
            return  # If user selects 'No', do nothing

        try:
            conn = sqlite3.connect("database.db")  # Connect to SQLite database
            curr = conn.cursor()

            # Execute delete query
            curr.execute("DELETE FROM return WHERE return_id = ?", (return_id.get(),))
            curr.execute(
                "UPDATE rental SET payment_status = ? WHERE rental_id = ?",
                ("Not Done", rental_id.get())
            )

            # Fetch the payed_amount from the rental table
            curr.execute("SELECT paid_amount FROM rental WHERE rental_id = ?", (rental_id.get(),))
            payed_amount_row = curr.fetchone()

            if payed_amount_row:
                payed_amount = payed_amount_row[0]
                # Update amount_to_be_paid and set payed_amount to 0
                curr.execute(
                    "UPDATE rental SET amount_tobe_payed = ?, paid_amount = ? WHERE rental_id = ?",
                    (payed_amount, 0, rental_id.get())
                )

            # Fetch the car_id to update car availability
            curr.execute("SELECT car_id FROM rental WHERE rental_id = ?", (rental_id.get(),))
            car_id_row = curr.fetchone()
            if car_id_row:
                car_id = car_id_row[0]
                # Update car availability to "Yes"
                curr.execute("UPDATE car SET car_availability = 'No' WHERE car_id = ?", (car_id,))

            conn.commit()  # Commit the transaction

            return_fetch_data()  # Refresh the UI after deletion
            clear()
            messagebox.showinfo("Success", "Record deleted successfully!", parent=new_window)  # Success message

        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Error occurred: {e}", parent=new_window)  # Error message

        finally:
            conn.close()  # Ensure the connection is closed

    def return_search_func():
        """Search for a return record by its ID"""
        search_query = search_by.get().strip()  # Get the search input and remove extra spaces

        if search_query == "":
            messagebox.showerror("Error!", "Please enter a Return ID to search!", parent=new_window)
            return

        try:
            conn = sqlite3.connect("database.db")  # Connect to the database
            curr = conn.cursor()

            # Ensure correct table name (rename if necessary)
            curr.execute('SELECT * FROM returns WHERE return_id = ?', (search_query,))  # Changed "return" to "returns"

            rows = curr.fetchall()  # Fetch the results

            if not rows:
                messagebox.showinfo("Not Found", "No return record found for the given ID.", parent=new_window)
            else:
                # Display or process the retrieved data
                for row in rows:
                    print(row)  # Replace this with your UI update logic

        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}", parent=new_window)

        finally:
            conn.close()  # Close the database connection

    # =======Buttons=========

    btn_frame = tk.Frame(detail_frame, bg="lightblue", bd=1, relief=tk.GROOVE)
    btn_frame.place(x=18, y=390, width=340, height=120)

    add_btn = tk.Button(btn_frame, bg='lightgreen', text="Add", font=('arial', 12), width=17, command=return_add_func)
    add_btn.grid(row=0, column=0, padx=2, pady=2)

    update_btn = tk.Button(btn_frame, bg='lightyellow', text="Update", font=('arial', 12), width=17,command=return_update_func)
    update_btn.grid(row=0, column=1, padx=3, pady=2)

    delete_btn = tk.Button(btn_frame, bg='orange', text="Delete", font=('arial', 12), width=17, command=return_delete_func)
    delete_btn.grid(row=1, column=0, padx=2, pady=2)

    clear_btn = tk.Button(btn_frame, bg='lightgrey', text="Clear", font=('arial', 12), width=17, command=clear)
    clear_btn.grid(row=1, column=1, padx=3, pady=2)

    back_btn = tk.Button(btn_frame, text="Back", font=("Arial", 12, "bold"), bg="#ff4500", fg="white",width=10,command=new_window.destroy)
    back_btn.grid(row=2, column=0, columnspan=2, padx=3, pady=2)  # Span across both columns

    #====search=======

    search_frame = tk.Frame(data_frame,bg='lightblue',bd=1,relief=tk.GROOVE)
    search_frame.pack(side=tk.TOP,fill=tk.X)

    search_lbl =  tk.Label(search_frame,text="Search",bg='lightgrey',font=('arial',12))
    search_lbl.grid(row=0,column=0,padx=12,pady=2)

    search_in =  tk.Entry(search_frame, font=("Arial", 14), textvariable=search_by)
    search_in.grid(row=0, column=1, padx=12, pady=2)

    search_btn = tk.Button(search_frame,bg='lightgreen',text="Search",font=('arial',12),width=10,command=return_search_func)
    search_btn.grid(row=0,column=2,padx=12,pady=2)

    showall_btn = tk.Button(search_frame,bg='lightgreen',text="Show All",font=('arial',12),width=10,command=return_fetch_data)
    showall_btn.grid(row=0,column=3,padx=12,pady=2)

    # ====Database Frame=======

    main_frame = tk.Frame(data_frame, bg="lightgrey", bd=2, relief=tk.GROOVE)
    main_frame.pack(fill=tk.BOTH, expand=True)

    y_scroll = tk.Scrollbar(main_frame, orient=tk.VERTICAL)
    x_scroll = tk.Scrollbar(main_frame, orient=tk.HORIZONTAL)

    return_table = ttk.Treeview(main_frame, columns=(
    "Return ID", "Rental ID", "Rental Date", "Returned Date", "Overdue Days", "Amount to be Payed"),
                             yscrollcommand=y_scroll.set, xscrollcommand=x_scroll.set)

    y_scroll.config(command=return_table.yview)
    x_scroll.config(command=return_table.xview)

    y_scroll.pack(side=tk.RIGHT, fill=tk.Y)
    x_scroll.pack(side=tk.BOTTOM, fill=tk.X)

    return_table.heading("Return ID", text="Return ID")
    return_table.heading("Rental ID", text="Rental ID")
    return_table.heading("Rental Date", text="Rental Date")
    return_table.heading("Returned Date", text="Returned Date")
    return_table.heading("Overdue Days", text="Overdue Days")
    return_table.heading("Amount to be Payed", text="Amount to be Payed")


    return_table['show'] = 'headings'

    return_table.column("Return ID", width=100)
    return_table.column("Rental ID", width=100)
    return_table.column("Rental Date", width=100)
    return_table.column("Returned Date", width=100)
    return_table.column("Overdue Days", width=100)
    return_table.column("Amount to be Payed", width=100)


    return_table.pack(fill=tk.BOTH, expand=True)
    return_fetch_data()
    return_table.bind("<ButtonRelease-1>", get_cursor)

    footer_frame = tk.Frame(new_window, bg="#4682b4", pady=10)
    footer_frame.pack(side=tk.BOTTOM, fill=tk.X)

    footer_label = tk.Label(
        footer_frame,
        text="© 2025 Car Rental System - Nuvin Amarasinghe",
        font=("Arial", 10, "italic"),
        fg="white",
        bg="#4682b4"
    )
    footer_label.pack()


def logout():
    confirm = messagebox.askyesno("Logout", "Do you want to log out?")
    if confirm:
        root.destroy()
        import Login_UI  # Ensure Login_UI is properly structured to run after import


# Assuming you have a username variable
username = session.current_username  # Replace with the actual username

root = tk.Tk()
width, height = 1200, 700

display_width = root.winfo_screenwidth()
display_height = root.winfo_screenheight()

left = int(display_width / 2 - width / 2)
top = int(display_height / 2 - height / 2)

root.geometry(f"{width}x{height}+{left}+{top}")
root.title("Car Rental System | Dashboard")
root.resizable(False, False)
root.iconbitmap("Logo.ico")

bg_image = Image.open("dashboard_bg.jpg")
bg_image = bg_image.resize((1400, 800), Image.LANCZOS)
bg_photo = ImageTk.PhotoImage(bg_image)

bg_label = tk.Label(root, image=bg_photo)
bg_label.place(relwidth=1, relheight=1)

title_frame = tk.Frame(root, bg="#4682b4", pady=10)
title_frame.pack(fill=tk.X)

title_label = tk.Label(
    title_frame,
    text="Car Rental System",
    font=("Arial", 20, "bold"),
    fg="white",
    bg="#4682b4"
)
title_label.pack()

# Create a label for the username at the top right
login_label = tk.Label(
    root,
    text=f"Logged in as: {username}",
    font=("Arial", 12),
    fg="black",
    bg="#4682b4",# Match the background color of the title frame
)
login_label.place(relx=0.95, rely=0.04, anchor='ne')  # Position it at the top right

separator = tk.Frame(root, bg="#b0c4de", height=2)
separator.pack(fill=tk.X, pady=10)

buttons = [
    ("Car Management", car_management),
    ("Customer Management", customer_management),
    ("Rental Management", rental),
    ("Return Management", return_car),
]

for text, command in buttons:
    button = tk.Button(
        root,
        text=text,
        font=("Arial", 14),
        bg="#4682b4",
        fg="white",
        activebackground="#5a9bd5",
        activeforeground="white",
        width=20,
        height=2,
        command=command
    )
    button.pack(pady=10)

logout_button = tk.Button(
    root,
    text="Logout",
    font=("Arial", 12, "bold"),
    bg="#ff4500",
    fg="white",
    activebackground="#ff6347",
    activeforeground="white",
    width=12,
    command=logout
)
logout_button.pack(pady=50)

footer_frame = tk.Frame(root, bg="#4682b4", pady=10)
footer_frame.pack(side=tk.BOTTOM, fill=tk.X)

footer_label = tk.Label(
    footer_frame,
    text="© 2025 Car Rental System - Nuvin Amarasinghe",
    font=("Arial", 10, "italic"),
    fg="white",
    bg="#4682b4"
)
footer_label.pack()

root.mainloop()