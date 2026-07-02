import sqlite3   # base de datos para usuarios/contraseñas
import hashlib   # hashes seguros y message digests
from flask import Flask, request

app = Flask(__name__)

db_name = 'usuarios.db'


@app.route('/')
def index():
    return 'Sitio DRY7122 - Gestion de usuarios con contraseñas en hash'


######################################### Registro con Hash #########################################################
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS USER_HASH
                (USERNAME  TEXT    PRIMARY KEY NOT NULL,
                HASH      TEXT    NOT NULL);''')
    conn.commit()
    try:
        hash_value = hashlib.sha256(request.form['password'].encode()).hexdigest()
        c.execute("INSERT INTO USER_HASH (USERNAME, HASH) "
                  "VALUES ('{0}', '{1}')".format(request.form['username'], hash_value))
        conn.commit()
    except sqlite3.IntegrityError:
        return "username has been registered."

    print('username: ', request.form['username'], ' password: ', request.form['password'], ' hash: ', hash_value)
    return "signup success"


def verify_hash(username, password):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    query = "SELECT HASH FROM USER_HASH WHERE USERNAME = '{0}'".format(username)
    c.execute(query)
    records = c.fetchone()
    conn.close()
    if not records:
        return False
    return records[0] == hashlib.sha256(password.encode()).hexdigest()


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if verify_hash(request.form['username'], request.form['password']):
            error = 'login success'
        else:
            error = 'Invalid username/password'
    else:
        error = 'Invalid Method'
    return error


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5800, ssl_context='adhoc')