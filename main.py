from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.contacts import router as contacts_router
from src.conf.config import settings

app = FastAPI(
    title="Contacts API",
    description="REST API for managing contacts using FastAPI and SQLAlchemy",
    version="1.0.0",
    debug=settings.debug
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(contacts_router, prefix="/api")


@app.get("/")
def read_root():
    return {"message": "Welcome to Contacts API"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug
    )
