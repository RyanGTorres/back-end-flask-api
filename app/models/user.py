
from app import db
from sqlalchemy.dialects.postgresql import UUID
import uuid

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    cpf = db.Column(db.String(20), unique=True, nullable=False)

    def to_json(self):
        return{
            'id':str(self.id), 
            'username':self.username,
            'email':self.email, 
            'cpf':self.cpf
            }
    
    def __repr__(self):
        return f'<User {self.username}>'
    
