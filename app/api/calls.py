from flask import request, g, jsonify
from . import api, auth
from .errors import bad_request, not_found, no_content
from ..data import Article, User



@api.post('/signup')
def signup():
    data = request.json
    for item in ['username', 'password']:
        if item not in list(data.keys()):
            return bad_request(item)
    user = User(data['username'])
    user.password = data['password']
    if user.is_user_exist():
        return bad_request('User already exists.')
    user.load_to_redis()
    return {
        'msg': 'User was successfully created.'
    }, 201

@api.get('/posts')
@auth.login_required
def get_posts():
    page = request.args.get('page') or '0'
    page = int(page)
    index = page * 10
    ls_of_article_json = []
    user_articles = g.current_user.articles()
    for article in user_articles[index:]:
        if index == page+10:
            break
        ls_of_article_json.append(article.to_json())
        index+=1
    if ls_of_article_json == []:
        return no_content('There was\'t any article.')
    return jsonify(ls_of_article_json)


@api.get('/article')
@auth.login_required
def get_article():
    article_id = request.args.get('id')
    if article_id is None:
        return bad_request('You should provide article id')
    user = g.current_user
    try:
        article_id = int(article_id)
    except ValueError as e:
        return bad_request(msg='You should check id')
    if not user.is_article_exits(article_id):
        return not_found('Article not found.')
    article = Article.get(article_id, user.id)
    return jsonify(article.to_json())

@api.post('/posts')
@auth.login_required
def create_new_articles():
    data = request.json
    for item in ['title', 'content', 'category', 'tags']:
        if item not in list(data.keys()): #check for missing field
            return bad_request(item)
    article = Article(g.current_user.id, data['title'],
                      data['content'], data['category'], data['tags'])
    article.load()  #load to redis    
    return {
        'id': article.id,
        'title': article.title,
        'content': article.content,
        'category': article.category,
        'tags': article.tags,
        'createAt': article.create_at.strftime('%Y-%m-%d %H:%M'),
        'updateAt': article.update_at.strftime('%Y-%m-%d %H:%M')
        }, 201

@api.put('/posts/<id>')
@auth.login_required
def update_article(id):
    data = request.json
    try:
        article_id = int(id)
    except ValueError as e:
        return bad_request(f'Invalid id {id}.')
    article = Article.get(article_id, g.current_user.id)
    # print('Current user ', g.current_user)
    for item in ['title', 'content', 'category', 'tags']:
        if item not in list(data.keys()):
            return  bad_request(f'{item} is missing.')
    old_data = {
                'Id': article.id,
        'Title': article.title,
        'Content': article.content,
        'Category': article.category,
        'Tags': article.tags,
        'CreateAt': article.create_at,
        'UpdateAt': article.update_at        
    }
    article.update(data)
    return {
        'old_data': old_data,
        'new_data':{
            'Id': article.id,
            'Title': article.title,
            'Content': article.content,
            'Category': article.category,
            'Tags': article.tags,
            'CreateAt': article.create_at,
            'UpdateAt': article.update_at
                }
    }, 201

@api.delete('/posts/<id>')
@auth.login_required
def delete(id):
        try:
            article_id = int(id)
        except ValueError as e:
            return bad_request(f'Invalid id {id}.')
        article = Article.get(article_id, g.current_user.id)
        if not article.delete():
            return bad_request('Invalid id ', id)
        return {
            'msg': f'Article with {article.id} id was successfully deleted.'
        }, 204

@api.get('/posts/bytitle')
@auth.login_required
def get_filter_posts():
    '''Get filter article info base on title'''
    data = request.json
    if 'title' not in list(data.keys()):
        return bad_request('You should provide title.')
    user = g.current_user
    for article in user.articles():
        if article.title == data['title']:
            return article.to_json()    
    return no_content('There was\'t any article.')


@api.get('/posts/bytags')
@auth.login_required
def get_filter_posts_base_tags():
    data = request.json 
    if 'tags' not in list(data.keys()):
        return bad_request('You should provide tags.')
    user = g.current_user
    tags = data['tags']
    list_of_article = list()
    for article in user.articles():
        for item in article.tags:
            #check all article tags item present in tags
            if item in tags and article.to_json() not in list_of_article:
                list_of_article.append(article.to_json())
    if list_of_article == []:
        return no_content()
    return jsonify({
        'articles': list_of_article
    })