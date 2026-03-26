from nicegui import ui
import requests

API_URL = "https://password-checker-api-h4hqbgf8bjbkd3dg.eastasia-01.azurewebsites.net/analyze"

def analyze():
    password = password_input.value

    response = requests.post(API_URL, json={
        "password": password
    })

    if response.status_code == 200:
        data = response.json()
        result_label.text = f"Entropy: {data['entropy']:.2f}, Strength: {data['score']}"
    else:
        result_label.text = "Error calling API"

ui.label("🔐 Password Checker").classes("text-2xl font-bold")

password_input = ui.input("Enter password").props("type=password")

ui.button("Analyze", on_click=analyze)

result_label = ui.label("")

ui.run()