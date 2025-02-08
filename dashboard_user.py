import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
import sqlite3
from tkcalendar import DateEntry
from datetime import date
import session


# Define button commands
def car_info():
    new_window = tk.Toplevel(root)
    new_window.geometry(f"{width}x{height}+{left}+{top}")
    new_window.title("Car Information")
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

    title_label = tk.Label(new_window, text="Car Information", font=("Arial", 18, "bold"))
    title_label.pack(pady=20)

    frame_width = 700
    frame_height = 575
    window_width = 1200
    window_height = 700

    x_position = (window_width - frame_width) // 2
    y_position = (window_height - frame_height) // 2

    data_frame = tk.Frame(new_window, bd=12, bg="lightgrey")
    data_frame.place(x=x_position, y=y_position, width=frame_width, height=frame_height)

    # Create the Back button
    back_btn = tk.Button(new_window, text="Back", font=("Arial", 12, "bold"), bg="#ff4500", fg="white",width=10,command=new_window.destroy)


    # Center the button below the data_frame
    back_btn.place(relx=0.5, rely=0.97, anchor='s')  # Place the button at the center below the data_frame

    #=====Variables====
    search_by = tk.StringVar()

    def car_fetch_data():
        conn = sqlite3.connect("database.db")  # Connect to SQLite database
        curr = conn.cursor()
        curr.execute("SELECT car_id,car_make,car_model,year_manufactured,car_color,car_availability,charge_per_day FROM car")
        rows = curr.fetchall()

        if len(rows) > 0:
            car_table.delete(*car_table.get_children())  # Clear existing data
            for row in rows:
                car_table.insert("", "end", values=row)  # Insert fetched data into Treeview

        conn.close()  # Close the connection

    def car_search_func():
        """Search for a car by its ID, Make, or Model"""
        search_query = search_by.get().strip()  # Get the search input and remove extra spaces

        if search_query == "":
            messagebox.showerror("Error!", "Please enter a Car Make or Car Model to search!", parent=new_window)
            return

        conn = None
        try:
            conn = sqlite3.connect("database.db")  # Connect to the database
            curr = conn.cursor()

            # Search query: Check if the input is numeric (assume it's an ID), otherwise, search by make or model
            if search_query.isdigit():
                curr.execute("SELECT * FROM car WHERE car_id = ?", (search_query,))
            else:
                # Search by car make or car model
                curr.execute("SELECT * FROM car WHERE car_make LIKE ? OR car_model LIKE ?",
                             ('%' + search_query + '%', '%' + search_query + '%'))

            rows = curr.fetchall()

            # Clear existing data in the table
            car_table.delete(*car_table.get_children())

            # Display search results
            if rows:
                for row in rows:
                    car_table.insert("", tk.END, values=row)
            else:
                messagebox.showinfo("No Results", "No matching records found!", parent=new_window)

        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Error occurred: {e}", parent=new_window)
        finally:
            if conn:
                conn.close()  # Ensure the connection is closed

    #======Search=========

    search_frame = tk.Frame(data_frame, bg='lightblue', bd=1, relief=tk.GROOVE)
    search_frame.pack(side=tk.TOP, fill=tk.X)

    search_lbl = tk.Label(search_frame, text="Search (make/model)", bg='lightgrey', font=('arial', 12))
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

    car_table = ttk.Treeview(main_frame, columns=("No.", "Car Make", "Car Model", "Year Manufactured", "Color", "Availability","Charge per Day"), yscrollcommand=y_scroll.set, xscrollcommand=x_scroll.set)

    y_scroll.config(command=car_table.yview)
    x_scroll.config(command=car_table.xview)

    y_scroll.pack(side=tk.RIGHT, fill=tk.Y)
    x_scroll.pack(side=tk.BOTTOM, fill=tk.X)

    car_table.heading("No.", text="No.")
    car_table.heading("Car Make", text="Car Make")
    car_table.heading("Car Model", text="Car Model")
    car_table.heading("Year Manufactured", text="Year Manufactured")
    car_table.heading("Color", text="Color")
    car_table.heading("Availability", text="Availability")
    car_table.heading("Charge per Day", text="Charge per Day")


    car_table['show'] = 'headings'

    car_table.column("No.", width=90)
    car_table.column("Car Make", width=90)
    car_table.column("Car Model", width=90)
    car_table.column("Color", width=90)
    car_table.column("Availability", width=90)
    car_table.column("Year Manufactured", width=108)
    car_table.column("Charge per Day", width=90)


    car_table.pack(fill=tk.BOTH, expand=True)
    car_fetch_data()

    footer_frame = tk.Frame(new_window, bg="#4682b4", pady=0.8)
    footer_frame.pack(side=tk.BOTTOM, fill=tk.X)

    footer_label = tk.Label(
        footer_frame,
        text="© 2025 Car Rental System - Nuvin Amarasinghe",
        font=("Arial", 6, "italic"),
        fg="white",
        bg="#4682b4"
    )
    footer_label.pack()









