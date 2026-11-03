# pip install flask requests
from flask import Flask, render_template_string, jsonify
import requests, json

app = Flask(__name__)

# ------------------- 1. CRYPTO API (CoinGecko) -------------------
def fetch_crypto():
    try:
        url = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids=bitcoin,ethereum,solana,cardano&per_page=4"
        r = requests.get(url, timeout=10)
        return r.json()
    except:
        return []

# ------------------- 2. WEATHER API (Open-Meteo) -------------------
def fetch_weather():
    try:
        url = "https://api.open-meteo.com/v1/forecast?latitude=31.5&longitude=74.3&current_weather=true"
        r = requests.get(url, timeout=10)
        return r.json().get("current_weather", {})
    except:
        return {}

# ------------------- 3. CURRENCY API (ExchangeRate-API) -------------------
def fetch_currency():
    try:
        url = "https://api.exchangerate-api.com/v4/latest/USD"
        r = requests.get(url, timeout=10)
        data = r.json()
        return {
            "USD_PKR": data["rates"].get("PKR"),
            "USD_EUR": data["rates"].get("EUR"),
            "USD_GBP": data["rates"].get("GBP"),
            "USD_INR": data["rates"].get("INR")
        }
    except:
        return {"USD_PKR": "N/A"}

# ------------------- 4. NEWS API (HackerNews Algolia) -------------------
def fetch_news():
    try:
        url = "https://hn.algolia.com/api/v1/search?query=technology&tags=story&hitsPerPage=4"
        r = requests.get(url, timeout=10)
        all_news = r.json().get("hits", [])
        return all_news[1:]
    except:
        return []

