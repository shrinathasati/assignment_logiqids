import sqlite3

DATABASE = "referral_system.db"

def initialize_database():
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()

    with open("schema.sql", "r") as f:
        cur.executescript(f.read())

    conn.commit()
    conn.close()
    print("Database initialized successfully!")

if __name__ == "__main__":
    initialize_database()
