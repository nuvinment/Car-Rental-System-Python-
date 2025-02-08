import tkinter as tk
from tkinter import messagebox, PhotoImage
from PIL import Image, ImageTk
import sqlite3
import session

#Start Programme Here=##############>>>/,.>>>>

def sign_up(parent, user_database):
    sign_up_window = tk.Toplevel(parent)
    width, height = 500, 500

    display_width = sign_up_window.winfo_screenwidth()
    display_height = sign_up_window.winfo_screenheight()

    left = int(display_width / 2 - width / 2)
    top = int(display_height / 2 - height / 2)

    sign_up_window.geometry(f"{width}x{height}+{left}+{top}")  # Center the window
    sign_up_window.title("Car Rental System | SignUp")
    sign_up_window.resizable(False, False)
    sign_up_window.iconbitmap("Logo.ico")

    # Load background image with reduced opacity
    bg_image = Image.open("signup_bg.jpg").convert("RGBA")
    bg_image = bg_image.resize((500, 500), Image.Resampling.LANCZOS)
    bg_photo = ImageTk.PhotoImage(bg_image)
    bg_label = tk.Label(sign_up_window, image=bg_photo)
    bg_label.place(relwidth=1, relheight=1)
    sign_up_window.image = bg_photo

    def register():
        name = name_entry.get()
        username = username_entry.get()
        email = email_entry.get()
        phone = phone_entry.get()
        nic = nic_entry.get()
        password = password_entry.get()

        if not username or not password or not name or not email or not phone or not nic:
            messagebox.showerror("Error", "All fields are required",parent=sign_up_window)
            return

        try:
            conn = sqlite3.connect("database.db")
            cursor = conn.cursor()

            # Insert the new user data into the `users` table
            cursor.execute(
                """
                INSERT INTO users (username, password, full_name, user_email, user_phone_no, nic_no)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (username, password, name, email, phone, nic)
            )
            conn.commit()
            conn.close()

            messagebox.showinfo("Success", "Account Created Successfully!",parent=sign_up_window)
            sign_up_window.destroy()
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}",parent=sign_up_window)

    frame = tk.Frame(sign_up_window, bg='lightgray', padx=10, pady=10)
    frame.place(relx=0.5, rely=0.5, anchor='center')

    tk.Label(frame, text="Full Name:", bg='lightgray', anchor='w').pack(pady=5, fill='x')
    name_entry = tk.Entry(frame, width=40, font=("Arial", 12), bd=2, relief="solid")
    name_entry.pack(pady=5)

    tk.Label(frame, text="Username:", bg='lightgray', anchor='w').pack(pady=5, fill='x')
    username_entry = tk.Entry(frame, width=40, font=("Arial", 12), bd=2, relief="solid")
    username_entry.pack(pady=5)

    tk.Label(frame, text="Email:", bg='lightgray', anchor='w').pack(pady=5, fill='x')
    email_entry = tk.Entry(frame, width=40, font=("Arial", 12), bd=2, relief="solid")
    email_entry.pack(pady=5)

    tk.Label(frame, text="Phone Number:", bg='lightgray', anchor='w').pack(pady=5, fill='x')
    phone_entry = tk.Entry(frame, width=40, font=("Arial", 12), bd=2, relief="solid")
    phone_entry.pack(pady=5)

    tk.Label(frame, text="N.I.C. Number:", bg='lightgray', anchor='w').pack(pady=5, fill='x')
    nic_entry = tk.Entry(frame, width=40, font=("Arial", 12), bd=2, relief="solid")
    nic_entry.pack(pady=5)

    tk.Label(frame, text="Create Password:", bg='lightgray', anchor='w').pack(pady=5, fill='x')
    password_entry = tk.Entry(frame, show='*', width=40, font=("Arial", 12), bd=2, relief="solid")
    password_entry.pack(pady=5)

    tk.Button(frame, text="Register", command=register, width=10, bg="lightgreen").pack(pady=10)
    tk.Button(frame, text="Back", command=sign_up_window.destroy , width=10 , bg="orange").pack(pady=10)



def logout():
    root.destroy()
    import Login_UI

# Dummy database
user_database = {}

# Create main login window
root = tk.Tk()
width, height = 500, 500

display_width = root.winfo_screenwidth()
display_height = root.winfo_screenheight()

left = int(display_width / 2 - width / 2)
top = int(display_height / 2 - height / 2)

root.geometry(f"{width}x{height}+{left}+{top}")  # Center the window
root.title("Car Rental System | Login")
root.resizable(False, False)
root.iconbitmap("Logo.ico")



# Load background image with reduced opacity
bg_image = Image.open("login_bg.jpg").convert("RGBA")
bg_image = bg_image.resize((500, 500), Image.Resampling.LANCZOS)
bg_photo = ImageTk.PhotoImage(bg_image)
bg_label = tk.Label(root, image=bg_photo)
bg_label.place(relwidth=1, relheight=1)

# Login function
def login():
    global current_username
    username = username_entry.get()
    password = password_entry.get()

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM admins WHERE admin_name = ? AND admin_password = ?", (username, password))
    admin = cursor.fetchone()

    if admin:
        session.current_username = username
        root.destroy()
        import Dashboard_UI  # Load the admin dashboard file
        return
        
        
    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    user = cursor.fetchone()

    if user:
        session.current_username = username
        root.destroy()
        import dashboard_user  # Import dashboard after login


        # Load the user dashboard file
    else:
        messagebox.showerror("Login Failed", "Invalid username or password")

    conn.close()


    

# Login Form
tk.Label(root, text="Username:", font=("Arial", 12)).pack(pady=5)
username_entry = tk.Entry(root, width=35, font=("Arial", 12), bd=2, relief="solid")
username_entry.pack(pady=30)

tk.Label(root, text="Password:",font=("Arial", 12)).pack(pady=5)
password_entry = tk.Entry(root, show="*", width=35, font=("Arial", 12), bd=2, relief="solid")
password_entry.pack(pady=30)

tk.Button(root, text="Login",font=("Helvetica", 10,), command=login, width=10 ,bg="lightgreen",fg="black").pack(pady=10)
tk.Button(root, text="Sign Up", font=("Helvetica", 10,),command=lambda: sign_up(root, user_database), width=10,bg="lightblue",fg="black").pack(pady=5)

root.mainloop()

