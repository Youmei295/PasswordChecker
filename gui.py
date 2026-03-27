from nicegui import ui
import requests

API_URL = "http://127.0.0.1:8000/analyze"  # local API

@ui.page("/")
def home():
    with ui.element("div").classes(
        "w-screen h-screen flex items-center justify-center bg-gray-100"
    ):
        with ui.card().classes("w-[420px] p-8 shadow-xl rounded-2xl space-y-4"):

            ui.label("🔐 Password Checker") \
                .classes("text-2xl font-bold text-center")

            password_input = ui.input("Enter password") \
                .props("type=password outlined") \
                .classes("w-full")

            result_label = ui.label("").classes("text-center text-lg")

            def analyze_click():
                response = requests.post(API_URL, json={
                    "password": password_input.value
                })

                if response.status_code == 200:
                    result = response.json()
                    score = result['score']

                    if score == "weak":
                        color = "red"
                    elif score == "medium":
                        color = "orange"
                    else:
                        color = "green"

                    result_label.text = f"Entropy: {result['entropy']:.2f} | Strength: {score}"
                    result_label.style(f"color: {color}")
                else:
                    result_label.text = "Error calling API"

            ui.button("Analyze", on_click=analyze_click) \
                .classes("w-full mt-2 bg-blue-500 text-white rounded-lg")

ui.run()