from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os
from . import con

# from redis import 

class Redis:
    '''This class hold basic operation for redis database'''
    def __init__(self):
            pass

    def exists_key(self, key):
        '''It will check key exist or not'''
        if con.exists(key) == 1:
            return True
        return False

    def load(self, *args, **kwargs):
        raise NotImplementedError

    def set_sadd(self, key:str, value:list) -> None:
        '''take list value and add that to redis set'''
        for item in value:
            con.sadd(key, item)


class Admin(Redis):
    def __init__(self):
        self.email = os.environ.get('ADMIN')
    
    def verify_password(self, password):
        '''It will verify password
        and return boolean value base on it'''
        # hash_pswd = con.hget(f'admin', 'password')
        hash_pswd = os.environ.get('ADMIN_PASSWORD')
        return hash_pswd == password
    
    def __repr__(self):
        return f'<User {self.email}>'

class User(Redis):
    def __init__(self, email, *args, **kwargs):
        '''There have three place where user info store
        first hash that store user info `user:id`
        second set that store user email user:emails where
        store like `user@mail.com:id`
        third a list where all available id will store like 
        `user:id`
        '''
        self.email = email
        if self.is_user_exist(): 
            #user already exits so load info
            self.__load_user_info()
            
        # else:
        #     print('Not execute.')
        #user not exits so load only email & save other info
        # to redis when load call 
    
    def generate_id(self):
        '''It will generate unique id'''
        id = con.incr('user:id')
        while True:     # It will generate unique user id
            if not self.exists_key(f'user:{id}'):
                # user id already exist so increment id
                break
            print('Calling and calling again and again')
            id = con.incr('user:id')
        return id
    
    @property
    def password(self):
        raise ValueError('Password can\'t access')
    
    @password.setter
    def password(self, value):
        self.pswd = generate_password_hash(value)
    
    def verify_password(self, password):
        '''It will verify password
        and return boolean value base on it'''
        return check_password_hash(con.hget(f'user:{self.id}', 'password'), password)

    def is_user_exist(self):
        '''It will check user exist or not
        if user exist then set user id
        '''
        emails_with_id = con.smembers('user:emails')
        # print('Here emails with id ', emails_with_id)
        if len(emails_with_id) == 0:
            # it was empty so insert new records
            return False
        for email_with_id in emails_with_id:
            email, id = email_with_id.split(':')
            if email == self.email:
                # email found now check user id exist or not
                if con.hgetall(f'user:{id}') != {}:
                    self.id = int(id) # set user id
                    return True
        return False

    def __load_user_info(self) -> None:
        '''If user exists then it load recodrs to user instance'''
        try:
            data = con.hgetall(f'user:{self.id}')
            self.pswd = data['password']
            self.timestamp = datetime.fromisoformat(data['timestamp'])
            self.last_seen = datetime.fromisoformat(data['lastseen'])
        except AttributeError as e:
            pass

    def load_to_redis(self)->bool:
        '''It will load user data to redis'''
        if self.is_user_exist():    #user already exists
            return True
        try:
            self.id = self.generate_id()    #new user
            self.timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            self.last_seen = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            redis_hash = {
                # 'name': self.name,
                'email': self.email, 
                'password': self.pswd,
                'timestamp': self.timestamp,
                'lastseen': self.last_seen
                }
        
            con.hmset(f'user:{self.id}', redis_hash)
            con.sadd('user:emails', f'{self.email}:{self.id}')
            
            #remove from here after complete
            con.expire(f'user:{self.id}', 7*24*60*60) # expire after 7 days
            con.expire('user:emails', 7*24*60*60)
            #to here 
            
            # return redis_hash
            return True
        
        except AttributeError as e:
            print('Can\'t load you should set password.\n ', e)
            return False
    
    def articles(self)->list:
        '''Return list of atricle written by user'''
        set_of_article = con.smembers(f'articles:{self.id}')
        list_of_article = list()
        for item in set_of_article:
            article_id = item.split(':')[1]
            list_of_article.append(Article.get(article_id, self.id))
            # print('ARtricles id ', article_id)
        return list_of_article
    
    def is_article_exits(self, article_id:int)->bool:
        '''This will check article exists or not and
        return boolean value base on it'''
        for article in self.articles():
            if article_id == article.id:
                return True
        return False


    @classmethod
    def get(cls, user_id = None, email = None):
        '''This method will return user info base on eamil
        or user id 
        To get user required one of parameter value'''
        if email is None and user_id is None:
            raise ValueError('You should provide one of thoes value')
        if email is None:
            email = con.hget(f'user:{user_id}', 'email')
        return cls(email)
        

    def __repr__(self):
        return f'<User {self.email}>'

