from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.db import Base, engine
from app.routers import clips, projects

app = FastAPI(title="Clip Generator API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(projects.router)
app.include_router(clips.router)


@app.on_event("startup")
def on_startup():
    # MVP: table creation via metadata, no migration tool yet.
    # Swap for Alembic once the schema needs to evolve safely in production.
    Base.metadata.create_all(bind=engine)


@app.get("/health")
def health():
    return {"status": "ok"}
