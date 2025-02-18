from flask import Flask, request, jsonify, send_file, render_template
import pandas as pd
import os

app = Flask(__name__)

# File to store ratings
FILE_PATH = "ratings.xlsx"

# Initialize Excel file if not exists
if not os.path.exists(FILE_PATH):
    df = pd.DataFrame(columns=["Team", "Rating"])
    df.to_excel(FILE_PATH, index=False)

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

        # Append rating to Excel
        df = pd.read_excel(FILE_PATH)
        new_entry = pd.DataFrame([{"Team": team, "Rating": rating}])
        df = pd.concat([df, new_entry], ignore_index=True)
        df.to_excel(FILE_PATH, index=False)

        return jsonify({"message": "Rating submitted successfully!"})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/download', methods=['GET'])
def download():
    try:
        return send_file(FILE_PATH, as_attachment=True)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
