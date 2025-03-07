from flask import Flask, render_template
import requests

app = Flask(__name__)

# Функция для получения случайной цитаты с API
def get_random_quote():
    try:
        response = requests.get("https://zenquotes.io/api/random")
        print(f"Статус код: {response.status_code}")  # Отладка
        print(f"Ответ API: {response.text}")  # Отладка
        if response.status_code == 200:
            quote_data = response.json()[0]  # Ответ возвращается в виде списка
            return {
                "content": quote_data["q"],  # Текст цитаты
                "author": quote_data["a"]    # Автор
            }
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