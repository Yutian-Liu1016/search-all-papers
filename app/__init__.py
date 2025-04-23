from flask import Flask
from .routes import DblpScraper, FlaskRoutes

def create_app():
    app = Flask(__name__)
    
    app.config.from_mapping(
        SECRET_KEY='your_secret_key',
    )

    scraper = DblpScraper()
    flask_routes = FlaskRoutes(scraper)
    app.register_blueprint(flask_routes.bp)


    return app