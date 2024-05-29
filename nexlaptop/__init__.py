from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///nexlaptop.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'secret_key'

    db.init_app(app)

    from .main import main_bp
    from .filters import filters_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(filters_bp)

    with app.app_context():
        db.create_all() 

    return app
