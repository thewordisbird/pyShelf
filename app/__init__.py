from flask import current_app, Flask
from config import DevelopmentConfig


def create_app(config=DevelopmentConfig):
    """Create an application instance with the desired configuration.

    Also where extentions and blueprints are registerd with the instance
    """
    # Create the application instance and load the desired configuration
    app = Flask(__name__)
    app.config.from_object(config)

    # Register Blueprints
    from app.books.routes import bp as books_bp
    from app.auth.routes import bp as auth_bp

    app.register_blueprint(books_bp)
    app.register_blueprint(auth_bp)
    # Register Extensions

    # Test route
    @app.route('/hello')
    def hello():
        return 'Hello, Flask!'
    
    return app
        



