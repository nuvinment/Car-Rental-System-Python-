import sqlite3

# Create a new database (or connect if it exists)
db_path = "database.db"  # Change path if needed
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Create tables
cursor.executescript("""
CREATE TABLE admins (
    admin_id INTEGER PRIMARY KEY,
    admin_name TEXT,
    admin_password TEXT
);

CREATE TABLE return (
    return_id INTEGER PRIMARY KEY,
    rental_id INTEGER REFERENCES rental (rental_id),
    rental_date TEXT REFERENCES rental (rental_date),
    returned_date TEXT,
    overdue_days INTEGER,
    amount_tobe_payed TEXT
);

CREATE TABLE rental (
    rental_id INTEGER PRIMARY KEY,
    car_id INTEGER REFERENCES car (car_id),
    user_id INTEGER REFERENCES users (user_id),
    rental_date TEXT,
    return_date TEXT,
    day_count INTEGER,
    rental_fee TEXT,
    paid_amount TEXT,
    payment_status TEXT,
    amount_tobe_payed TEXT
);

CREATE TABLE car (
    car_id INTEGER PRIMARY KEY,
    car_make TEXT,
    car_model TEXT,
    year_manufactured INTEGER,
    car_number TEXT,
    car_milage TEXT,
    charge_per_day INTEGER,
    car_availability TEXT,
    car_color TEXT
);

CREATE TABLE users (
    user_id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT,
    full_name TEXT,
    user_email TEXT,
    user_phone_no INTEGER,
    nic_no TEXT UNIQUE
);
""")

# Commit and close the connection
conn.commit()
conn.close()

print("Database created successfully!")