def new_reservation():
    new_window = tk.Toplevel(root)
    new_window.geometry(f"{width}x{height}+{left}+{top}")
    new_window.title("New Reservation")
    new_window.resizable(False, False)

    new_window.iconbitmap("Logo.ico")

    # Load and set the background image
    bg_image = Image.open("reservation_bg.jpg")  # Load the image
    bg_image = bg_image.resize((1200, 700), Image.LANCZOS)  # Resize the image if necessary
    bg_photo = ImageTk.PhotoImage(bg_image)  # Convert to PhotoImage

    # Create a label to hold the background image
    bg_label = tk.Label(new_window, image=bg_photo)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)  # Fill the entire window

    title_label = tk.Label(bg_label, text="New Reservation", font=("Arial", 18, "bold"))
    title_label.pack(pady=20)

    frame_width = 500
    frame_height = 575
    window_width = 1200
    window_height = 700

    # Position the frame to the left side of the window
    x_position = 0
    y_position = (window_height - frame_height) // 2

    # Create a frame for the input fields
    data_frame = tk.Frame(new_window, bd=12, bg="lightgrey")
    data_frame.place(x=x_position, y=y_position, width=frame_width, height=frame_height)

    # Add the back button to the data frame instead of the background label
    back_button = tk.Button(data_frame, text="Back", font=("Arial", 12, "bold"), bg="#ff4500", fg="white", width=10, command=new_window.destroy)
    back_button.place(relx=0.46, rely=0.86, anchor="center")

    # Keep a reference to the image to prevent garbage collection
    bg_label.image = bg_photo

    # Continue with the rest of your code...
    # (Entry fields, buttons, etc.)

    #====Variables========
    total_amount_var = tk.StringVar()

    # =====Entry Fields=====
    carmake_lbl = tk.Label(data_frame, text="Car Make", font=('Arial', 12), bg="lightgrey")
    carmake_lbl.grid(row=1, column=0, padx=2, pady=10)

    car_make_combo = ttk.Combobox(data_frame, font=('Arial', 12))
    car_make_combo.grid(row=1, column=1, padx=2, pady=10)

    # Car Model
    carmodel_lbl = tk.Label(data_frame, text="Car Model", font=('Arial', 12), bg="lightgrey")
    carmodel_lbl.grid(row=2, column=0, padx=2, pady=10)

    car_model_combo = ttk.Combobox(data_frame, font=('Arial', 12))
    car_model_combo.grid(row=2, column=1, padx=2, pady=10)

    # Car Year
    caryear_lbl = tk.Label(data_frame, text="Car Year", font=('Arial', 12), bg="lightgrey")
    caryear_lbl.grid(row=3, column=0, padx=2, pady=10)

    car_year_combo = ttk.Combobox(data_frame, font=('Arial', 12))
    car_year_combo.grid(row=3, column=1, padx=2, pady=10)

    # Car Color
    carcolor_lbl = tk.Label(data_frame, text="Car Color", font=('Arial', 12), bg="lightgrey")
    carcolor_lbl.grid(row=4, column=0, padx=2, pady=10)

    car_color_combo = ttk.Combobox(data_frame, font=('Arial', 12))
    car_color_combo.grid(row=4, column=1, padx=2, pady=10)

    # Reservation Date
    reservation_date_lbl = tk.Label(data_frame, text="Reservation Date", font=('Arial', 12), bg="lightgrey")
    reservation_date_lbl.grid(row=5, column=0, padx=2, pady=10)

    reservation_date_entry = DateEntry(data_frame, font=("Arial", 12), date_pattern="yyyy-mm-dd", width=18)
    reservation_date_entry.grid(row=5, column=1, padx=2, pady=2)

    return_date_lbl = tk.Label(data_frame, text="Return Date", font=('Arial', 12), bg="lightgrey")
    return_date_lbl.grid(row=6, column=0, padx=2, pady=10)

    return_date_entry = DateEntry(data_frame, font=("Arial", 12), date_pattern="yyyy-mm-dd", width=18)
    return_date_entry.grid(row=6, column=1, padx=2, pady=2)

    # Day Count Label and Entry
    daycount_lbl = tk.Label(data_frame, text="Day Count", font=('Arial', 12), bg="lightgrey")
    daycount_lbl.grid(row=7, column=0, padx=2, pady=2)

    daycount_ent = tk.Entry(data_frame, font=('arial', 12), state='readonly')
    daycount_ent.grid(row=7, column=1, padx=2, pady=2)

    # Total Amount to be Paid
    total_amount_lbl = tk.Label(data_frame, text="Total Amount to be Paid", font=('Arial', 12), bg="lightgrey")
    total_amount_lbl.grid(row=8, column=0, padx=2, pady=10)

    total_amount_entry = tk.Entry(data_frame, font=('Arial', 12), textvariable=total_amount_var, state='readonly')
    total_amount_entry.grid(row=8, column=1, padx=2, pady=10)

    def fetch_car_data():
        car_availability = "Yes"
        try:
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            cursor.execute("SELECT car_make FROM car WHERE car_availability=?", (car_availability,))
            makes = [row[0] for row in cursor.fetchall()]
            car_make_combo['values'] = makes
        except sqlite3.Error as e:
            messagebox.showerror("Error!", "Database error: {e}", parent=new_window)

        finally:
            conn.close()

    def fetch_models(event):
        selected_make = car_make_combo.get()
        car_availability = "Yes"
        try:
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            cursor.execute("SELECT car_model FROM car WHERE car_make=? AND car_availability=?", (selected_make, car_availability,))
            models = [row[0] for row in cursor.fetchall()]
            car_model_combo['values'] = models
        except sqlite3.Error as e:
            messagebox.showerror("Error!", "Database error: {e}", parent=new_window)
        finally:
            conn.close()

    def fetch_years(event):
        selected_model = car_model_combo.get()
        try:
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            cursor.execute("SELECT year_manufactured FROM car WHERE car_model=?", (selected_model,))
            years = [row[0] for row in cursor.fetchall()]
            car_year_combo['values'] = years
        except sqlite3.Error as e:
            messagebox.showerror("Error!", "Database error: {e}", parent=new_window)
        finally:
            conn.close()

    def fetch_colors(event):
        selected_model = car_model_combo.get()
        selected_year = car_year_combo.get()
        try:
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            cursor.execute("SELECT car_color FROM car WHERE car_model=? AND year_manufactured=?", (selected_model, selected_year))
            colors = [row[0] for row in cursor.fetchall()]
            car_color_combo['values'] = colors
        except sqlite3.Error as e:
            messagebox.showerror("Error!", "Database error: {e}", parent=new_window)
        finally:
            conn.close()

    def fetch_charge_per_day():
        selected_make = car_make_combo.get()
        selected_model = car_model_combo.get()
        selected_year = car_year_combo.get()
        try:
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            cursor.execute("SELECT charge_per_day FROM car WHERE car_make=? AND car_model=? AND year_manufactured=?", (selected_make, selected_model, selected_year))
            charge = cursor.fetchone()
            return charge[0] if charge else 0
        except sqlite3.Error as e:
            messagebox.showerror("Error!", "Database error: {e}", parent=new_window)
            return 0
        finally:
            conn.close()

    def calculate_total_amount():
        charge_per_day = fetch_charge_per_day()
        try:
            day_count = int(daycount_ent.get())
            total_amount = charge_per_day * day_count
            total_amount_var.set(f"Rs.{total_amount}")
        except ValueError:
            total_amount_var.set("Rs.0.00")

    def calculate_day_count(event=None):
        try:
            reservation_date = reservation_date_entry.get_date()
            return_date = return_date_entry.get_date()
            day_count = (return_date - reservation_date).days
            if day_count < 0:
                raise ValueError("Return date must be after reservation date.")
            daycount_ent.config(state='normal')
            daycount_ent.delete(0, tk.END)
            daycount_ent.insert(0, str(day_count))
            daycount_ent.config(state='readonly')
            calculate_total_amount()  # Update total amount when day count changes
        except Exception as e:
            daycount_ent.config(state='normal')
            daycount_ent.delete(0, tk.END)
            daycount_ent.insert(0, "Error")
            daycount_ent.config(state='readonly')

    reservation_date_entry.bind("<<DateEntrySelected>>", calculate_day_count)
    return_date_entry.bind("<<DateEntrySelected>>", calculate_day_count)

    car_make_combo.bind("<<ComboboxSelected>>", fetch_models)
    car_model_combo.bind("<<ComboboxSelected>>", fetch_years)
    car_year_combo.bind("<<ComboboxSelected>>", fetch_colors)

    # Add button functionality
    def add_rental():
        username = session.current_username
        try:
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            cursor.execute("SELECT user_id FROM users WHERE username=?", (username,))
            user_id = cursor.fetchone()
            user_id = user_id[0] if user_id else None

            if user_id is None:
                messagebox.showerror("Error!", "User  ID not found.", parent=new_window)
                return

            # Fetch car ID based on selected values
            selected_make = car_make_combo.get()
            selected_model = car_model_combo.get()
            selected_year = car_year_combo.get()
            selected_color = car_color_combo.get()

            cursor.execute("""
                SELECT car_id FROM car 
                WHERE car_make=? AND car_model=? AND year_manufactured=? AND car_color=?
            """, (selected_make, selected_model, selected_year, selected_color))
            car_id = cursor.fetchone()
            car_id = car_id[0] if car_id else None

            if car_id is None:
                messagebox.showerror("Error!","CAR  ID not found.", parent=new_window)
                return

            # Get other details
            rental_date = reservation_date_entry.get_date()
            return_date = return_date_entry.get_date()
            day_count = int(daycount_ent.get())
            amount_to_be_paid = total_amount_var.get().replace("Rs.", "").replace(",", "").strip()

            # Insert into rental table
            cursor.execute("""
                INSERT INTO rental (car_id, user_id, rental_date, return_date, day_count, rental_fee, paid_amount, payment_status, amount_tobe_payed)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
            car_id, user_id, rental_date, return_date, day_count, amount_to_be_paid, 0, "Not Done", amount_to_be_paid))

            # Update car availability
            cursor.execute("""
                UPDATE car 
                SET car_availability = 'No' 
                WHERE car_id = ?
            """, (car_id,))

            conn.commit()
            messagebox.showinfo("Success","Rental added successfully", parent=new_window)
            clear_fields()
        except sqlite3.Error as e:

            messagebox.showerror("Error!", "Database error: {e}", parent=new_window)
        finally:
            conn.close()

    # Clear button functionality
    def clear_fields():
        car_make_combo.set('')
        car_model_combo.set('')
        car_year_combo.set('')
        car_color_combo.set('')

        # Set the date entries to today's date
        today = date.today()
        reservation_date_entry.set_date(today)
        return_date_entry.set_date(today)

        daycount_ent.config(state='normal')
        daycount_ent.delete(0, tk.END)
        daycount_ent.config(state='readonly')
        total_amount_var.set("Rs.0.00")

    # Button frame
    btn_frame = tk.Frame(data_frame, bg="lightblue", bd=1, relief=tk.GROOVE)
    btn_frame.place(x=50, y=390, width=340, height=40)

    add_btn = tk.Button(btn_frame, bg='lightgreen', text="Add", font=('arial', 12), width=17, command=add_rental)
    add_btn.grid(row=0, column=0, padx=2, pady=2)

    clear_btn = tk.Button(btn_frame, bg='lightyellow', text="Clear", font=('arial', 12), width=17, command=clear_fields)
    clear_btn.grid(row=0, column=1, padx=3, pady=2)

    fetch_car_data()

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





def my_reservations():
    new_window = tk.Toplevel(root)
    new_window.geometry(f"{width}x{height}+{left}+{top}")
    new_window.title("My Reservations")
    new_window.resizable(False, False)

    new_window.iconbitmap("Logo.ico")

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

    title_label = tk.Label(new_window, text="My Reservations", font=("Arial", 18, "bold"))
    title_label.pack(pady=20)

    frame_width = 700
    frame_height = 575
    window_width = 1200
    window_height = 700

    x_position = 0
    y_position = (window_height - frame_height) // 2

    data_frame = tk.Frame(new_window, bd=12, bg="lightgrey")
    data_frame.place(x=x_position, y=y_position, width=frame_width, height=frame_height)

    back_button = tk.Button(new_window, text="Back", font=("Arial", 12, "bold"), bg="#ff4500", fg="white",width=10,command=new_window.destroy)
    back_button.place(relx=0.76, rely=0.86)

    def fetch_data():
        try:
            conn = sqlite3.connect("database.db")
            curr = conn.cursor()

            username = session.current_username  # Get logged-in username

            curr.execute("SELECT user_id FROM users WHERE username=?", (username,))
            user_data = curr.fetchone()
            if not user_data:
                print("User not found.")
                return

            user_id = user_data[0]

            curr.execute("""
                SELECT rental_id, car_id, rental_date, return_date, rental_fee, 
                       payment_status, paid_amount, amount_tobe_payed 
                FROM rental WHERE user_id=?
            """, (user_id,))
            rental_rows = curr.fetchall()

            if not rental_rows:
                print("No rental records found for this user.")
                return

            car_table.delete(*car_table.get_children())

            for rental in rental_rows:
                rental_id, car_id, rental_date, return_date, rental_fee, payment_status, paid_amount, amount_tobe_payed = rental

                curr.execute("""
                    SELECT car_make, car_model, year_manufactured, car_color
                    FROM car WHERE car_id=?
                """, (car_id,))
                car_data = curr.fetchone()

                if not car_data:
                    print(f"Car details not found for Car ID {car_id}")
                    continue

                car_make, car_model, year_manufactured, car_color = car_data

                row_data = (
                    rental_id, car_make, car_model, year_manufactured, car_color,
                    rental_date, return_date, rental_fee, payment_status, amount_tobe_payed
                )
                car_table.insert("", "end", values=row_data)

            print("Data fetched successfully.")

        except sqlite3.Error as e:
            print(f"Database error: {e}")

        finally:
            conn.close()

    def generate_bill():
        """Generate and display the bill for the selected reservation."""
        selected_item = car_table.selection()
        if not selected_item:
            messagebox.showwarning("Selection Error", "Please select a row to generate the bill.", parent=new_window)
            return

        row_data = car_table.item(selected_item)["values"]
        if not row_data:
            messagebox.showerror("Error", "No data found for the selected row.")
            return

        rental_id, car_make, car_model, year_manufactured, car_color, rental_date, return_date, total_amount, payment_status, amount_due = row_data

        bill_text.delete("1.0", tk.END)
        bill_details = f"""
        
                                CAR RENTAL SYSTEM
                                    KALUTARA
                                    
                        ********** RENTAL BILL **********
                          Rental ID       : {rental_id}
                          Car Make        : {car_make}
                          Car Model       : {car_model}
                          Year            : {year_manufactured}
                          Color           : {car_color}
                          Rental Date     : {rental_date}
                          Return Date     : {return_date}
                          Total Amount    : Rs.{total_amount}
                          Payment Status  : {payment_status}
                          Amount Due      : Rs.{amount_due}
                         *********************************
                                    Thank You!
        """
        bill_text.insert(tk.END, bill_details)

    def save_bill():
        """Save the generated bill to a text file."""
        bill_content = bill_text.get("1.0", tk.END).strip()
        if not bill_content:
            messagebox.showwarning("Error", "No bill to save. Please generate a bill first.")
            return

        with open("bill.txt", "w") as file:
            file.write(bill_content)

        messagebox.showinfo("Success", "Bill saved as bill.txt" ,parent=new_window)

    # === Database Frame ===
    main_frame = tk.Frame(data_frame, bg="lightgrey", bd=2, relief=tk.GROOVE)
    main_frame.pack(fill=tk.BOTH, expand=True)

    y_scroll = tk.Scrollbar(main_frame, orient=tk.VERTICAL)
    x_scroll = tk.Scrollbar(main_frame, orient=tk.HORIZONTAL)

    car_table = ttk.Treeview(main_frame, columns=("No.", "Car Make", "Car Model", "Year Manufactured", "Color",
                                                  "Rental Date", "Return Date", "Total Amount", "Payment Status",
                                                  "Amount to be payed"),
                             yscrollcommand=y_scroll.set, xscrollcommand=x_scroll.set)

    y_scroll.config(command=car_table.yview)
    x_scroll.config(command=car_table.xview)

    y_scroll.pack(side=tk.RIGHT, fill=tk.Y)
    x_scroll.pack(side=tk.BOTTOM, fill=tk.X)

    car_table.heading("No.", text="No.")
    car_table.heading("Car Make", text="Car Make")
    car_table.heading("Car Model", text="Car Model")
    car_table.heading("Year Manufactured", text="Year Manufactured")
    car_table.heading("Color", text="Color")
    car_table.heading("Rental Date", text="Rental Date")
    car_table.heading("Return Date", text="Return Date")
    car_table.heading("Total Amount", text="Total Amount")
    car_table.heading("Payment Status", text="Payment Status")
    car_table.heading("Amount to be payed", text="Amount to be payed")

    car_table['show'] = 'headings'

    car_table.column("No.", width=90)
    car_table.column("Car Make", width=90)
    car_table.column("Car Model", width=90)
    car_table.column("Year Manufactured", width=108)
    car_table.column("Color", width=90)
    car_table.column("Rental Date", width=90)
    car_table.column("Return Date", width=90)
    car_table.column("Total Amount", width=90)
    car_table.column("Payment Status", width=90)
    car_table.column("Amount to be payed", width=110)

    car_table.pack(fill=tk.BOTH, expand=True)

    # === Right Side Bill Display ===
    bill_frame = tk.Frame(new_window, bd=10, relief=tk.GROOVE, bg="white")
    bill_frame.place(x=750, y=100, width=400, height=450)

    bill_label = tk.Label(bill_frame, text="Bill Receipt", font=("Arial", 14, "bold"), bg="white")
    bill_label.pack(pady=5)

    bill_text = tk.Text(bill_frame, font=("Arial", 10), width=40, height=18)
    bill_text.pack(fill=tk.BOTH, expand=True)

    bill_button_frame = tk.Frame(bill_frame)
    bill_button_frame.pack()

    tk.Button(bill_button_frame, text="Generate Bill", command=generate_bill, bg="lightblue").grid(row=0, column=0, padx=5, pady=5)
    tk.Button(bill_button_frame, text="Save Bill", command=save_bill, bg="springgreen").grid(row=0, column=1, padx=5, pady=5)

    fetch_data()

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


    # You can add additional widgets to the data_frame here


def logout():
    confirm = messagebox.askyesno("Logout", "Do you want to log out?")
    if confirm:
        root.destroy()
        import Login_UI  # Ensure Login_UI is properly structured to run after import

# Create the main window
# Assuming you have a username variable
username = session.current_username  # Replace with the actual username

root = tk.Tk()
width, height = 1200, 700

display_width = root.winfo_screenwidth()
display_height = root.winfo_screenheight()

left = int(display_width / 2 - width / 2)
top = int(display_height / 2 - height / 2)

root.geometry(f"{width}x{height}+{left}+{top}")  # Center the window
root.title("Car Rental System | Dashboard")
root.resizable(False, False)
root.iconbitmap("Logo.ico")

# Load and set background image
bg_image = Image.open("dashboard_bg.jpg")
bg_image = bg_image.resize((1400, 800), Image.LANCZOS)
bg_photo = ImageTk.PhotoImage(bg_image)

bg_label = tk.Label(root, image=bg_photo)
bg_label.place(relwidth=1, relheight=1)

# Title Label with decoration
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

# Greeting Label
greeting_label = tk.Label(
    root,
    text=f"Welcome {username}!",
    font=("Arial", 14),
    fg="black",
    bg="snow"  # Match the background color of the separator
)
greeting_label.pack(pady=(10, 0))  # Add some padding to the top

# Add a decorative separator line
separator = tk.Frame(root, bg="#b0c4de", height=2)
separator.pack(fill=tk.X, pady=10)

# Buttons with decorations
buttons = [
    ("Car Information", car_info),
    ("New Reservation", new_reservation),
    ("My Reservations", my_reservations),
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
    button.pack(pady=30)

# Logout Button with decoration
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
logout_button.pack(pady=80)

# Footer label for additional decorations
footer_frame = tk.Frame(root, bg="#4682b4", pady=8)
footer_frame.pack(side=tk.BOTTOM, fill=tk.X)

footer_label = tk.Label(
    footer_frame,
    text="© 2025 Car Rental System - Nuvin Amarasinghe",
    font=("Arial", 10, "italic"),
    fg="white",
    bg="#4682b4"
)
footer_label.pack()

# Run the application
root.mainloop()