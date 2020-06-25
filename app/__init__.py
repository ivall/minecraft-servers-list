from flask import Flask
from flask_mysqldb import MySQL

mysql = MySQL()


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')

    mysql.init_app(app)

    app.jinja_env.trim_blocks = True
    app.jinja_env.lstrip_blocks = True

    from app.blueprints.add_server import add_server_blueprint
    from app.blueprints.add_vote import add_vote_blueprint
    from app.blueprints.index_blueprint import index_blueprint

    app.register_blueprint(index_blueprint)
    app.register_blueprint(add_server_blueprint)
    app.register_blueprint(add_vote_blueprint)

    from app.functions import update_servers
    update_servers()

    return app
