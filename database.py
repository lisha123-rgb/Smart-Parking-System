import sqlite3
import os

def init_db():
    conn = sqlite3.connect('parking.db')
    cursor = conn.cursor()
    
    # Create user table (without numberplate)
    cursor.execute('''CREATE TABLE IF NOT EXISTS user(
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        name TEXT, 
        password TEXT, 
        mobile TEXT, 
        email TEXT
    )''')
    
    # Create wallet table
    cursor.execute('''CREATE TABLE IF NOT EXISTS wallet(
        balance REAL, 
        phone TEXT
    )''')
    
    # Create history table
    cursor.execute('''CREATE TABLE IF NOT EXISTS history(
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        name TEXT, 
        mobile TEXT, 
        email TEXT, 
        numberplate TEXT, 
        slot TEXT, 
        booked_time DATETIME DEFAULT CURRENT_TIMESTAMP,
        entry DATETIME,
        exit DATETIME,
        amount TEXT,
        status TEXT DEFAULT 'active'
    )''')
    
    # Create feedback table
    cursor.execute('''CREATE TABLE IF NOT EXISTS feedback(
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        name TEXT, 
        email TEXT, 
        feed TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )''')
    
    conn.commit()
    conn.close()

def get_db_connection():
    conn = sqlite3.connect('parking.db')
    conn.row_factory = sqlite3.Row
    return conn