from flask import Blueprint, request, jsonify
from app.services.user_service import UserService
from app.models import user_schema
import logging


user_bp = Blueprint('users', __name__, url_prefix='/api/users')

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

user_schema_single = user_schema.UserSchema()
user_schema_many = user_schema.UserSchema(many=True)

@user_bp.route('/', methods=['GET'])
def get_all_users():
    page = request.args.get('page', default=1, type=int)
    perpage = request.args.get('perpage', default=10, type=int)

    if page < 1:
        return jsonify({'error': 'Página inválida. Deve ser maior que 0.'}), 400
    if perpage <=    page or perpage > 100:
        return jsonify({'error': 'Itens por página inválidos. Deve ser entre 1 e 100.'}), 400
    
    pagination = UserService.get_all_users(page=page, perpage=perpage)
    result = user_schema_many.dump(pagination)
    return jsonify(result), 200



@user_bp.route('/<uuid:user_id>', methods=['GET'])
def get_user_by_id(user_id):
    user = UserService.get_user_by_id(user_id)
    if not user:
        return jsonify({'error', 'Usuario não encontrado'}), 404
    
    user_data = user_schema_single.dump(user)
    return jsonify(user_data), 200

@user_bp.route('/email/<string:user_email>', methods=['GET'])
def get_user_by_email(user_email):
    user = UserService.get_user_by_email(user_email)

    if not user:
        return jsonify({'error':'Error ao encontrar usuario'}),404
    
    user_data = user_schema_single.dump(user)
    return jsonify(user_data),200


@user_bp.route('/<uuid:user_id>', methods=['PUT'])
def uptdate_user(user_id):
    try:
        json_data = request.get_json()
        valid_data = user_schema_single.load(json_data)
        
        if not json_data:
            return jsonify({'error': 'Confira e envie novamente'}), 400
        
        uptdate_user = UserService.update_user(
            user_id,
            username=valid_data['username'],
            email=valid_data['email'],
            cpf=valid_data['cpf']
        )       
        result = user_schema_single.dump(uptdate_user)
        return jsonify(result),200
    
    except ValueError as e:
        return jsonify({'error': str(e)}), 409



@user_bp.route('/', methods=['POST'])
def save_user():

    data = request.get_json()
    print("Recebi:", data, type(data))
    
    if not data or not all(k in data for k in ['username', 'email', 'cpf']):
        return jsonify({'error': 'Campos obrigatorios ausentes'}), 400
    
    try:
        print(type(data))
        print(data)
        validate_data = user_schema_single.load(data)
        
        new_user = UserService.create_user(
            username=validate_data['username'],
            email=validate_data['email'],
            cpf=validate_data['cpf']
        )
        
        result = user_schema_single.dump(new_user)

        return jsonify(result), 201
    
    except ValueError as e:
        return jsonify({'error': str(e)}), 409

@user_bp.route('/<uuid:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
    
    try:
        validate_data = user_schema_single.load(data)

        updated_user = UserService.update_user(
            username=validate_data.get('username'),
            email=validate_data.get('email'),
            cpf=validate_data.get('cpf')
        )
        
        result = user_schema_single.dump(updated_user)
        return jsonify(result), 200
    
    except ValueError as e:
        return jsonify({'error': str(e)}), 404


@user_bp.route('/<uuid:user_id>', methods=['DELETE'])
def delete_user(user_id):

    try:
        UserService.delete_user(user_id)
        return jsonify({'message': 'Usuário deletado com sucesso!'}), 200
    
    except ValueError as e:
        return jsonify({'error': str(e)}), 404