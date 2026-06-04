# FastAPI Template

Minimal FastAPI starter with SQLite, CORS, and environment-based config.

## Setup

```bash
cp .env.example .env
./run.sh
```

API runs at `http://localhost:8000`. Docs at `/docs`.

## Env Variables

| Variable           | Default                   |
|--------------------|---------------------------|
| `DEBUG`            | `false`                   |
| `PORT`             | `8000`                    |
| `FRONTEND_ORIGINS` | `http://localhost:3000`   |
| `DB_PATH`          | `./data.db`               |
| `DB_SCHEMA_PATH`   | `./Project/db/schema.sql` |

## Adding a Route

Create `Project/routes/yourroute.py` with a `router = APIRouter()`, then add it to `all_routes` in `Project/routes/__init__.py`.
