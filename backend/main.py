import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import asyncpg

app = FastAPI()

# Settings & Middleware
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:pass@localhost:5432/db")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database Schema
class Task(BaseModel):
    title: str

# Health Endpoint
@app.get("/health")
async def health_check():
    return {"status": "ok"}

# API Endpoint
@app.get("/api/v1/tasks")
async def get_tasks():
    conn = await asyncpg.connect(DATABASE_URL)
    try:
        # Check if the table exists; if not, create it to ensure the app doesn't crash
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id SERIAL PRIMARY KEY,
                title TEXT NOT NULL,
                completed BOOLEAN DEFAULT FALSE
            )
        """)

        # 2. Check row
        rows = await conn.fetch("SELECT * FROM tasks")
        
        if not rows:
            return [{"id": 0, "title": "No tasks found in DB", "completed": False}]

        return [dict(r) for r in rows]
    
    except Exception as e:
        return {"error": str(e)}
    finally:
        await conn.close()

