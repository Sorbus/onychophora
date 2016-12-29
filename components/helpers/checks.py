def serverowner(function):
    """
    Limits function to the server owner
    """

    def wrapper(*args, **kwargs):
        
        
        return function(*args, **kwargs)
    return wrapper