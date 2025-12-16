from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.core.config import settings
from app.api.v1.endpoints import ai_tutor
from app.db.session import engine
from app.db.base import Base

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Create tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan
)

# Route de santé
@app.get("/health")
async def health_check():
    return {"status": "ok", "app_name": settings.PROJECT_NAME}

# Inclusion des routeurs
app.include_router(ai_tutor.router, prefix=f"{settings.API_V1_STR}/ai", tags=["AI Tutor"])

from app.api.v1.endpoints import auth, users, courses
app.include_router(auth.router, prefix=f"{settings.API_V1_STR}/auth", tags=["Auth"])
app.include_router(users.router, prefix=f"{settings.API_V1_STR}/users", tags=["Users"])
app.include_router(courses.router, prefix=f"{settings.API_V1_STR}/courses", tags=["Courses"])

from app.api.v1.endpoints import certificates
app.include_router(certificates.router, prefix=f"{settings.API_V1_STR}/certificates", tags=["Certificates"])

from app.api.v1.endpoints import video
app.include_router(video.router, prefix=f"{settings.API_V1_STR}/video", tags=["Video Classrooms"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
