from flask import Flask
from flask_login import LoginManager
from models import db
from config import config
from routes.main_routes import main_routes
from routes.user_routes import user_routes
import secrets



#Creating the application through a factory function wlil allow us to create multiple instances of the appnlication  
def create_app():
    app = Flask(__name__)
    # Configuración de la clave secreta
    app.secret_key = secrets.token_hex(32)
    # Configuración adicional desde el objeto config    
    app.config.from_object(config['development'])
    
    # Db configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{app.root_path}/database.db"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    
    # Loging Manager configuration
    login_manager = LoginManager()
    login_manager.login_view = 'main.login'
    login_manager.init_app(app)

    # Import the User class    
    from models import User
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    # Bind the app with db
    db.init_app(app)
    
    with app.app_context():
        db.create_all()
        # Create the initial admin user
        from initial_data import create_admin
        create_admin()
    app.register_blueprint(main_routes)
    app.register_blueprint(user_routes)
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)


    

    