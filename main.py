from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from checker import password_analyzer

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/")
def home(request: Request):
    # Pass the dictionary as the second argument
    return templates.TemplateResponse(
        request=request, 
        name="index.html", 
        context={"result": None}
    )

@app.post("/analyze-form")
def analyze_form(request: Request, password: str = Form(...)):
    result = password_analyzer(password)
    return templates.TemplateResponse(
        request=request, 
        name="index.html", 
        context={"result": result})