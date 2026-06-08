import sqlite3
import pandas as pd
import os
from datetime import datetime

DB_PATH = "data/prediction_history.db"

def init_db():
    """Creates the table, or upgrades it if it's missing the name column."""
    os.makedirs("data", exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS history (
            date TEXT,
            patient_id TEXT,
            patient_name TEXT,
            risk_level TEXT,
            probability TEXT
        )
    ''')
    
    # Safely force the new 'patient_name' column into older tables
    try:
        cursor.execute("ALTER TABLE history ADD COLUMN patient_name TEXT DEFAULT 'Unknown'")
    except sqlite3.OperationalError:
        pass # The column already exists, so we do nothing.
        
    conn.commit()
    conn.close()

# --- THIS IS THE CRITICAL FIX (Notice it now takes 4 arguments) ---
def save_prediction(patient_id, patient_name, risk_level, probability):
    """
    Saves a prediction record to the SQLite database.
    """
    try:
        # 1. Connect to the database
        conn = sqlite3.connect('data/prediction_history.db')
        cursor = conn.cursor()
        
        # 2. Generate the current date/time
        current_date = datetime.now().strftime("%Y-%m-%d %H:%M")
        
        # 3. Execute the insert (Notice: 5 columns, 5 question marks, 5 variables)
        cursor.execute('''
            INSERT INTO history (patient_id, patient_name, date, risk_level, probability)
            VALUES (?, ?, ?, ?, ?)
        ''', (patient_id, patient_name, current_date, risk_level, probability))
        
        # 4. Commit and close
        conn.commit()
        
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    finally:
        if conn:
            conn.close()

def get_history():
    init_db()
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM history ORDER BY date DESC", conn)
    conn.close()
    return df

def get_next_patient_id():
    """Acts like a Primary Key: Counts existing records and generates the next sequential ID."""
    init_db()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM history")
    count = cursor.fetchone()[0]
    conn.close()
    
    next_id_number = 1001 + count
    return f"PT-{next_id_number}"