class Article(Redis):
    '''If you create new record then you can use class object
    if you want to retrive old record then you should use class method'''
    def __init__(self, user_id:int, title:str, content:str,
                  category:str, tags:list, id=None, *args, **kwargs)->None:
        '''Article details will store  `article:id`
        and a set articles'''
        self.title = title
        self.content = content
        self.category = category
        self.tags = list(tags)
        self.owner = User.get(user_id=user_id)
        self.create_at = datetime.now()
        self.update_at = datetime.now()
        if id is not None:      #for past records
            self.id = id

    def generate_id(self):
        '''It will generate unique id
        where key was `article_id:{owner_id}`'''
        id = con.incr(f'article_id:{self.owner.id}')
        con.expire(f'article_id:{self.owner.id}', 7*24*60*60) # expire after 7 days
        return int(id)

    def load(self, id=None):
        '''It will load article info at `article:{owner_id}:article_id`
        and owner's articles will store at `article:{owner_id}`'''
        article_info = {
            'title' : self.title,
            'content' : self.content,
            'category': self.category,
            'owner_id': self.owner.id,
            'createAt': self.create_at.strftime('%Y-%m-%d %H:%M'),
            'updateAt': self.update_at.strftime('%Y-%m-%d %H:%M')
        }
        if id is None:
            self.id = self.generate_id()
        else:
            self.id = id
        con.hset(f'article:{self.owner.id}:{self.id}', mapping=article_info)
        self.set_sadd(f'article:{self.owner.id}:{self.id}:tags', self.tags)
        con.sadd(f'articles:{self.owner.id}', f'article:{self.id}')
        # con.sadd('articles:id', f'article:{id}')        #list of present articles


        #remove from here after complete
        con.expire(f'article:{self.owner.id:{self.id}}', 7*24*60*60) # expire after 7 days
        con.expire(f'article:{self.owner.id}:{self.id}:tags', 7*24*60*60) # expire after 7 days
        con.expire(f'articles:{self.owner.id}', 7*24*60*60) # expire after 7 days
        #to here 

    def update(self, data:dict)->None:
        '''This will update article previous data'''
        self.title = data['title']
        self.content = data['content']
        self.category = data['category']
        self.tags = data['tags']
        self.update_at = datetime.now()

        self.load(self.id)


    @classmethod
    def get(cls, id:int, user_id:int):
        data = con.hgetall(f'article:{user_id}:{id}')
        tags = con.smembers(f'article:{user_id}:{id}:tags')
        article = cls(user_id, data['title'], data['content'],
        data['category'], tags)
        article.id = int(id)        #redis sent str data so make it int
        article.create_at = datetime.strptime(
            data['createAt'],
            '%Y-%m-%d %H:%M'
        )
        article.update_at = datetime.strptime(
            data['updateAt'],
            '%Y-%m-%d %H:%M'
        )
        return article

    def delete(self)->bool:
        try:
            con.delete(f'article:{self.owner.id}:{self.id}')
            con.delete(f'article:{self.owner.id}:{self.id}:tags')
            con.srem(f'articles:{self.owner.id}', f'article:{self.id}')
            return True
        except Exception as e:
            return False  

    def to_json(self)->dict:
        '''return json format dict'''
        return {
        'Id': self.id,
        'Title': self.title,
        'Content': self.content,
        'Category': self.category,
        'Tags': self.tags,
        'CreateAt': self.create_at.strftime('%Y-%m-%d %H:%M'),
        'UpdateAt': self.update_at.strftime('%Y-%m-%d %H:%M'),
        'Owner': self.owner.email
    }

    def __repr__(self):
        return f'<ID: {self.id}>, <OWNER: {self.owner.email}>'