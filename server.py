""" Server """
from bottle import (
    run, get, post, 
    response, request, 
    HTTPResponse)
from marshmallow import ValidationError
from models import Note, User
from schemas import NoteSchema, UserSchema
import json
from peewee import fn, IntegrityError
from authorization import requires_auth, get_token 

@get('/')
@requires_auth
def list_notes():
    """ List all notes """
    note = Note.select()
    schema = NoteSchema()
    result = schema.dump(note, many=True)
    response.content_type = 'application/json'
    return json.dumps(result.data)

@post('/')
@requires_auth
def create_note():
    """ Create a new note """
    note_data = request.json
    schema = NoteSchema()
    try:
        note = schema.load(note_data).data
    except ValidationError as err:
        response.status = 400
        return schema.get_validation_errors(err)
        
    note.save()
    result = schema.dump(note).data
    return HTTPResponse(result, status=201)  
    
@post('/signup/')
def signup():
    """ Create User """
    user_data = request.json
    schema = UserSchema()
    try:
        user = schema.load(user_data).data
    except ValidationError as err:
        response.status = 400
        return schema.get_validation_errors(err)

    try:
        query = User.insert(
        username=user.username,
        password=fn.make_password(user.password)).execute()
    except IntegrityError as err:
        return {
                "code": "username_already_exist",
                "description": "User does not exist"
                }
    result = schema.dump(user).data
    return HTTPResponse(result, status=201)

@post('/login/')
def login():
    """ User login """
    user_data = request.json
    schema = UserSchema()
    try: 
        user = schema.load(user_data).data
    except ValidationError as err:
        response.status = 400
        return schema.get_validation_errors(err)
    
    try:
        db_user = User.select().where(User.username == user.username).get()
    except User.DoesNotExist as err:
        return {
                "code": "user_does_not_exist",
                "description": "User does not exist"
                }

    if fn.check_password(user.password, db_user.password) == True:
        return get_token(user.username)


run(host='localhost', port=8000, debug=True)