from fastapi import FastAPI
from pydantic import BaseModel
from checker import password_analyzer
from nicegui import ui

app = FastAPI()

# -------- API PART --------
class PasswordRequest(BaseModel):
    password: str

@app.post("/analyze")
def analyze(data: PasswordRequest):
    return password_analyzer(data.password)

# -------- NICEGUI FRONTEND --------
@ui.page("/")
def home():
    # FULLSCREEN CENTERING
    with ui.element("div").classes(
        "w-screen h-screen flex items-center justify-center bg-gray-100"
    ):

        # CARD
        with ui.card().classes("w-[420px] p-8 shadow-xl rounded-2xl space-y-4"):

            ui.label("🔐 Password Checker") \
                .classes("text-2xl font-bold text-center")

            password_input = ui.input("Enter password") \
                .props("type=password outlined") \
                .classes("w-full")

            result_label = ui.label("") \
                .classes("text-center text-lg")

            def analyze_click():
                result = password_analyzer(password_input.value)

                score = result['score']

                if score == "weak":
                    color = "red"
                elif score == "medium":
                    color = "orange"
                else:
                    color = "green"

                result_label.text = f"Entropy: {result['entropy']:.2f} | Strength: {score}"
                result_label.style(f"color: {color}")

            ui.button("Analyze", on_click=analyze_click) \
                .classes("w-full mt-2 bg-blue-500 text-white rounded-lg")

# -------- CONNECT NICEGUI TO FASTAPI --------
ui.run_with(app)