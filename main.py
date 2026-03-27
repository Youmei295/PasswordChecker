from fastapi import FastAPI
from pydantic import BaseModel
from checker import password_analyzer
from fastapi.middleware.cors import CORSMiddleware



app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # for now (later restrict)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PasswordRequest(BaseModel):
    password: str

@app.post("/analyze")
def analyze(data: PasswordRequest):
    return password_analyzer(data.password)