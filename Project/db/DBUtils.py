import sqlite3
from contextlib import contextmanager
from Project.config import DB_PATH

@contextmanager
def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()         

def init_db(db_schema_path):
    with get_db() as conn:
        with open(db_schema_path) as f:
            conn.executescript(f.read())