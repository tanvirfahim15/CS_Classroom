from paths.Blog import ArticleStrategy

class BlogArticleConcreteStrategy(ArticleStrategy.ArticleStrategy):
    title = ""
    body = ""
    author = ""

    def BlogArticleConcreteStrategy(self):
        pass

    def create_article(self, title, body, author):
        self.title = title
        self.body = body
        self.author = author

    def getTitle(self):
        return self.title

    def getBody(self):
        return self.body

    def getAuthor(self):
        return self.author

    def setTitle(self, title):
        self.title = title

    def setBody(self, body):
        self.body = body

    def setAuthor(self, author):
        self.author = author