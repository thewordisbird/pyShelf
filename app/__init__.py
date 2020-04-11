from flask import current_app, Flask
from config import DevelopmentConfig, TestingConfig

def create_app(config=DevelopmentConfig):
    """Create an application instance with the desired configuration.

    Also where extentions and blueprints are registerd with the instance
    """
    # Create the application instance and load the desired configuration
    app = Flask(__name__)
    app.config.from_object(config)

    # Register Blueprints

    # Register Extensions

    # Test route
    @app.route('/hello')
    def hello():
        return 'Hello, Flask!'
    
    return app



