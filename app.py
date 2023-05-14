import os

import openai
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")
test_news_headline_input = "이르면 16일 전기료 인상, ‘냉방비 폭탄’ 여부 날씨에 달렸다… 외식업·상가발 물가상승 불가피";

@app.route("/", methods=("GET", "POST"))
def index():
    if request.method == "POST":
        print('request POST started.');
        news_headline = test_news_headline_input;
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=generate_prompt(news_headline),
            temperature=0.6,
            n=1,
            max_tokens=256,
            stop=None,
        )
        print(response);
        return redirect(url_for("index", result=response.choices[0].text))

    result = request.args.get("result")
    return render_template("index.html", result=result)


def generate_prompt(animal):
    return """Suggest three names for an animal that is a superhero.

def generate_prompt(news_headline):
    return """Suggest a podcast script about '{}' as following form sheet\n"
          "제목: <br/>"
          "요약: <br/>"
          "\n\n"
          Please start writing the script.
          """.format(
        news_headline.capitalize()
    )
