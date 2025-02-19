from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# Store votes in a list (Temporary Storage - can be replaced with a database)
votes = []

# Admin Secret Key
SECRET_KEY = "admin123"  # Change this for security

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/rate', methods=['POST'])
def rate():
    try:
        data = request.json
        team = data.get("team")
        rating = data.get("rating")

        if not all([team, rating]):
            return jsonify({"error": "Missing required fields"}), 400

        # Store rating
        votes.append({"team": team, "rating": int(rating)})

        return jsonify({"message": "Rating submitted successfully!"})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/check_votes', methods=['POST'])
def check_votes():
    try:
        data = request.json
        key = data.get("key")

        if key != SECRET_KEY:
            return jsonify({"error": "Invalid key"}), 403

        # Count votes per team
        team_ratings = {}
        for vote in votes:
            team = vote["team"]
            if team in team_ratings:
                team_ratings[team]["total_votes"] += 1
                team_ratings[team]["total_rating"] += vote["rating"]
            else:
                team_ratings[team] = {"total_votes": 1, "total_rating": vote["rating"]}

        # Calculate average ratings
        results = {team: {"votes": data["total_votes"], "average_rating": round(data["total_rating"] / data["total_votes"], 1)}
                   for team, data in team_ratings.items()}

        return jsonify(results)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
