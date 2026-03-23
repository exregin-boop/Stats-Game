import os
from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# Прокси для обхода ограничений
PROXIES = {
    "cr": "https://proxy.royaleapi.dev/v1",
    "coc": "https://cocproxy.royaleapi.dev/v1",
    "bs": "https://bsproxy.royaleapi.dev/v1"
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/<game>/players')
def get_stats(game):
    tag = request.args.get('tag')
    if not tag:
        return jsonify({"error": "No tag provided"}), 400

    # Очищаем тег от решетки, если она пришла
    clean_tag = tag.strip('#').strip()
    
    # Берем ключ из переменных Railway (Settings -> Variables)
    # Названия должны быть: CR_KEY, COC_KEY, BS_KEY
    key_name = f"{game.upper()}_KEY"
    api_key = os.getenv(key_name)

    if not api_key:
        return jsonify({"error": f"API Key {key_name} not found in Railway Variables"}), 500

    # Формируем финальный URL для прокси
    # Пример: https://proxy.royaleapi.dev/v1/players/%23YPJGC20PL
    url = f"{PROXIES.get(game)}/players/%23{clean_tag}"
    
    headers = {"Authorization": f"Bearer {api_key}"}
    
    try:
        response = requests.get(url, headers=headers)
        # Если Supercell вернул ошибку, пробрасываем её
        if response.status_code != 200:
            return jsonify(response.json()), response.status_code
            
        return jsonify(response.json())
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Railway сам подставит нужный порт
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
