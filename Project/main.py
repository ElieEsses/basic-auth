import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from Project.config import DB_SCHEMA_PATH, DEBUG_MODE, FRONTEND_ORIGINS, PORT
from Project.db.DBUtils import init_db
from Project.routes import all_routes

if DEBUG_MODE:
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)
    logging.getLogger("hpack").setLevel(logging.WARNING)


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db(DB_SCHEMA_PATH)
    yield


app = FastAPI(
    title="FastAPI Template",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=FRONTEND_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"message": "FastAPI template is running"}


for route_module in all_routes:
    app.include_router(route_module.router, prefix="/api")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("Project.main:app", host="0.0.0.0", port=PORT, reload=DEBUG_MODE)
