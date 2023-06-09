import os
import openai
from flask import Flask, redirect, render_template, request, url_for
from Utils.NewsScrapper import NewsScrapper
from Utils.SpeechGenerator import SpeechGenerator
from Utils.VideoGenerator.ThumbVideoGenerator import ThumbVideoGenerator
from Utils.YoutubeUploader import YouTubeUploader

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")
news_route_url = "https://news.naver.com/main/ranking/popularDay.naver"


@app.route("/", methods=("GET", "POST"))
def index():
    if request.method == "POST":
        print('Apppy - request POST started.')
        news = NewsScrapper(news_route_url).get_news(1)[0]
        news_headline = news.title
        news_description = news.text
        news_top_image = news.top_image

        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=generate_prompt(news_headline),
            temperature=0.6,
            n=1,
            max_tokens=256,
            stop=None,
        )

        ai_script = response.choices[0].text
        audio = SpeechGenerator().generate(ai_script, news_headline)
        if(news_top_image == ''):
            return redirect(url_for("index", result="got Errors."))
        ThumbVideoGenerator().generate(news_top_image, audio, news_headline)
        YouTubeUploader().upload_video(news_headline, news_description)
        return redirect(url_for("index", result=ai_script))

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
