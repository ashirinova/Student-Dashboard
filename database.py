import sqlite3
from typing import List, Tuple, Optional
from config import DB_NAME

def create_connection() -> Optional[sqlite3.Connection]:
    """SQLite Verilənlər bazası ilə əlaqə yaradır."""
    try:
        conn = sqlite3.connect(DB_NAME, check_same_thread=False)
        return conn
    except sqlite3.Error as err:
        print(f"Database connection error: {err}")
        return None

def init_db():
    """Cədvəl və nümayiş üçün ilkin məlumatları yaradır."""
    conn = create_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Students (
                Id INTEGER PRIMARY KEY AUTOINCREMENT,
                Name TEXT NOT NULL,
                Score REAL NOT NULL
            )
        """)
        cursor.execute("SELECT COUNT(*) FROM Students")
        if cursor.fetchone()[0] == 0:
            cursor.executemany(
                "INSERT INTO Students (Name, Score) VALUES (?, ?)",
                [('Ali', 85), ('Leyla', 72), ('Murad', 48), ('Aysel', 91), ('Kamran', 63), ('Nigar', 95), ('Elvin', 55)]
            )
        conn.commit()
        conn.close()

def add_student(name: str, score: float) -> bool:
    """Yeni tələbə əlavə edir."""
    conn = create_connection()
    if not conn:
        return False
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Students (Name, Score) VALUES (?, ?)", (name, score))
        conn.commit()
        return True
    except sqlite3.Error as err:
        print(f"Error adding student: {err}")
        return False
    finally:
        conn.close()

def update_student_score(student_id: int, new_score: float) -> bool:
    """Tələbənin balını yeniləyir."""
    conn = create_connection()
    if not conn:
        return False
    try:
        cursor = conn.cursor()
        cursor.execute("UPDATE Students SET Score = ? WHERE Id = ?", (new_score, student_id))
        conn.commit()
        return True
    except sqlite3.Error as err:
        print(f"Error updating student: {err}")
        return False
    finally:
        conn.close()

def delete_student(student_id: int) -> bool:
    """Tələbəni bazadan silir."""
    conn = create_connection()
    if not conn:
        return False
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Students WHERE Id = ?", (student_id,))
        conn.commit()
        return True
    except sqlite3.Error as err:
        print(f"Error deleting student: {err}")
        return False
    finally:
        conn.close()

def get_students() -> List[Tuple[int, str, float]]:
    """Bütün tələbələri gətirir."""
    conn = create_connection()
    if not conn:
        return []
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT Id, Name, Score FROM Students ORDER BY Id DESC")
        return cursor.fetchall()
    except sqlite3.Error as err:
        print(f"Error fetching students: {err}")
        return []
    finally:
        conn.close()

def get_student(search_name: str) -> List[Tuple[int, str, float]]:
    """Adına görə tələbələri axtarır."""
    conn = create_connection()
    if not conn:
        return []
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT Id, Name, Score FROM Students WHERE Name LIKE ?", (f"%{search_name}%",))
        return cursor.fetchall()
    except sqlite3.Error as err:
        print(f"Error searching student: {err}")
        return []
    finally:
        conn.close()