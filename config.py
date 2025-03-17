
class Base:
    SECRET_KEY = 'don\'t guess it'


class Development(Base):
    pass

class Testing(Base):
    pass

class Production(Base):
    pass

config = {
    'dev': Development,
    'test': Testing,
    'deploy': Production
}