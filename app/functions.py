import threading
import mysql.connector
import requests

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="",
  db="servers"
)
cur = mydb.cursor(buffered=True)


def update_servers():
    threading.Timer(150.0, update_servers).start()
    cur.execute("SELECT id, ip, status FROM servers")
    servers = cur.fetchall()
    for server in servers:
        getdata = requests.get('https://api.mcsrvstat.us/2/'+server[1]).json()
        status = getdata["online"]
        if status:
            online_players = getdata["players"]["online"]
            max_players = getdata["players"]["max"]
            players = str(online_players) + '/' + str(max_players)
            version = getdata["version"]
            name = getdata["motd"]["clean"]
            name = str(name)[2:][:-2].replace("', '", "")
            name = name.replace("&lt;", "<")
            name = name.replace("&gt;", ">")  # rakowy kod, w przyszłości zmienię
            name = name.replace("&amp;", "&")
            cur.execute("UPDATE servers SET name=%s, version=%s, players=%s, status=%s WHERE id=%s", (name, version, players, status, server[0],))
        elif not status:
            if server[2] == '1':
                cur.execute("UPDATE servers SET status=%s WHERE id=%s",('0',server[0],))
    mydb.commit()
