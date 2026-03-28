#qwerty
from fastapi import FastAPI
from pydantic import BaseModel
from checker import password_analyzer
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import os
import pyodbc

def get_connection():
    try:
        conn_str = (
            "DRIVER={ODBC Driver 17 for SQL Server};"
            f"SERVER={os.getenv('DB_SERVER')};"
            f"DATABASE={os.getenv('DB_NAME')};"
            f"UID={os.getenv('DB_USER')};"
            f"PWD={os.getenv('DB_PASSWORD')};"
            "Encrypt=yes;"
            "TrustServerCertificate=no;"
            "Connection Timeout=30;"
        )
        return pyodbc.connect(conn_str)
    except Exception as e:
        print("Connection error:", e)
        raise

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    IF NOT EXISTS (
        SELECT * FROM sysobjects 
        WHERE name='results' AND xtype='U'
    )
    CREATE TABLE results (
        id INT IDENTITY(1,1) PRIMARY KEY,
        password NVARCHAR(255),
        score NVARCHAR(50),
        entropy FLOAT
    )
    """)

    conn.commit()
    conn.close()
@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        init_db()
    except Exception as e:
        print("Init DB failed:", e)
    yield

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://password-checker-frontend-gweqdkf7e7gfbvde.eastasia-01.azurewebsites.net"],  # for now (later restrict)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PasswordRequest(BaseModel):
    password: str

@app.post("/analyze")
def analyze(data: PasswordRequest):
    result = password_analyzer(data.password)

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO results (password, score, entropy) VALUES (?, ?, ?)",
        data.password, result['score'], result['entropy']
    )

    conn.commit()
    conn.close()

    return result