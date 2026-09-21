from flask import Flask, request, jsonify
import datetime
import sys

app = Flask(__name__)

@app.route('/')
def home():
    print("HOME HIT", file=sys.stderr)
    return "Server is running!", 200

@app.route('/zapisz', methods=['GET', 'POST'])
def zapisz():
    lat = request.args.get('lat')
    lon = request.args.get('lon')
    
    # Force print to stderr so Render captures it immediately in logs
    print(f"RAW REQUEST RECEIVED: args={request.args}", file=sys.stderr)
    
    if lat and lon:
        czas = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        wpis = f"[{czas}] Lat: {lat}, Lon: {lon} | Maps: https://maps.google.com/?q={lat},{lon}\n"
        print(f"ZLAPANO WSPOLRZEDNE: {wpis}", file=sys.stderr)
        sys.stderr.flush()
        with open('wspolrzedne.txt', 'a', encoding='utf-8') as f:
            f.write(wpis)
        return jsonify({"status": "success", "lat": lat, "lon": lon}), 200
    
    print("BLAD: Brak wspolrzednych", file=sys.stderr)
    sys.stderr.flush()
    return jsonify({"status": "error", "message": "Brak wspolrzednych"}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
