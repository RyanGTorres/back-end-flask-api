
from marshmallow import Schema, fields, ValidationError, validates
from marshmallow.validate import Length, Email
from app.ultils.cpf_validator import validate_cpf

class UserSchema(Schema):
    id = fields.UUID()
    username = fields.Str(
        required=True, 
        validate=Length(min=3, max=50, error ="O nome de usuario deve ter entre 3 e 50 caracteres")
    , error_messages={"required": "Nome de usuario é obrigatório",
                       "null": "Nome de usuario não pode ser nulo",
                       "invalid": "Nome de usuario inválido"})
    
    password = fields.Str(
        required=True,
        validate=Length(min=6, max=100, error="A senha deve ter entre 6 e 100 caracteres"))
    
    email = fields.Email(required=True, 
        validate=Length(max=100, error="O email deve ter no maximo 100 caracteres")
        ,error_messages={"required": "Email é obrigatório",
                       "null": "Email não pode ser nulo",
                       "invalid": "Email inválido"})
    
    cpf = fields.Str(required=True, validate=Length(equal=11, error="O CPF deve ter exatamente 11 caracteres")
                     , error_messages={"required": "CPF é obrigatório",
                       "null": "CPF não pode ser nulo",
                       "invalid": "CPF inválido"})
    
    
    def validate_cpf(cpf):
        validate_cpf(cpf)
        
class UserUpdateSchema(Schema):
    username = fields.Str(
        validate=Length(min=3, max=50, error ="O nome de usuario deve ter entre 3 e 50 caracteres")
    , error_messages={"null": "Nome de usuario não pode ser nulo",
                       "invalid": "Nome de usuario inválido"})
    
    password = fields.Str(
        validate=Length(min=6, max=100, error="A senha deve ter entre 6 e 100 caracteres"))
    
    email = fields.Email( 
        validate=Length(max=100, error="O email deve ter no maximo 100 caracteres")
        ,error_messages={"null": "Email não pode ser nulo",
                       "invalid": "Email inválido"})
    