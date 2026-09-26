from flask import Flask, render_template, request, jsonify
from google import genai
import os

app = Flask(__name__)

# Get Gemini API key from environment variable
api_key = os.getenv("GEMINI_API_KEY")

# Create Gemini client
client = genai.Client(api_key=api_key)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():

    try:
        data = request.get_json()

        user_msg = data.get("message", "").strip()

        if not user_msg:
            return jsonify({
                "reply": "Please enter a question."
            })

        # Send the user's message to Gemini AI
        response = client.models.generate_content(
            model="gemini-3.8-flash",
            contents=user_msg
        )

        # Get AI response
        bot_reply = response.text

        return jsonify({
            "reply": bot_reply
        })

    except Exception as e:

        print("Error:", e)

        return jsonify({
            "reply": "Sorry, there was an error connecting to the AI service."
        }), 500


if __name__ == "__main__":
    app.run(debug=True)