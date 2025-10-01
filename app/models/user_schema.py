
from marshmallow import Schema, fields, ValidationError, validates
from marshmallow.validate import Length, Email

class UserSchema(Schema):
    id = fields.UUID()
    username = fields.Str(
        required=True, 
        validate=Length(min=3, max=50, error ="O nome de usuario deve ter entre 3 e 50 caracteres")
    , error_messages={"required": "Nome de usuario é obrigatório",
                       "null": "Nome de usuario não pode ser nulo",
                       "invalid": "Nome de usuario inválido"})
    
    email = fields.Email(required=True, 
        validate=Length(max=100, error="O email deve ter no maximo 100 caracteres")
        ,error_messages={"required": "Email é obrigatório",
                       "null": "Email não pode ser nulo",
                       "invalid": "Email inválido"})
    
    cpf = fields.Str(required=True, validate=Length(equal=11, error="O CPF deve ter exatamente 11 caracteres")
                     , error_messages={"required": "CPF é obrigatório",
                       "null": "CPF não pode ser nulo",
                       "invalid": "CPF inválido"})
    
    
@validates('cpf')
def validade_cpf(cpf):
    cpf_sem_acentuacao = cpf.replace('.', '').replace('-', '')

    if not cpf_sem_acentuacao.isdigit() or len(cpf_sem_acentuacao) != 11:
        raise ValidationError("CPF deve conter exatamente 11 dígitos numéricos.")
    
    if cpf_sem_acentuacao == cpf_sem_acentuacao[0] * 11:
        raise ValidationError("CPF inválido: todos os dígitos são iguais.")
    
    if validate_cpf_digits(cpf_sem_acentuacao):
        raise ValidationError("CPF inválido: dígitos verificadores incorretos.")
    
def validate_cpf_digits(cpf):
    def calculate_digit(cpf, factor):
        total = sum(int(digit) * (factor - index) for index, digit in enumerate(cpf))
        remainder = total % 11
        return '0' if remainder < 2 else str(11 - remainder)

    first_digit = calculate_digit(cpf[:9], 10)
    second_digit = calculate_digit(cpf[:10], 11)

    if cpf[-2:] != first_digit + second_digit:
        raise ValidationError("CPF inválido: dígitos verificadores incorretos.")
    
   