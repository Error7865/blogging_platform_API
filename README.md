

#   Blogging Platform API
A simple RESTful API with basic CRUD operations for a personal blogging platform.

Here a user can perform following operations:
* Create a new blog post
* Update an existing blog post
* Delete an existing blog post
* Get a single blog post
* Get all blog posts
* Filter blog posts by a search term


Before start you need to create a `.env` file with following values :

        REDIS_HOST = HOST_NAME
        REDIS_PORT = PORT
        DB = 0
        REDIS_PASSWORD = PASSWORD

               

Here all API urls:

## SignUp:

*endpoint* : `/api/signup`  \
*method* : **POST**    \
**Purpose** : Get count as user.

Pass a json file with `username` email and `password` password to count as user.

For example :

        {
            'username': username,
            'password': password
        }


## Create new article:-    
*endpoint* : `/api/article`  \
*method* : **POST**    \
**Purpose** : Create a new article
You must pass data which content below keys:    

        {
            'id': article_id,
            'title': article_title,
            'content': article_content,
            'category': article_category,
            'tags': article_tags,
        }

> __Note:__ You should pass username and password with requst.


## Get Any Article:
*endpoint* : `/api/article?id=0`  \
*method* : **GET**    \
**Purpose** : Get any article info.

You must replace value of `id`  with your desire article id.


## Get All Articles:
*endpoint* : `/api/posts?page=0`  \
*method* : **GET**    \
**Purpose** : Get all article info.

You must replace value of `page`  with a number and default value of it 0. Every page contain maximum 10 blog details.

## Update Article:

*endpoint* : `/api/posts/<id>`  \
*method* : **PUT**    \
**Purpose** : Update any existing  article.

## Delete Article:
*endpoint* : `/api/posts/<id>`  \
*method* : **DELETE**    \
**Purpose** : Delete article from records.

You must replace value of `id`  with your desire article id that you want to delete.
You must be writer of this article before it to 
delete.

## Filter Articles:
1. **Filter Base on Article Title:**

*endpoint* : `/posts/bytitle`  \
*method* : **GET**    \
**Purpose** : Get any article info.

It will return single article details.

2. ** Filter Base on Article : ** 


*endpoint* : `/posts/bytags`  \
*method* : **GET**    \
**Purpose** : Get list of articles  information.

It will return list of articles.
You must be owner of thoes articles to get all of thoes information.


This inspired by ([roadmap.sh](https://roadmap.sh/projects/blogging-platform-api))

