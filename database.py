import sqlite3
from datetime import datetime

DB_PATH = "phishing_detector.db"

def create_connection():
    """
    Opens a connection to the SQLite database.
    Creates the database file if it doesn't exist yet.
    """
    conn = sqlite3.connect(DB_PATH)
    return conn

def create_table():
    """
    Creates the analysis_results table if it doesn't already exist.
    """
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS analysis_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            email_text TEXT NOT NULL,
            verdict TEXT NOT NULL,
            confidence REAL NOT NULL,
            num_urls INTEGER,
            num_ip_links INTEGER,
            num_suspicious_words INTEGER,
            num_exclamations INTEGER,
            num_all_caps INTEGER,
            email_length INTEGER
        )
    ''')
    conn.commit()
    conn.close()

def save_result(email_text, verdict, confidence, features):
    """
    Inserts a single analysis result into the database.
    'features' is the handcrafted_features dictionary from detector.py.
    """
    conn = create_connection()
    cursor = conn.cursor()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute('''
        INSERT INTO analysis_results 
        (timestamp, email_text, verdict, confidence, num_urls, num_ip_links,
         num_suspicious_words, num_exclamations, num_all_caps, email_length)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        timestamp,
        email_text,
        verdict,
        confidence,
        features["num_urls"],
        features["num_ip_links"],
        features["num_suspicious_words"],
        features["num_exclamations"],
        features["num_all_caps"],
        features["email_length"]
    ))
    conn.commit()
    conn.close()

def get_history():
    """
    Returns all past analysis results as a list of rows.
    Each row is a tuple: (id, timestamp, email_text, verdict, confidence, ...).
    """
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, timestamp, email_text, verdict, confidence FROM analysis_results ORDER BY id DESC")
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_stats():
    """
    Calculates and returns summary statistics from the database.
    Returns a dictionary with total count, phishing count, legitimate count, and percentages.
    """
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM analysis_results")
    total = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM analysis_results WHERE verdict = 'phishing'")
    phishing_count = cursor.fetchone()[0]

    legit_count = total - phishing_count

    conn.close()

    stats = {
        "total": total,
        "phishing": phishing_count,
        "legitimate": legit_count,
        "phishing_pct": round((phishing_count / total) * 100, 2) if total > 0 else 0,
        "legitimate_pct": round((legit_count / total) * 100, 2) if total > 0 else 0
    }
    return stats

if __name__ == "__main__":
    # Quick test: create table, insert a fake result, and read it back
    create_table()
    print("Table created successfully.")

    # Insert a test result
    test_features = {
        "num_urls": 2,
        "num_ip_links": 1,
        "num_suspicious_words": 4,
        "num_exclamations": 3,
        "num_all_caps": 1,
        "email_length": 150
    }
    save_result("This is a test phishing email.", "phishing", 95.0, test_features)
    print("Test result saved.")

    # Read history
    history = get_history()
    print(f"\nHistory ({len(history)} records):")
    for row in history:
        print(f"  [{row[0]}] {row[1]} | {row[3].upper()} ({row[4]}%) | {row[2][:50]}...")

    # Show stats
    stats = get_stats()
    print(f"\nStats:")
    print(f"  Total analyzed: {stats['total']}")
    print(f"  Phishing: {stats['phishing']} ({stats['phishing_pct']}%)")
    print(f"  Legitimate: {stats['legitimate']} ({stats['legitimate_pct']}%)")
