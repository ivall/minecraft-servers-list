import bcrypt

from flask import request, jsonify, Blueprint
from app import mysql

from app.forms import AddVoteForm

add_vote_blueprint = Blueprint('add_vote_blueprint', __name__)


@add_vote_blueprint.route('/add_vote', methods=['POST'])
def add_vote():
    add_vote_form = AddVoteForm()
    if add_vote_form.is_submitted():
        if request.form.get('recaptcha'):
            server_id = request.form['id']
            ip = request.remote_addr.encode('utf-8')
            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM votes WHERE server_id=%s", (server_id,))
            check_vote = cur.fetchall()
            if check_vote:
                for row in check_vote:
                    if bcrypt.hashpw(ip, row['user_ip'].encode('utf-8')) == row['user_ip'].encode('utf-8'):
                        return jsonify({"message": "Oddano już głos na ten serwer"}), 409
                    continue
            ip = request.remote_addr.encode('utf-8')
            hash_ip = bcrypt.hashpw(ip, bcrypt.gensalt())
            cur.execute("INSERT INTO votes (server_id, user_ip) VALUES (%s,%s)", (server_id, hash_ip))
            cur.execute("SELECT votes FROM servers WHERE id=%s",(server_id,))
            table = cur.fetchone()
            votes = table['votes']
            cur.execute("UPDATE servers SET votes=%s+1 WHERE id=%s", (votes, server_id,))
            mysql.connection.commit()
            cur.close()
            count_votes = votes + 1
            return jsonify({"message": "Oddano głos", 'votes': count_votes}), 200
        return jsonify({"message": "Wystąpił błąd podczas walidacji"}), 409
