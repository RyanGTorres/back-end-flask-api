from app import db
from app.models.user import User
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash
from typing import Optional
from uuid import UUID
import logging


class UserService:

    @staticmethod
    def get_all_users(page=1,perpage=10):
        """Retorna todos os usuarios"""
        return User.query.paginate(
            page=page, 
            per_page=perpage, 
            error_out=False).items
    
    @staticmethod
    def get_user_by_id(user_id: UUID)-> Optional[User]:
        """Busca usuario pelo id"""
        return User.query.get(user_id)
    
    @staticmethod
    def get_user_by_email(user_email: str)-> Optional[User]:
        """Retorna usuario pelo email"""
        return User.query.filter_by(email=user_email).first()
    
    @staticmethod
    def create_user(username, password, email, cpf):
        """Cria um novo usuario"""
        if UserService.get_user_by_email(email):
            raise ValueError("Email já cadastrado!")
        
        new_user = User(
            username=username,
            password= generate_password_hash(password), 
            email=email, 
            cpf=cpf)
        try:
            db.session.add(new_user)
            db.session.commit()
            return new_user
        except IntegrityError as e:
            db.session.rollback()
            raise ValueError("Erro ao criar usuário: dados duplicados")
        
    @staticmethod
    def update_user(user_id, username=None, password=None, email=None, cpf=None):
        """Atualiza um usuario existente"""
        user = UserService.get_user_by_id(user_id)

        if not user:
            raise ValueError("Usuario não encontrado")
        
        if username is not None:
            user.username = username
        if password is not None:
            user.password = generate_password_hash(password)
        if email is not None:
            user.email = email


        try:
            db.session.commit()
            return user
        except IntegrityError as e:
            db.session.rollback()
            raise ValueError(f"Erro ao atualizar usuário",str(e))
    
    @staticmethod
    def delete_user(user_id):
        """Deleta um usuario"""
        user = UserService.get_user_by_id(user_id)
        if not user:
            raise ValueError("Usuario não encontrado")
        
        db.session.delete(user)
        db.session.commit()
        return True
    
    @staticmethod
    def verify_login_user(email, password):
        """Verifica as credenciais do usuario"""
        user = UserService.get_user_by_email(email)
        if not user or not check_password_hash(user.password, password):
            raise ValueError("Credenciais inválidas")
        return user
       