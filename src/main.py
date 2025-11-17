from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import api_router  # Import the aggregated router

# Initialize the FastAPI app instance here
app = FastAPI(title="UH Pathfinder API")

# Add CORS middleware to allow frontend calls from different origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def read_root():
    return {"message": "Welcome to the UH Pathfinder API"}


@app.get("/health")
async def health() -> dict:
    return {"status": "ok"}

# Include the main API router in the application
app.include_router(api_router, prefix="/api/v1")

if __name__ == "__main__":
    # This block allows running the application with 'python main.py'
    # Use 'pip install uvicorn' first
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)