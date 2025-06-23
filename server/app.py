from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from .config import Config
import logging
from logging.handlers import RotatingFileHandler
import os

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()

def setup_logging(app):
    if not os.path.exists('logs'):
        os.mkdir('logs')
    
    file_handler = RotatingFileHandler('logs/late_show_api.log', maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('Late Show API startup')

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    setup_logging(app)

    from .controllers.auth_controller import auth_bp
    from .controllers.guest_controller import guest_bp
    from .controllers.episode_controller import episode_bp
    from .controllers.appearance_controller import appearance_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(guest_bp)
    app.register_blueprint(episode_bp)
    app.register_blueprint(appearance_bp)

    @app.after_request
    def after_request(response):
        if response.status_code != 500:
            app.logger.info(f'Request: {request.method} {request.path} - Status: {response.status_code}')
        return response

    @app.errorhandler(500)
    def internal_error(error):
        app.logger.error(f'Server Error: {error}')
        return jsonify({'error': 'Internal server error'}), 500

    return app
