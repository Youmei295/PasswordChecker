from fastapi import FastAPI
from checker import password_analyzer
from pydantic import BaseModel
app = FastAPI()
class PasswordRequest(BaseModel):
    password: str
@app.get("/")
def root():
    return {"message": "Password Checker API is running"}

@app.post("/analyze")
def analyze(data: PasswordRequest):
    return password_analyzer(data.password)