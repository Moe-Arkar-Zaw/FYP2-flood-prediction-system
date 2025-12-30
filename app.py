from flask import Flask, render_template, redirect, url_for, session
from config import Config 
from backend.database import db
from backend.models import * # loads all ORM models
from backend.auth.auth_service import bcrypt

from flask_migrate import Migrate

# Import blueprints
from backend.routes.admin_routes import admin_bp 
from backend.routes.user_routes import user_bp
from backend.routes.api_routes import api_bp
from backend.auth.auth_routes import auth_bp
from backend.user_profile.profile_routes import profile_bp

migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    migrate.init_app(app, db)

    # Resgister blueprints
    app.register_blueprint(admin_bp, url_prefix="/admin")
    app.register_blueprint(user_bp, url_prefix="/user")
    app.register_blueprint(api_bp, url_prefix="/api")
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(profile_bp, url_prefix="/user-profile")

    @app.route("/")
    def home():
        return redirect(url_for('public_dashboard'))
    
    @app.route("/public_dashboard")
    def public_dashboard():
        return render_template("user/dashboard.html")
    
    @app.context_processor
    def inject_user():
        if "user_id" in session:
         user = User.query.get(session["user_id"])
         return dict(current_user=user)
        return dict(current_user=None)
    
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)

