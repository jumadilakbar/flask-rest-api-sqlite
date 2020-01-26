from flask import request, jsonify
from app import app
from .models import *
from .const import HttpStatus
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)
import requests
 
@app.route('/api/v1/news', methods=['GET'])
def news():
    if request.method == 'GET':
        construct = {
            'error': [],
            'success': True,
            'user': News.getAll()
        }
        response = jsonify(construct)
        response.status_code = HttpStatus.OK
    return response

@app.route('/api/v1/news/add', methods=['POST'])
def news_add():
    construct = {}
    try:
        country = request.form.get('country')
        category = request.form.get('category')
        apikey = request.form.get('apikey')
        url = "https://newsapi.org/v2/top-headlines?country="+country+"&category="+category+"&apiKey="+apikey
        data = requests.get(url)
        pre_data = data.json()
        for i in range(0, len(pre_data['articles'])):
            id_from_news = pre_data['articles'][i]['source']['id']
            name = pre_data['articles'][i]['source']['name']
            author = pre_data['articles'][i]['author']
            title = pre_data['articles'][i]['title']
            description = pre_data['articles'][i]['description']
            url = pre_data['articles'][i]['url']
            urlToImage = pre_data['articles'][i]['urlToImage']
            publishedAt = pre_data['articles'][i]['publishedAt']
            content = pre_data['articles'][i]['content']
            print("-------")
            news = News(
                id_from_news = id_from_news,
                name = name,
                author = author,
                title = title,
                description = description,
                url = url,
                urlToImage = urlToImage,
                publishedAt = publishedAt,
                content = content,
                country = country,
                category = category
                )
            news.save()
        jumlah = str(len(pre_data['articles']))
        data_masuk = jumlah+' Data saved'
        construct['success'] = True
        construct['message'] = data_masuk
        response = jsonify(construct)
        response.status_code = HttpStatus.CREATED
    except Exception as e:
        construct['success'] = False
        construct['error'] = str(e)
        response = jsonify(construct)
        response.status_code = HttpStatus.BAD_REQUEST
    return response

@app.route('/api/v1/news/filter', methods=['POST'])
def new_filter():
    construct = {}
    try:
        country = request.form.get('country')
        category = request.form.get('category')
        data_news = News.query.filter(News.country==country or News.category==category).all()
        
        if data_news == None :
            construct['success'] = True
            construct['mesagge'] = ' Data Null'
        else:
            result = []
            for news in data_news:
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
            construct['success'] = True
            construct['mesagge'] = 'get data by country or category'
            construct['data'] = result
        response = jsonify(construct)
        response.status_code = HttpStatus.CREATED
    except Exception as e:
        construct['success'] = False
        construct['error'] = str(e)
        response = jsonify(construct)
        response.status_code = HttpStatus.BAD_REQUEST
    return response

# @app.route('/api/v1/user/who_me', methods=['GET'])
# @jwt_required
# def who_me():
#     # Access the identity of the current user with get_jwt_identity
#     current_user = get_jwt_identity()
#     return jsonify(logged_in_as=current_user), 200

