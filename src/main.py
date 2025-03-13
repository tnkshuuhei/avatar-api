"""
Main entry point for the API application.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.routes import router as general_router
from src.api.personality_routes import router as personality_router

app = FastAPI(
    title="AI Avatar API",
    description="API for interacting with AI avatars with different personalities",
    version="1.0.0",
)

# Configure CORS to allow requests from your frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(general_router)
app.include_router(personality_router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=True)
