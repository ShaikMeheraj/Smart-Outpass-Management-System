import sqlite3

# Database setup
def init_db():
    conn = sqlite3.connect("users.db")
    #drop table
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT UNIQUE,
            role TEXT,
            branch TEXT,
            student_image BLOB,
            category TEXT,
            password TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS outpass (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT,
            subject TEXT,
            reason TEXT,
            from_date TEXT,
            to_date TEXT,
            status TEXT
                   
        )
    """)
    conn.commit()
    conn.close()

# Database setup
# Register a new user
def register_user(name, email, role, branch, student_image,category, password):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    try:
        if student_image is not None:
            student_image = student_image.read()
        cursor.execute("""
            INSERT INTO users (name, email, role, branch, student_image,category, password)
            VALUES (?, ?, ?, ?, ?,?,?)
        """, (name, email, role, branch, student_image,category, password))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

# Validate login credentials
def validate_user(email, password):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email = ? AND password = ?", (email, password))
    user = cursor.fetchone()
    conn.close()
    return user

def forgot_password(email):
    conn=sqlite3.connect("users.db")
    cursor=conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
    user = cursor.fetchone()
    conn.close()

def fetch_user(email):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
    user = cursor.fetchone()
    conn.close()
    return user

def add_outpass(email, subject, reason, from_date, to_date, status):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO outpass (email, subject, reason, from_date, to_date, status)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (email, subject, reason, from_date, to_date, status))
    conn.commit()
    conn.close()

def fetch_outpass(email):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM outpass WHERE email = ?", (email,))
    outpass = cursor.fetchall()
    conn.close()
    return outpass

def fetch_all_outpass():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM outpass")
    outpass = cursor.fetchall()
    conn.close()
    return outpass

def update_outpass(id, status):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE outpass SET status = ? WHERE id = ?", (status, id))
    conn.commit()
    conn.close()

def fetch_all_users():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    conn.close()
    return users

def fetch_users_by_branch(branch):
    #selct role is student and branch is branch
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE role = 'student' AND branch = ?", (branch,))
    users = cursor.fetchall()
    conn.close()
    return users