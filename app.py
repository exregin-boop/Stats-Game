import os
from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# Прокси для обхода блокировок (если сервер Railway не в РФ/РБ)
PROXIES = {
    "cr": "https://proxy.royaleapi.dev/v1",
    "coc": "https://cocproxy.royaleapi.dev/v1",
    "bs": "https://bsproxy.royaleapi.dev/v1"
}

# Ключи берем из переменных окружения Railway (Settings -> Variables)
API_KEYS = {
    "cr": os.getenv("CR_KEY"),
    "coc": os.getenv("COC_KEY"),
    "bs": os.getenv("BS_KEY")
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/<game>/<path:endpoint>')
def proxy_api(game, endpoint):
    tag = request.args.get('tag')
    if not tag:
        return jsonify({"error": "No tag provided"}), 400
    
    # Формируем URL. Если тег передан, добавляем его к эндпоинту
    url = f"{PROXIES[game]}/{endpoint}"
    if tag:
        # Для запросов типа /players/%23TAG
        url = url.replace("players/", f"players/%23{tag.strip('#')}")
    
    headers = {"Authorization": f"Bearer {API_KEYS[game]}"}
    
    try:
        response = requests.get(url, headers=headers)
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
