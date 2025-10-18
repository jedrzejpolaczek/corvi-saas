from fastapi import FastAPI, HTTPException, Depends, Form, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
import os

# Simple settings without complex imports
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://corvi:corvi123@postgres:5432/corvi")

app = FastAPI(title="Corvi API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models for requests
class LoginRequest(BaseModel):
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class User(BaseModel):
    id: int
    email: str
    name: str

class LogoutResponse(BaseModel):
    message: str

@app.get("/")
async def root():
    return {"message": "Corvi API is running!", "database_url": DATABASE_URL}

@app.get("/health")
async def health():
    return {"status": "healthy", "version": "1.0.0"}

@app.post("/auth/login", response_model=Token)
async def login(login_data: LoginRequest):
    if login_data.email == "demo@corvi.ai" and login_data.password == "demo123":
        return {
            "access_token": "demo_token_12345",
            "token_type": "bearer"
        }
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")

@app.post("/auth/token", response_model=Token)
async def token(
    username: str = Form(None),
    password: str = Form(None),
    email: str = Form(None),
    grant_type: str = Form(None)
):
    login_email = username or email
    
    print(f"Login attempt - email/username: {login_email}, password: {password}, grant_type: {grant_type}")
    
    if login_email == "demo@corvi.ai" and password == "demo123":
        return {
            "access_token": "demo_token_12345",
            "token_type": "bearer"
        }
    else:
        raise HTTPException(status_code=401, detail="Incorrect username or password")

# *** DODAJ ENDPOINTS WYLOGOWANIA ***
@app.post("/auth/logout", response_model=LogoutResponse)
async def logout():
    return {"message": "Successfully logged out"}

@app.delete("/auth/logout", response_model=LogoutResponse)
async def logout_delete():
    return {"message": "Successfully logged out"}

@app.get("/auth/logout", response_model=LogoutResponse)
async def logout_get():
    return {"message": "Successfully logged out"}

@app.get("/auth/me", response_model=User)
async def get_current_user():
    return {
        "id": 1,
        "email": "demo@corvi.ai",
        "name": "Demo User"
    }

@app.get("/users/me", response_model=User)
async def get_user_profile():
    return {
        "id": 1,
        "email": "demo@corvi.ai", 
        "name": "Demo User"
    }

@app.get("/projects")
async def get_projects():
    return [
        {"id": 1, "name": "Demo Project", "description": "Sample project for demo"},
        {"id": 2, "name": "Test Project", "description": "Another sample project"}
    ]

@app.get("/experiments")
async def get_experiments():
    return [
        {"id": 1, "name": "Demo Experiment", "project_id": 1},
        {"id": 2, "name": "Test Experiment", "project_id": 1}
    ]