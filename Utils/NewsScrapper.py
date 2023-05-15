from newspaper import build, Article
class NewsScrapper:
    def __init__(self, src_url):
        self.src_url = src_url;
        
    def __create_news_with(self, url):
        news = Article(url, language='ko')
        news.download();
        news.parse();
        return news;
        
    def __get_news_urls(self, num_of_news):
        urls = [];
        articles = build(self.src_url).articles;
        
        for article in articles[:num_of_news]:
            urls.append(article.url)
        
        return urls;
    
    def get_news(self, num_of_news): 
        news = []
        
        for url in  self.__get_news_urls(num_of_news): 
            news.append(self.__create_news_with(url))
        
        return news
 