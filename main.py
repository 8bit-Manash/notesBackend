# Import FastAPI class to create our backend application
from fastapi import FastAPI

# Import router object from routes.py (contains all API endpoints)
from routes import router

# Import CORS middleware to allow frontend (browser) to talk to backend
from fastapi.middleware.cors import CORSMiddleware

# Create FastAPI application object
app = FastAPI()
# This line creates your server

# Add CORS middleware to the app
app.add_middleware(
    CORSMiddleware,

    # Allow requests from any frontend (React, browser, etc.)
    allow_origins=["*"],

    # Allow all HTTP methods (GET, POST, PUT, DELETE, etc.)
    allow_methods=["*"],

    # Allow all headers (Authorization, Content-Type, etc.)
    allow_headers=["*"],
)

# Attach all routes (APIs) from routes.py to this FastAPI app
app.include_router(router)

