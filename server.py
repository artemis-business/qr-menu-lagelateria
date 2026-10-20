from flask import Flask, jsonify, send_file
from flask_cors import CORS
import pymongo

app = Flask(__name__)
CORS(app)

# ⚠️ MONGODB LİNKİNİ BURAYA YAPIŞTIR
MONGODB_URL = "mongodb+srv://athenakh1010_db_user:TRAtr9DA3QVm9Dsd@cluster0.tu40bvl.mongodb.net"
client = pymongo.MongoClient(MONGODB_URL)
db = client["kafe_db"]
menu_koleksiyonu = db["menu"]
kategori_koleksiyonu = db["kategoriler"]

# VERCEL İÇİN ANA SAYFA YÖNLENDİRMESİ
@app.route('/')
def home():
    return send_file('index.html')

@app.route('/api/menu', methods=['GET'])
def get_menu():
    try:
        kategoriler = list(kategori_koleksiyonu.find({}, {"_id": 0})) 
        urunler = list(menu_koleksiyonu.find().sort("_id", -1))
        
        for urun in urunler:
            urun['_id'] = str(urun['_id'])
            
        return jsonify({
            "status": "success",
            "kategoriler": kategoriler,
            "urunler": urunler
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
