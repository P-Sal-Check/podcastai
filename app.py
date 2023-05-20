import os
import openai
from flask import Flask, redirect, render_template, request, url_for
from Utils.NewsScrapper import NewsScrapper
from Utils.SpeechGenerator import SpeechGenerator

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")
news_route_url = "https://news.naver.com/main/ranking/popularDay.naver"


@app.route("/", methods=("GET", "POST"))
def index():
    if request.method == "POST":
        print('request POST started.')
        news_headline = NewsScrapper(news_route_url).get_news(1)[0].title
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=generate_prompt(news_headline),
            temperature=0.6,
            n=1,
            max_tokens=256,
            stop=None,
        )
        print(response)
        return redirect(url_for("index", result=response.choices[0].text))

    result = request.args.get("result")
    return render_template("index.html", result=result)


def generate_prompt(news_headline):
    return """Suggest a podcast script about '{}' as following form sheet\n"
          "제목: <br/>"
          "요약: <br/>"
          "\n\n"
          Please start writing the script.
          """.format(
        news_headline.capitalize()
    )
