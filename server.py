import os
from flask import Flask, jsonify, send_file
from flask_cors import CORS
import pymongo
import certifi

app = Flask(__name__)
CORS(app)

MONGODB_URL = "mongodb+srv://athenakh1010_db_user:TRAtr9DA3QVm9Dsd@cluster0.tu40bvl.mongodb.net"
client = pymongo.MongoClient(MONGODB_URL, tlsCAFile=certifi.where(), serverSelectionTimeoutMS=10000)
db = client["kafe_db"]
menu_koleksiyonu = db["menu"]
kategori_koleksiyonu = db["kategoriler"]

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
HTML_YOLU = os.path.join(THIS_FOLDER, 'index.html')

@app.route('/')
def home():
    if os.path.exists(HTML_YOLU):
        return send_file(HTML_YOLU)
    return jsonify({"status": "error", "message": "HTML bulunamadı. Vercel klasör yapınızı kontrol edin."}), 404

@app.route('/logo.jpg')
def serve_logo():
    logo_yolu = os.path.join(THIS_FOLDER, 'logo.jpg')
    if os.path.exists(logo_yolu):
        return send_file(logo_yolu, mimetype='image/jpeg')
    return jsonify({"status": "error", "message": "Logo bulunamadı."}), 404

@app.route('/api/menu', methods=['GET'])
def get_menu():
    try:
        kategoriler = list(kategori_koleksiyonu.find({}, {"_id": 0})) 
        urunler = list(menu_koleksiyonu.find().sort("_id", -1))
        for urun in urunler:
            urun['_id'] = str(urun['_id'])
        return jsonify({"status": "success", "kategoriler": kategoriler, "urunler": urunler})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
