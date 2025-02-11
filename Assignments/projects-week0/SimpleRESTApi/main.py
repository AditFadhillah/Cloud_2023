from flask import Flask, request, jsonify
import httpx

app = Flask(__name__)

@app.route("/getword/<word>")
def get_word(word):
    r = httpx.get("https://api.dictionaryapi.dev/api/v2/entries/en/" + word)
    return r.json()


if __name__ == "__main__":
    app.run(debug=True)