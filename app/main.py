from fastapi import FastAPI
from app.api.routes import router as policy_router
from app.models import Base
from app.database import engine

# Create all tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Retention Policy Service")

app.include_router(policy_router, prefix="/api/policies", tags=["Policies"])
