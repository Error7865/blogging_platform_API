import unittest
import random
from faker import Faker
from datetime import datetime
from app.data import User, Article

class TestUser(unittest.TestCase):

    def test_user_instance(self):
        user = User('reab@mail.com', 'reba')
        self.assertIsNotNone(user.last_seen)
        
    @unittest.skip
    def test_article_instance(self):
        '''it contain some duplicate data so I skip it'''
        user = User('reab@mail.com')    #demo user
        f = Faker()
        a = Article(user.id, f.text(), f.text(160), f.word(),
                    f.words())
        a.load()
        self.assertEqual(datetime.now().strftime('%Y-%m-%d %H:%M'), 
                         a.create_at.strftime('%Y-%m-%d %H:%M'))

    @unittest.skip
    def test_user_articles(self):
        user = User.get(email = 'reab@mail.com')    #demo user
        articles = user.articles()
        self.assertEqual(type(articles), list)
        self.assertEqual(type(articles[0].title), type('string'))
        
    def test_user_article_exits(self):
        user = User('richi@mail.com')
        # print('articles :\n', user.articles())
        self.assertTrue(user.is_article_exits(4))
        self.assertFalse(user.is_article_exits(6))

    def test_delete_article(self):
        user = User('richi@mail.com')
        article = random.choice(user.articles())
        self.assertTrue(article.delete())