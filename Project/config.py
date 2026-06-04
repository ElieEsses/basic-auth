import os
import dotenv

dotenv.load_dotenv()


def _get_bool(name: str, default: bool = False) -> bool:
    return os.environ.get(name, str(default)).strip().lower() in {
        "1",
        "true",
        "yes",
        "on",
    }


def _get_int(name: str, default: int) -> int:
    value = os.environ.get(name)
    return int(value) if value not in (None, "") else default


def _get_list(name: str, default: str) -> list[str]:
    value = os.environ.get(name, default)
    return [item.strip() for item in value.split(",") if item.strip()]


DEBUG_MODE = _get_bool("DEBUG", default=False)
PORT = _get_int("PORT", default=8000)
FRONTEND_ORIGINS = _get_list("FRONTEND_ORIGINS", "http://localhost:3000")
DB_SCHEMA_PATH = os.environ.get("DB_SCHEMA_PATH", "./Project/db/schema.sql")
DB_PATH = os.environ.get("DB_PATH", "./data.db")