from newspaper import build, Article

def main():
    cnn_paper = build("https://news.naver.com/main/ranking/popularDay.naver");
    urls = [];
    for article in cnn_paper.articles[:10]: # 상위 10개
        urls.append(article.url);

    for url in urls :
        artDetail = Article(url, language='ko');
        artDetail.download();
        artDetail.parse();
        print(artDetail.title);  


if __name__ == '__main__':
    main();