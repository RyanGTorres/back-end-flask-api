from marshmallow import ValidationError, validates

def validate_cpf(cpf: str) -> bool:

    cpf_limpo = ''.join(filter(str.isdigit, cpf))
    
    # Verifica se tem 11 dígitos
    if len(cpf_limpo) != 11:
        raise ValidationError("CPF deve conter exatamente 11 dígitos.")
    
    # Verifica se todos os dígitos são iguais
    if cpf_limpo == cpf_limpo[0] * 11:
        raise ValidationError("CPF inválido: todos os dígitos são iguais.")
    
    # Calcula primeiro dígito verificador
    soma = sum(int(cpf_limpo[i]) * (10 - i) for i in range(9))
    resto = soma % 11
    digito1 = 0 if resto < 2 else 11 - resto
    
    if int(cpf_limpo[9]) != digito1:
        raise ValidationError("CPF inválido: primeiro dígito verificador incorreto.")
    
    # Calcula segundo dígito verificador
    soma = sum(int(cpf_limpo[i]) * (11 - i) for i in range(10))
    resto = soma % 11
    digito2 = 0 if resto < 2 else 11 - resto
    
    if int(cpf_limpo[10]) != digito2:
        raise ValidationError("CPF inválido: segundo dígito verificador incorreto.")
    
    return True