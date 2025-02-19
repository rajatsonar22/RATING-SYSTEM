#updated code
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# In-memory storage for ratings
ratings_list = []

# Secret key for checking votes
SECRET_KEY = "admin123"  # Change this to your own secret key

@app.route('/')
def home():
    return render_template("index.html")  # Serve frontend

@app.route('/rate', methods=['POST'])
def rate():
    try:
        data = request.json
        team = data.get("team")
        rating = data.get("rating")

        if not all([team, rating]):
            return jsonify({"error": "Missing required fields"}), 400

        # Store rating in memory
        ratings_list.append({"Team": team, "Rating": rating})

        return jsonify({"message": "Rating submitted successfully!"})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/check_votes', methods=['POST'])
def check_votes():
    try:
        data = request.json
        entered_key = data.get("key")

        if entered_key == SECRET_KEY:
            total_votes = len(ratings_list)
            return jsonify({"total_votes": total_votes})
        else:
            return jsonify({"error": "Invalid key"}), 403

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
