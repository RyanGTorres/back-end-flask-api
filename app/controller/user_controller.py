from flask import Blueprint, request, jsonify
from app.services.user_service import UserService
import logging

user_bp = Blueprint('users', __name__, url_prefix='/api/users')

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

@user_bp.route('/', methods=['GET'])
def get_all_users():
    users = UserService.get_all_users()
    return jsonify([user.to_json() for user in users]), 200


@user_bp.route('/<uuid:user_id>', methods=['GET'])
def get_user_by_id(user_id):
    user = UserService.get_user_by_id(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    return jsonify(user.to_json()), 200

@user_bp.route('/email/<string:user_email>', methods=['GET'])
def get_user_by_email(user_email):
    user = UserService.get_user_by_email(user_email)

    if not user:
        return jsonify({'error':'Error ao encontrar usuario'}),404
    return jsonify(user.to_json()),200


@user_bp.route('/<uuid:user_id>', methods=['/PUT'])
def uptdate_user(user_id):
    data = request.get_json()
    try:
        UserService.update_user(
            username=data['username'],
            email=data['email'],
            cpf=data['cpf']
        )       
        return jsonify(data.to_json()),200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400



@user_bp.route('/', methods=['POST'])
def save_user():
    data = request.get_json()
    
    if not data or not all(k in data for k in ['username', 'email', 'cpf']):
        return jsonify({'error': 'Missing required fields'}), 400
    
    try:
        logger.info(f"Criando usuário: {data.get('username')}")
        
        new_user = UserService.create_user(
            username=data['username'],
            email=data['email'],
            cpf=data['cpf']
        )
        
        return jsonify(new_user.to_json()), 201
    
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

@user_bp.route('/<uuid:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
    
    try:
        updated_user = UserService.update_user(
            user_id,
            username=data.get('username'),
            email=data.get('email'),
            cpf=data.get('cpf')
        )
        
        return jsonify(updated_user.to_json()), 200
    
    except ValueError as e:
        return jsonify({'error': str(e)}), 404


@user_bp.route('/<uuid:user_id>', methods=['DELETE'])
def delete_user(user_id):

    try:
        UserService.delete_user(user_id)
        return jsonify({'message': 'Usuário deletado com sucesso!'}), 200
    
    except ValueError as e:
        return jsonify({'error': str(e)}), 404