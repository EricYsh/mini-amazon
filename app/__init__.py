from flask import Flask
from flask_login import LoginManager
from .config import Config
from .db import DB


login = LoginManager()
login.login_view = 'users.login'


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    app.db = DB(app)
    login.init_app(app)

    from .index import bp as index_bp
    app.register_blueprint(index_bp)

    from .users import bp as user_bp
    app.register_blueprint(user_bp)

    from .wishlist import bp as wishlist_bp
    app.register_blueprint(wishlist_bp)

    from .cart import bp as cart_bp
    app.register_blueprint(cart_bp)

    from .usercomment import bp as usercomment_bp
    app.register_blueprint(usercomment_bp)

    from .purchases import bp as purchases_bp
    app.register_blueprint(purchases_bp)

    from .inventory import bp as inventory_bp
    app.register_blueprint(inventory_bp)
    
    from .product import bp as product_bp
    app.register_blueprint(product_bp)

    from .clientorder import bp as clientorder_bp
    app.register_blueprint(clientorder_bp)

    from .profiles import bp as profiles_bp
    app.register_blueprint(profiles_bp)

    from .trend import bp as trend_bp
    app.register_blueprint(trend_bp)

    from .userorder import bp as userorder_bp
    app.register_blueprint(userorder_bp)

    return app
