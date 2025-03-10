from flask import Flask, render_template
import requests

app = Flask(__name__)

# Функция для получения случайной цитаты с API
def get_random_quote():
    try:
        response = requests.get("https://api.quotable.io/random")
        if response.status_code == 200:
            return response.json()  # Возвращаем цитату в формате JSON
        else:
            return None  # Если статус код не 200
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при запросе к API: {e}")
        return None

@app.route("/")
def home():
    # Получаем случайную цитату
    quote = get_random_quote()
    # Передаем цитату в шаблон
    return render_template("quotes.html", quote=quote)

if __name__ == "__main__":
    app.run(debug=True)