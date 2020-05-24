from flask import Flask, Blueprint, render_template
from flask_mysqldb import MySQL

from forms import AddServerForm, AddVoteForm

index_blueprint = Blueprint('index_blueprint', __name__)

app = Flask(__name__)
app.config.from_object('config')
mysql = MySQL(app)


@index_blueprint.route('/')
def index():
    add_server_form = AddServerForm()
    add_vote_form = AddVoteForm()
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM servers ORDER BY `votes` DESC, `status` DESC")
    servers = cur.fetchall()
    return render_template("index.html", servers=servers, add_server_form=add_server_form, add_vote=add_vote_form)
