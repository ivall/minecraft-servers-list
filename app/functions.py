import threading
import mysql.connector
import requests
import html

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="",
  db="servers"
)
cur = mydb.cursor(buffered=True)


def server_data(get_server_data):
    online_players = get_server_data["players"]["online"]
    max_players = get_server_data["players"]["max"]
    players = str(online_players) + '/' + str(max_players)
    version = get_server_data["version"]
    name = get_server_data["motd"]["clean"]
    name = str(name)[2:][:-2].replace("', '", "")
    name = html.unescape(name)
    return name, version, players


def update_servers():
    threading.Timer(150.0, update_servers).start()
    cur.execute("SELECT id, ip, status FROM servers")
    servers = cur.fetchall()
    for server in servers:
        get_server_data = requests.get('https://api.mcsrvstat.us/2/'+server[1]).json()
        status = get_server_data["online"]
        if status:
            name, version, players = server_data(get_server_data)
            cur.execute("UPDATE servers SET name=%s, version=%s, players=%s, status=%s WHERE id=%s", (name, version, players, status, server[0],))
        elif not status:
            if server[2] == '1':
                cur.execute("UPDATE servers SET status=%s WHERE id=%s",('0',server[0],))
    mydb.commit()
