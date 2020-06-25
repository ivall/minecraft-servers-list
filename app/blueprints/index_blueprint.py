from flask import Blueprint, render_template
from app import mysql

from app.forms import AddServerForm, AddVoteForm

index_blueprint = Blueprint('index_blueprint', __name__)


@index_blueprint.route('/')
def index():
    add_server_form = AddServerForm()
    add_vote_form = AddVoteForm()
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM servers ORDER BY `votes` DESC, `status` DESC")
    servers = cur.fetchall()
    return render_template("index.html", servers=servers, add_server_form=add_server_form, add_vote=add_vote_form)
