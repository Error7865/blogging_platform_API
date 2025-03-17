from app import crate_app
from app.data import con, Admin, User, Article

app = crate_app('dev')

@app.cli.command()
def test():
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity = 2).run(tests)

@app.shell_context_processor
def load_shell_data():
    return {
        'con': con,
        'Admin': Admin,
        'User': User, 
        'Article': Article
    }

if __name__ == "__main__":
    app.run(debug=True)


    #testing some code 
    # from faker import Faker
    # f = Faker()
    # u = User('robin@mail.com')
    # u.password = 'robin'
    # u.load_to_redis()
    # print('Here was password ', u.pswd)
    # from werkzeug.security import check_password_hash
    # check = check_password_hash(u.pswd, 'robin')
    # # u.id
    # print('Here verify password ', u.verify_password('robin'))
    # from app import con
    # print('password:  ', con.hget('user:3', 'password'))
    #remove those later
