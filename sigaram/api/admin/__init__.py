def create_login(f):
    '''
    Decorator for creating login
    '''
    print f.__name__
    def inner(*args, **kwargs):
        print type(args[1])
        return f(*args, **kwargs)

    return inner