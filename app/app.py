from flask import Flask
from flask_mysqldb import MySQL

from blueprints.add_server import add_server_blueprint
from blueprints.add_vote import add_vote_blueprint
from blueprints.index_blueprint import index_blueprint

from functions import update_servers

app = Flask(__name__)
app.config.from_object('config')
mysql = MySQL(app)

app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True


app.register_blueprint(index_blueprint)


app.register_blueprint(add_server_blueprint)


app.register_blueprint(add_vote_blueprint)


update_servers()

if __name__ == '__main__':
    app.run()
