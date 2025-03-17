import unittest
import json
from base64 import b64encode
from faker import Faker
from app import crate_app

class TestAPI(unittest.TestCase):
    def setUp(self):
        self.app = crate_app('test')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()

    def tearDown(self):
        self.app_context.pop()

    def get_api_headers(self, email, password):
        return {
            'Authorization': 'Basic '+b64encode(f'{email}:{password}'.encode()).decode(), 
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
    
    def test_create_richi_by_sign_up(self):
        data = {
            'username': 'richi@mail.com',
            'password': 'richi'
        }
        response = self.client.post('/api/signup', headers = self.get_api_headers('richi@mail.com', 'richi'),
                                  data = json.dumps(data))

    def test_user_signup(self):
        '''test `/api/signup` url with post method'''
        f = Faker()
        email = f.email()
        password = f.password()
        data = {
            'username': email,
            'password': password
        }
        response = self.client.post('/api/signup', data = json.dumps(data),
                                    headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        })
        response_data = response.json
        self.assertEqual(201, response.status_code)
        self.assertIn('msg', list(response_data.keys()))


    # @unittest.skip
    def test_post_article(self):
        '''test `/api/article` url with post method'''
        f = Faker()
        title = f.text()
        content = f.text()+f.text()
        category = f.word()
        tags = f.words()
        data={
                'title': title,
                'content': content,
                'category': category,
                'tags': tags
            }
        response = self.client.post('/api/posts', headers = self.get_api_headers('richi@mail.com', 'richi'),
                                  data = json.dumps(data))
        response_data = response.json
        self.assertIn('title', list(response_data.keys()))
        self.assertEqual(title, response_data['title'])
        self.assertEqual(201, response.status_code)

        #testing `/api/article` url with GET method
        get_response = self.client.get(f'/api/article?id={response_data['id']}',
                                        headers = self.get_api_headers('richi@mail.com', 'richi'))
        get_data = get_response.json
        self.assertEqual(content, get_data['Content'])
        self.assertEqual(title, get_data['Title'])

    def test_update_article(self):
        f = Faker()
        #testing `/api/posts/<id>` for update article 
        new_title = f.text()
        new_content = f.text()+f.text()
        new_category = f.word()
        new_tags = f.words()
        data={
                'title': new_title,
                'content': new_content,
                'category': new_category,
                'tags': new_tags
            }
        put_response = self.client.put(f'/api/posts/{2}',
                                       headers = self.get_api_headers('richi@mail.com', 'richi'),
                                       data = json.dumps(data))
        put_data = put_response.json
        # print('here response data  \n', put_response.get_data(as_text=True))
        self.assertEqual(201, put_response.status_code)
        # self.assertEqual(put_data['old_data']['title'], title)
        self.assertEqual(put_data['new_data']['Title'], new_title)

    def test_delete_article(self):
        '''test `/api/posts/<id>` with delete method'''
        f = Faker()
        title = f.text()
        content = f.text()+f.text()
        category = f.word()
        tags = f.words()
        data={
                'title': title,
                'content': content,
                'category': category,
                'tags': tags
            }
        response = self.client.post('/api/posts', headers = self.get_api_headers('richi@mail.com', 'richi'),
                                  data = json.dumps(data))
        response_data = response.json
        #A new article created 

        delete_response = self.client.delete(f'/api/posts/{response_data["id"]}',
                                headers = self.get_api_headers('richi@mail.com', 'richi'))
        
        self.assertEqual(204, delete_response.status_code)

    def test_user_all_articles(self):
        response = self.client.get('/api/posts',
                                   headers = self.get_api_headers('richi@mail.com', 'richi'))
        response_data = response.json
        self.assertEqual(len(response_data), 10)

        #test for no content
        response = self.client.get('/api/posts?page=204',
                                   headers = self.get_api_headers('richi@mail.com', 'richi'))
        self.assertEqual(response.status_code, 204)

    def test_filter_article_by_title(self):
        '''test `/api/posts/bytitle` with get method'''
        #create a new article
        f = Faker()
        title = f.text()
        content = f.text()+f.text()
        category = f.word()
        tags = f.words()
        data={
                'title': title,
                'content': content,
                'category': category,
                'tags': tags
            }
        response = self.client.post('/api/posts', headers = self.get_api_headers('richi@mail.com', 'richi'),
                                  data = json.dumps(data))
        article = response.json

        #testing filter by title
        response = self.client.get('/api/posts/bytitle', headers = self.get_api_headers('richi@mail.com', 'richi'),
                                  data = json.dumps({
                                      'title': title
                                  }))
        got_article = response.json

        self.assertEqual(article['id'],
                         got_article['Id'])
        self.assertEqual(got_article['Title'],
                         title)
        
    def test_filter_article_by_tags(self):
        '''test `/api/posts/bytags` with get method'''
        f = Faker()
        title = f.text()
        content = f.text()+f.text()
        category = f.word()
        tags = f.words()
        data={
                'title': title,
                'content': content,
                'category': category,
                'tags': tags
            }
        title1 = f.text()
        content1 = f.text()+f.text()
        category1 = f.word()
        tags1 = f.words()
        data1={
                'title': title1,
                'content': content1,
                'category': category1,
                'tags': tags1
            }
        #create two new article 
        response = self.client.post('/api/posts', headers = self.get_api_headers('richi@mail.com', 'richi'),
                                  data = json.dumps(data))
        test_data = response.json
        v='hello'
        response_id = response.json['id']
        response1 = self.client.post('/api/posts', headers = self.get_api_headers('richi@mail.com', 'richi'),
                                  data = json.dumps(data1))
        response1_id = response1.json['id']

        #testing filter by tags
        response = self.client.get('/api/posts/bytags', headers = self.get_api_headers('richi@mail.com', 'richi'),
                                   data = json.dumps({
                                       'tags': [tags[0], tags1[1]]
                                   }))
        response_data = response.json
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response_data['articles']), 2)
    