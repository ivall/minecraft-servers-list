import requests

from flask import Flask, request, jsonify, Blueprint
from flask_mysqldb import MySQL

from functions import server_data

add_server_blueprint = Blueprint('add_server_blueprint', __name__)

app = Flask(__name__)
app.config.from_object('config')
mysql = MySQL(app)


@add_server_blueprint.route('/add', methods=['POST'])
def add_server():
    server_ip = request.form['ip']
    if server_ip:
        cur = mysql.connection.cursor()
        cur.execute("SELECT id FROM servers WHERE ip=%s", (server_ip,))
        check_server_exists = cur.fetchall()
        if not check_server_exists:
            get_server_data = requests.get('https://api.mcsrvstat.us/2/' + server_ip).json()
            status = get_server_data["online"]
            if status:
                name, version, players = server_data(get_server_data)
                cur.execute("INSERT INTO servers (name, ip, version, players, status) VALUES(%s, %s, %s, %s, %s)",
                            (name, server_ip, version, players, 1))
                mysql.connection.commit()
                cur.close()
                return jsonify({"message": "Serwer został dodany"}), 200
            return jsonify({"message": "Serwer jest wyłączony"}), 400
        return jsonify({"message": "Taki serwer jest już na liście"}), 409
    return jsonify({"message": "Proszę podać IP serwera"}), 400
