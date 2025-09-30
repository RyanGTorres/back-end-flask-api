from flask import Flask
from os import environ
from dotenv import load_dotenv
from app import db
from app.controller.user_controller import user_bp

def create_app():
    load_dotenv()
    
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DB_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    
    app.register_blueprint(user_bp)
    
    with app.app_context():
        db.create_all()

    
    return app  


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)