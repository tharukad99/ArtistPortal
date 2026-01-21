# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
# from flask_cors import CORS
# import os

# db = SQLAlchemy()

# def create_app(config_object="config.Config"):
#     # base project folder = parent of this file's folder
#     base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

#     app = Flask(
#         __name__,
#         template_folder=os.path.join(base_dir, "templates"),
#         static_folder=os.path.join(base_dir, "static"),
#     )

#     app.config.from_object(config_object)
#     CORS(app)
#     db.init_app(app)

#     from .routes.artists import artists_bp
#     from .routes.activities import activities_bp
#     from .routes.metrics import metrics_bp
#     from .routes.sources import sources_bp

#     app.register_blueprint(artists_bp, url_prefix="/api/artists")
#     app.register_blueprint(activities_bp, url_prefix="/api/activities")
#     app.register_blueprint(metrics_bp, url_prefix="/api/metrics")
#     app.register_blueprint(sources_bp, url_prefix="/api/sources")

#     return app



# artistportal/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_login import LoginManager
import os

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = "auth.login"  # endpoint name: auth.login
login_manager.login_message = "Please log in as admin to access this page."

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
    login_manager.init_app(app)

    # Import models so Flask-Login can load User
    from .models import User  # noqa: F401

    @login_manager.user_loader
    def load_user(user_id: str):
        return User.query.get(int(user_id))

    # ---- Register API blueprints (your existing ones) ----
    from .routes.artists import artists_bp
    from .routes.activities import activities_bp
    from .routes.metrics import metrics_bp
    from .routes.sources import sources_bp

    app.register_blueprint(artists_bp, url_prefix="/api/artists")
    app.register_blueprint(activities_bp, url_prefix="/api/activities")
    app.register_blueprint(metrics_bp, url_prefix="/api/metrics")
    app.register_blueprint(sources_bp, url_prefix="/api/sources")

    # ---- Register Auth blueprint (NEW) ----
    from .routes.auth import auth_bp
    app.register_blueprint(auth_bp)

    # Create tables (simple dev approach)
    # In production, use migrations (Flask-Migrate/Alembic).
    with app.app_context():
        db.create_all()

    return app
