from fastapi import APIRouter

from Project.db.DBUtils import get_db
from Project.models.data import Data, UserData

router = APIRouter()


@router.get("/data")
def list_data() -> list[Data]:
    with get_db() as conn:
        rows = conn.execute("SELECT id, title FROM sample_data").fetchall()
        return [Data(id=row["id"], title=row["title"]) for row in rows]


@router.post("/data")
def create_data(body: UserData) -> Data:
    with get_db() as conn:
        cursor = conn.execute("INSERT INTO sample_data (title) VALUES (?)", (body.title,))
        row = conn.execute(
            "SELECT id, title FROM sample_data WHERE id = ?", (cursor.lastrowid,)
        ).fetchone()

        return Data(id=row["id"], title=row["title"])
