from flask import Flask
from .extensions import db, jwt, migrate
from dotenv import load_dotenv
import os

load_dotenv()

def create_app():
    app = Flask(__name__)

    app.config.from_mapping(
        SECRET_KEY=os.getenv('SECRET_KEY'),
        SQLALCHEMY_DATABASE_URI=os.getenv('DATABASE_URL'),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        JWT_SECRET_KEY=os.getenv('JWT_SECRET_KEY'),
    )

    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)

    from .models import User, Task

    # Blueprints
    from .auth.routes import auth_bp
    from .tasks.routes import tasks_bp
    from .admin.routes import admin_bp

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(tasks_bp, url_prefix='/tasks')
    app.register_blueprint(admin_bp, url_prefix='/admin')

    return app
