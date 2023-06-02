import requests
import nltk
from flask import Flask, render_template, url_for
from flask import request as req

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def Index():
    return render_template("index.html")


@app.route('/Summarize', methods=["GET", "POST"])
def Summarize():
    if req.method == "POST":
        API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
        headers = {
            "Authorization": f"Bearer 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"}

        data = req.form["inputdata"]

        rangeValue = int(req.form["maxL"])
        tokens = len(nltk.word_tokenize(data))
        maxLen = int((tokens * rangeValue) / 100)
        minLen = maxLen // 2

        def query(payload):
            response = requests.post(API_URL, headers=headers, json=payload)
            return response.json()

        output = query({
            "inputs": data,
            "parameters": {"min_length": minLen, "max_length": maxLen},
        })[0]

        return render_template("index.html", inputdata=data, res=output["summary_text"], )

    else:
        return render_template("index.html")


if __name__ == '__main__':
    app.debug = True
    app.run()
