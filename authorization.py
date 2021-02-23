import jwt
from exceptions import AuthorizationError
from bottle import request, response

JWT_SECRET = 'secret'
JWT_ALGORITHM = 'HS256'

def jwt_token_from_header():
    """ Get token from header """

    auth = request.headers.get('Authorization', None)
    
    if not auth:
        raise AuthorizationError({'code': 'authorization_header_missing', 'description': 'Authorization header is expected'})
 
    parts = auth.split()
 
    if parts[0].lower() != 'bearer':
        raise AuthorizationError({'code': 'invalid_header', 'description': 'Authorization header must start with Bearer'})
    elif len(parts) == 1:
        raise AuthorizationError({'code': 'invalid_header', 'description': 'Token not found'})
    elif len(parts) > 2:
        raise AuthorizationError({'code': 'invalid_header', 'description': 'Authorization header must be Bearer + \s + token'})
 
    return parts[1]

def requires_auth(func):
    """Provides JWT based authentication for any decorated function assuming credentials available in an "Authorization" header"""
    def decorated(*args, **kwargs):
        try:
            token = jwt_token_from_header()
        except AuthorizationError as reason:
            response.status = 400
            return reason.msg          
 
        try:
            token_decoded = jwt.decode(token, JWT_SECRET)    # throw away value
        except jwt.DecodeError as message:
            response.status = 401 
            return {'code': 'token_invalid', 'description': message.args[0]} 
        
 
        return func(*args, **kwargs)
 
    return decorated

def get_token(username):
    """ Return user's token """  
    encoded_jwt = jwt.encode({"user":username}, JWT_SECRET, JWT_ALGORITHM)
    return ({'token': encoded_jwt.decode('utf-8')})