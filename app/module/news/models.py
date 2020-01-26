from app import db

class News(db.Model):
    __tablename__ = 'news' #Must be defined the table name

    news_id = db.Column(db.Integer, unique=True, primary_key=True, nullable=False)
    id_from_news = db.Column(db.String)
    name = db.Column(db.String)
    author = db.Column(db.String)
    title = db.Column(db.String)
    description  = db.Column(db.String(1000))
    url = db.Column(db.String(1000))
    urlToImage = db.Column(db.String(1000))
    publishedAt = db.Column(db.String)
    content = db.Column(db.String(10000))
    country = db.Column(db.String)
    category = db.Column(db.String)

    def __init__(self, id_from_news, name, author, title, description, url, urlToImage, publishedAt, content, country, category):
        self.id_from_news = id_from_news
        self.name = name
        self.author = author
        self.title = title
        self.description = description
        self.url = url
        self.urlToImage = urlToImage
        self.publishedAt = publishedAt
        self.content = content
        self.country = country
        self.category = category

    def __repr__(self):
        return "<Name: {}".format(self.name)

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def getAll():
        datanews = News.query.all()
        result = []
        for news in datanews:
            obj = {
                "id_from_news" : news.id_from_news,
                "name" : news.name,
                "author" : news.author,
                "title" : news.title,
                "description" : news.description,
                "url" : news.url,
                "urlToImage" : news.urlToImage,
                "publishedAt" : news.publishedAt,
                "content" : news.content,
                "country" : news.country,
                "category": news.category
            }
            result.append(obj)
        return result

    def delete(self):
        db.session.delete(self)
        db.session.commit()
