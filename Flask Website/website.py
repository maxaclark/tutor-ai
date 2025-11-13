from flask import Flask, render_template, request, jsonify, session
from tutorbot import init_conversation, get_bot_response
from flask_cors import CORS
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)
CORS(app)

@app.route("/")
def index():
    if "messages" not in session:
        session["messages"] = init_conversation()
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json["message"]
    messages = session.get("messages", init_conversation())
    bot_reply, updated_messages = get_bot_response(user_input, messages)
    session["messages"] = updated_messages
    return jsonify({"response": bot_reply})

if __name__ == "__main__":
    app.run(debug=True)



# to start the server run
# pip install -r sitereqs.txt
# python website.py