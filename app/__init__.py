from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import config_by_name

db = SQLAlchemy()

def create_app(config_name='development'):
    """Application factory"""
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])
    
    # Initialize database
    db.init_app(app)
    
    # Register blueprints
    from app.routes import main_bp, students_bp, courses_bp, grades_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(students_bp, url_prefix='/students')
    app.register_blueprint(courses_bp, url_prefix='/courses')
    app.register_blueprint(grades_bp, url_prefix='/grades')
    
    # Register error handlers
    @app.errorhandler(404)
    def not_found_error(error):
        from flask import render_template
        return render_template('errors/404.html'), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        from flask import render_template
        db.session.rollback()
        return render_template('errors/500.html'), 500
    
    return app
