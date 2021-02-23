""" Schemas  """

from marshmallow import (
    Schema, fields, post_load, 
    ValidationError, validate,
    validates_schema
    )
from models import Note, User

class BaseSchema(Schema):
    """ Base schema """

    class Meta:
        """ Meta class """
        strict = True

    @validates_schema
    def validate_data(self, data):
        """ Check data is not empty """
        if not data:
            raise ValidationError("Data is empty")
    
    def get_validation_errors(self, err):
        """ Return errors in JSON. """
        return {
            "code": "note_validation_error",
            "description": [e for e in err.messages.values()]
        }
        
class NoteSchema(BaseSchema):
    """ Schema for Note serilization """
    title = fields.Str(required=True, validate=validate.Length(max=60))
    content = fields.Str()
    created = fields.DateTime()

    @post_load
    def create_note(self, data, **kwargs):
        """ Return Note object """
        return Note(**data)


class UserSchema(BaseSchema):
    """ Schema for User serilization """
    username = fields.Str(required=True, validate=validate.Length(max=60))
    password = fields.Str(required=True, validate=validate.Length(max=60))
    join_date = fields.DateTime()
    
    @post_load
    def create_user(self, data, **kwargs):
        """ Return Note object """
        return User(**data)