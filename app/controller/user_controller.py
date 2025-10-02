from flask import Blueprint, request, jsonify, current_app
from app.services.user_service import UserService
from app.models import user_schema
from flask_jwt_extended import jwt_required , create_access_token, get_jwt_identity
from datetime import timedelta



user_bp = Blueprint('users', __name__, url_prefix='/api/users')

user_schema_single = user_schema.UserSchema()
user_schema_many = user_schema.UserSchema(many=True)
user_update_schema = user_schema.UserUpdateSchema()

@user_bp.route('/register', methods=['POST'])
def save_user():

    data = request.get_json()
    print(data)
    print(type(data))
    
    if not data or not all(k in data for k in ['username', 'password','email', 'cpf']):
        return jsonify({'error': 'Campos obrigatorios ausentes'}), 400
    
    try:
        validate_data = user_schema_single.load(data)
        
        new_user = UserService.create_user(
            username=validate_data['username'],
            email=validate_data['email'],
            password=validate_data['password'],
            cpf=validate_data['cpf']
        )
        
        result = user_schema_single.dump(new_user)
        current_app.logger.info(f"Novo usuario cadastrado: {new_user.username}")
        return jsonify(result), 201
    
    except ValueError as e:
        current_app.logger.error(f"Erro ao cadastrar usuario: {str(e)}")
        return jsonify({'error': str(e)}), 409

@user_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    
    if not data or not all(k in data for k in ['email', 'password']):
        return jsonify({'error': 'Campos obrigatorios ausentes'}), 400
    
    try:
        user = UserService.verify_login_user(data['email'], data['password'])
        token = create_access_token(identity=str(user.id),
                                    expires_delta=timedelta(hours=1))
        return jsonify({'access_token': token}), 200
    
    except ValueError as e:
        return jsonify({'error': str(e)}), 401

@user_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    try:
        user_id = get_jwt_identity()
        user = UserService.get_user_by_id(user_id)
        return jsonify(user_schema_single.dump(user)), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404



@user_bp.route('/', methods=['GET'])
@jwt_required()
def get_all_users():
    try:
        page = request.args.get('page', default=1, type=int)
        perpage = request.args.get('perpage', default=10, type=int)
        if page < 1:
            return jsonify({'error': 'Página inválida. Deve ser maior que 0.'}), 400
        if perpage < 1 or perpage > 100:
            return jsonify({'error': 'Itens por página inválidos. Deve ser entre 1 e 100.'}), 400
        pagination = UserService.get_all_users(page=page, perpage=perpage)
        result = user_schema_many.dump(pagination)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@user_bp.route('/<uuid:user_id>', methods=['GET'])
@jwt_required()
def get_user_by_id(user_id):
    user = UserService.get_user_by_id(user_id)
    if not user:
        return jsonify({'error': 'Usuario não encontrado'}), 404
    
    user_data = user_schema_single.dump(user)
    return jsonify(user_data), 200

@user_bp.route('/email/<string:user_email>', methods=['GET'])
@jwt_required()
def get_user_by_email(user_email):
    user = UserService.get_user_by_email(user_email)

    if not user:
        return jsonify({'error':'Error ao encontrar usuario'}),404
    
    user_data = user_schema_single.dump(user)
    return jsonify(user_data),200


@user_bp.route('/<uuid:user_id>', methods=['PUT'])
@jwt_required()
def uptdate_user(user_id):
    try:
        json_data = request.get_json()
        valid_data = user_update_schema.load(json_data)
        
        if not json_data:
            return jsonify({'error': 'Confira e envie novamente'}), 400
        
        uptdate_user = UserService.update_user(
            user_id,
            username=valid_data.get('username'),
            password=valid_data.get('password'),
            email=valid_data.get('email'),
        )       
        result = user_update_schema.dump(uptdate_user)
        return jsonify(result),200
    
    except ValueError as e:
        return jsonify({'error': str(e)}), 409

@user_bp.route('/<uuid:user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):

    try:
        UserService.delete_user(user_id)

        return jsonify({'message': 'Usuário deletado com sucesso!'}), 200
    
    except ValueError as e:
        return jsonify({'error': str(e)}), 404