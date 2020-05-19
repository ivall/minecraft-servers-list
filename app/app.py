from flask import Flask, render_template, request, flash, jsonify
from flask_mysqldb import MySQL
from functions import update_servers
from forms import AddServerForm, AddVote
import bcrypt
import requests

app = Flask(__name__)
app.config.from_object('config')
mysql = MySQL(app)

app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True


@app.route('/')
def index():
    add_server_form = AddServerForm()
    add_vote_form = AddVote()
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM servers ORDER BY `votes` DESC, `status` DESC")
    servers = cur.fetchall()
    return render_template("index.html", servers=servers, add_server_form=add_server_form, add_vote=add_vote_form)


@app.route('/add', methods=['POST'])
def add_server():
    ip = request.form['ip']
    if ip:
        cur = mysql.connection.cursor()
        cur.execute("SELECT id FROM servers WHERE ip=%s", (ip,))
        check_server_exists = cur.fetchall()
        if not check_server_exists:
            getdata = requests.get('https://api.mcsrvstat.us/2/' + ip).json()
            status = getdata["online"]
            if status:
                version = getdata["version"]
                online_players = getdata["players"]["online"]
                max_players = getdata["players"]["max"]
                players = str(online_players) + '/' + str(max_players)
                name = getdata["motd"]["clean"]
                name = str(name)[2:][:-2].replace("', '", "")
                name = name.replace("&lt;", "<")
                name = name.replace("&gt;", ">")  # rakowy kod, w przyszłości zmienię
                name = name.replace("&amp;", "&")
                cur.execute("INSERT INTO servers (name, ip, version, players, status) VALUES(%s, %s, %s, %s, %s)",
                            (name, ip, version, players, 1))
                mysql.connection.commit()
                cur.close()
                return jsonify({"message": "Serwer został dodany"}), 200
            return jsonify({"message": "Serwer jest wyłączony"}), 400
        return jsonify({"message": "Taki serwer jest już na liście"}), 409
    return jsonify({"message": "Proszę podać IP serwera"}), 400


@app.route('/add_vote', methods=['POST'])
def add_vote():
    add_vote_form = AddVote()
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


update_servers()

if __name__ == '__main__':
    app.run()