# ------------------- 5. FILE HANDLING -------------------
def save_all(data):
    with open("all_data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

# ------------------- 6. FRONTEND (HTML/CSS/JS) -------------------
HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
<title>4-in-1 Automation Tool</title>
<style>
body{font-family: 'Segoe UI', Arial; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height:100vh; color:white; text-align:center; padding:20px; margin:0;}
h1{font-size:32px; margin-bottom:5px;}
.buttons{margin:20px 0;}
.btn{padding:12px 22px; margin:8px; border:none; border-radius:25px; cursor:pointer; font-size:15px; font-weight:bold; color:white; transition:0.3s;}
.btn-crypto{background:#f59e0b;} .btn-weather{background:#06b6d4;} .btn-currency{background:#10b981;} .btn-news{background:#ef4444;}
.btn:hover{transform:scale(1.1);}
.card{background:rgba(255,255,255,0.15); backdrop-filter:blur(10px); padding:18px; margin:12px; border-radius:15px; display:inline-block; width:230px; box-shadow:0 8px 20px rgba(0,0,0,0.2); text-align:left; vertical-align:top;}
.row-title{font-size:22px; margin-top:30px; background:rgba(0,0,0,0.2); display:inline-block; padding:8px 20px; border-radius:20px;}
</style>
</head>
<body>
<h1>🤖 4-in-1 Python Automation Tool</h1>
<p>Frontend + Backend + Multiple External APIs + File Handling</p>
<div class="buttons">
<button class="btn btn-crypto" onclick="showSection('crypto')">💰 Crypto</button>
<button class="btn btn-weather" onclick="showSection('weather')">🌤️ Weather</button>
<button class="btn btn-currency" onclick="showSection('currency')">💵 Currency</button>
<button class="btn btn-news" onclick="showSection('news')">📰 News</button>
<button class="btn" style="background:#3b82f6;" onclick="loadData()">🔄 Fetch All (Show All)</button>
</div>
<div id="result">Loading...</div>
<script>
let allData = {};
async function loadData(){
    document.getElementById('result').innerHTML = "<h2>⏳ Fetching all APIs...</h2>";
    let res = await fetch('/api/data');
    allData = await res.json();
    showAllSections();
}
function showAllSections(){
    let html = "";
    html += "<div class='row-title'>💰 Crypto Market (4 Coins)</div><br>";
    allData.crypto.forEach(c=>{
        html += `<div class="card"><h3>${c.name} (${c.symbol.toUpperCase()})</h3><h2>$${c.current_price}</h2><p>24h: ${c.price_change_percentage_24h?.toFixed(2)}%</p></div>`;
    });
    let w = allData.weather;
    html += `<br><div class='row-title'>🌤️ Lahore Weather - Live</div><br><div class="card"><h3>Temperature: ${w.temperature}°C</h3><p>Wind: ${w.windspeed} km/h</p><p>Time: ${w.time}</p></div>`;
    let c = allData.currency;
    html += `<br><div class='row-title'>💵 USD Exchange Rates</div><br>
    <div class="card"><h3>🇵🇰 1 USD = ${c.USD_PKR} PKR</h3></div>
    <div class="card"><h3>🇪🇺 1 USD = ${c.USD_EUR} EUR</h3></div>
    <div class="card"><h3>🇬🇧 1 USD = ${c.USD_GBP} GBP</h3></div>
    <div class="card"><h3>🇮🇳 1 USD = ${c.USD_INR} INR</h3></div>`;
    html += "<br><div class='row-title'>📰 Latest Tech News</div><br>";
    allData.news.forEach(n=>{
        let date = new Date(n.created_at).toLocaleDateString();
        html += `<div class="card" style="width:320px;"><h4 style="margin-top:0;">${n.title}</h4><p style="font-size:13px; opacity:0.8;">📅 ${date} | 👍 ${n.points} points</p><p style="font-size:13px;">by ${n.author}</p><a href="${n.url}" target="_blank" style="background:#facc15; color:black; padding:8px 15px; border-radius:20px; text-decoration:none; font-weight:bold; display:inline-block; margin-top:10px;">Read Full News →</a></div>`;
    });
    document.getElementById('result').innerHTML = html;
}
function showSection(type){
    let html = "";
    if(type=='crypto'){
        html += "<div class='row-title'>💰 Crypto Market (4 Coins)</div><br>";
        allData.crypto.forEach(c=>{
            html += `<div class="card"><h3>${c.name} (${c.symbol.toUpperCase()})</h3><h2>$${c.current_price}</h2><p>24h: ${c.price_change_percentage_24h?.toFixed(2)}%</p></div>`;
        });
    }
    if(type=='weather'){
        let w = allData.weather;
        html += `<div class='row-title'>🌤️ Lahore Weather - Live</div><br><div class="card"><h3>Temperature: ${w.temperature}°C</h3><p>Wind: ${w.windspeed} km/h</p><p>Time: ${w.time}</p></div>`;
    }
    if(type=='currency'){
        let c = allData.currency;
        html += `<div class='row-title'>💵 USD Exchange Rates</div><br>
        <div class="card"><h3>🇵🇰 1 USD = ${c.USD_PKR} PKR</h3></div>
        <div class="card"><h3>🇪🇺 1 USD = ${c.USD_EUR} EUR</h3></div>
        <div class="card"><h3>🇬🇧 1 USD = ${c.USD_GBP} GBP</h3></div>
        <div class="card"><h3>🇮🇳 1 USD = ${c.USD_INR} INR</h3></div>`;
    }
    if(type=='news'){
        html += "<div class='row-title'>📰 Latest Tech News</div><br>";
        allData.news.forEach(n=>{
            let date = new Date(n.created_at).toLocaleDateString();
            html += `<div class="card" style="width:320px;"><h4 style="margin-top:0;">${n.title}</h4><p style="font-size:13px; opacity:0.8;">📅 ${date} | 👍 ${n.points} points</p><p style="font-size:13px;">by ${n.author}</p><a href="${n.url}" target="_blank" style="background:#facc15; color:black; padding:8px 15px; border-radius:20px; text-decoration:none; font-weight:bold; display:inline-block; margin-top:10px;">Read Full News →</a></div>`;
        });
    }
    document.getElementById('result').innerHTML = html;
}
loadData();
</script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_PAGE)

@app.route('/api/data')
def api_data():
    crypto = fetch_crypto()
    weather = fetch_weather()
    currency = fetch_currency()
    news = fetch_news()
    final = {"crypto": crypto, "weather": weather, "currency": currency, "news": news}
    save_all(final)
    return jsonify(final)

# ------------------- 8. RUN SERVER - FIXED -------------------
# ------------------- 8. RUN SERVER -------------------
if __name__ == '__main__':
    import webbrowser
    import threading

    # Ye function 1.5 second baad khud browser khol dega
    def open_browser():
        webbrowser.open_new("http://127.0.0.1:5000")

    threading.Timer(1.5, open_browser).start()
    
    app.run(debug=True, use_reloader=False, port=5000)