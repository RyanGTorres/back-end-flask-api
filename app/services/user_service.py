from app import db
from app.models.user import User
from sqlalchemy.exc import IntegrityError


class UserService:

    @staticmethod
    def get_all_users(page=1,perpage=10):
        """Retorna todos os usuarios"""
        return User.query.paginate(
            page=page, 
            per_page=perpage, 
            error_out=False).items
    
    @staticmethod
    def get_user_by_id(user_id):
        """Busca usuario pelo id"""
        return User.query.get(user_id)
    
    @staticmethod
    def get_user_by_email(user_email):
        """Retorna usuario pelo email"""
        return User.query.filter_by(email=user_email).first()
    
    @staticmethod
    def create_user(username, email, cpf):
        """Cria um novo usuario"""
        if UserService.get_user_by_email(email):
            raise ValueError("Email já cadastrado!")
        
        new_user = User(username=username, email=email, cpf=cpf)

        try:
            db.session.add(new_user)
            db.session.commit()
            return new_user
        except IntegrityError as e:
            db.session.rollback()
            raise ValueError("Erro ao criar usuário: dados duplicados")
        
    @staticmethod
    def update_user(user_id, username=None, email=None, cpf=None):
        """Atualiza um usuario existente"""
        user = UserService.get_user_by_id(user_id)

        if not user:
            raise ValueError("Usuario não encontrado")
        
        if username is not None:
            user.username = username
        if email is not None:
            user.email = email
        if cpf is not None:
            user.cpf = cpf
        
        try:
            db.session.commit()
            return user
        except IntegrityError as e:
            db.session.rollback()
            raise ValueError(f"Erro ao atualizar usuário: {str(e)}")
    
    @staticmethod
    def delete_user(user_id):
        """Deleta um usuario"""
        user = UserService.get_user_by_id(user_id)
        if not user:
            raise ValueError("Usuario não encontrado")
        
        db.session.delete(user)
        db.session.commit()
        return True