from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from checker import password_analyzer

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/analyze-form")
def analyze_form(request: Request, password: str = Form(...)):
    result = password_analyzer(password)
    return templates.TemplateResponse("index.html", {
        "request": request,
        "result": result
    })