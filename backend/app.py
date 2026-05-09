from flask import Flask, jsonify, request
from flask_cors import CORS
from pymongo import MongoClient
from scraper import scrape_reviews

app = Flask(__name__)
CORS(app)

# Connect to local MongoDB
client = MongoClient("mongodb+srv://eliasebenezer2004_db_user:<kDB46ZGl0b4irVth>@cluster0.a3tda98.mongodb.net/?appName=Cluster0")
db = client["product_sentiment_db"]
reviews_collection = db["reviews"]

@app.route("/api/analyze", methods=["POST"])
def analyze_product():
    data = request.json
    url = data.get("url")
    
    if not url:
        return jsonify({"error": "URL is required"}), 400
        
    scraped_data = scrape_reviews(url)
    
    if scraped_data:
        # Clear old data for demo purposes, then insert new
        reviews_collection.delete_many({}) 
        reviews_collection.insert_many(scraped_data)
        return jsonify({"message": "Success", "count": len(scraped_data)})
        
    return jsonify({"error": "No reviews found"}), 404

@app.route("/api/dashboard", methods=["GET"])
def get_dashboard_data():
    # Fetch reviews and calculate sentiment distribution for the chart
    all_reviews = list(reviews_collection.find({}, {"_id": 0}))
    
    pipeline = [{"$group": {"_id": "$sentiment", "count": {"$sum": 1}}}]
    chart_data = [{"name": r["_id"], "value": r["count"]} for r in reviews_collection.aggregate(pipeline)]
    
    return jsonify({"reviews": all_reviews, "chartData": chart_data})

if __name__ == "__main__":
    app.run(debug=True, port=5000)
