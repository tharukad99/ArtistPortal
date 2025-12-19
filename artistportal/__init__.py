from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os

db = SQLAlchemy()

def create_app(config_object="config.Config"):
    # base project folder = parent of this file's folder
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    app = Flask(
        __name__,
        template_folder=os.path.join(base_dir, "templates"),
        static_folder=os.path.join(base_dir, "static"),
    )

    app.config.from_object(config_object)
    CORS(app)
    db.init_app(app)

    from .routes.artists import artists_bp
    from .routes.activities import activities_bp
    from .routes.metrics import metrics_bp
    from .routes.sources import sources_bp

    app.register_blueprint(artists_bp, url_prefix="/api/artists")
    app.register_blueprint(activities_bp, url_prefix="/api/activities")
    app.register_blueprint(metrics_bp, url_prefix="/api/metrics")
    app.register_blueprint(sources_bp, url_prefix="/api/sources")

    return app
