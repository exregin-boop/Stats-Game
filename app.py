from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# Сюда вставь свои токены с сайтов разработчиков
KEYS = {
    "clash_royale": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6IjMzMDE0MzAyLWJmZWItNGFlMy1hOGRiLTgzNDI4ZDdlOWFiNSIsImlhdCI6MTc3NDI1MjQ1NSwic3ViIjoiZGV2ZWxvcGVyLzYzZTgwOWYxLTk1MDAtMTYxNi0zZDIwLTBiZjA0MTc2YTA4MSIsInNjb3BlcyI6WyJyb3lhbGUiXSwibGltaXRzIjpbeyJ0aWVyIjoiZGV2ZWxvcGVyL3NpbHZlciIsInR5cGUiOiJ0aHJvdHRsaW5nIn0seyJjaWRycyI6WyI0NS43OS4yMTguNzkiXSwidHlwZSI6ImNsaWVudCJ9XX0.fmMvcEYRTR7d-20ltfJRtuf2EWd6-DVdxYmtFib36URZvwDi8nSb3S08xGDnf1HUE1PAPNC7gNWN96ETHt5g2A",
    "clash_of_clans": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6IjhjNzlhOTI0LWQ2M2ItNDk2NS05NTFkLTA4OTlmNmY0NjM1NyIsImlhdCI6MTc3NDI1MjY3NSwic3ViIjoiZGV2ZWxvcGVyLzYxYzBjNjkzLTBjMGUtZDMxOC0xZGEyLWI0YjZlNmE5YzYwMyIsInNjb3BlcyI6WyJjbGFzaCJdLCJsaW1pdHMiOlt7InRpZXIiOiJkZXZlbG9wZXIvc2lsdmVyIiwidHlwZSI6InRocm90dGxpbmcifSx7ImNpZHJzIjpbIjQ1Ljc5LjIxOC43OSJdLCJ0eXBlIjoiY2xpZW50In1dfQ.XlrZbw7dX1nMRxXEfnF3sIL802S90UKRM7aEWtalyFZHKQpi5Hx8LOvihNs1c-FfiTpAVOjtvBQT4kt8PSquBg",
    "brawl_stars": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6ImJmYWM0NWNkLTFkNjctNDQxNC04ZjNjLWVmNjc2NmZlMmJmYyIsImlhdCI6MTc3NDI1MjkzNSwic3ViIjoiZGV2ZWxvcGVyL2Y1MGI0YzdiLWIxMGEtZmI1NS04ZmM2LTZlNzZkYmM0MmI0YSIsInNjb3BlcyI6WyJicmF3bHN0YXJzIl0sImxpbWl0cyI6W3sidGllciI6ImRldmVsb3Blci9zaWx2ZXIiLCJ0eXBlIjoidGhyb3R0bGluZyJ9LHsiY2lkcnMiOlsiNDUuNzkuMjE4Ljc5Il0sInR5cGUiOiJjbGllbnQifV19.Vrm_jCU5yEjKrca-vRpP4lazn6pprBsas3hL1cn76k9USykVkUS7p4zaAY6s_t4lkXzBpnghm5EpldMyJXS1Ng"
}

@app.route('/')
def index():
    return render_template('index.html') # Твой HTML файл

@app.route('/get_stats', methods=['POST'])
def get_stats():
    data = request.json
    game = data.get('game')
    tag = data.get('tag').strip('#').upper()
    
    proxies = {
        "clash_royale": "https://proxy.royaleapi.dev/v1/players/%23",
        "clash_of_clans": "https://cocproxy.royaleapi.dev/v1/players/%23",
        "brawl_stars": "https://bsproxy.royaleapi.dev/v1/players/%23"
    }

    url = f"{proxies[game]}{tag}"
    headers = {"Authorization": f"Bearer {KEYS[game]}"}
    
    response = requests.get(url, headers=headers)
    return jsonify(response.json())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
