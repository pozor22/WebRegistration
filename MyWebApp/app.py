import requests
from flask import Flask, render_template, request, redirect
import psycopg2

app = Flask(__name__)
conn = psycopg2.connect(database='service_db', user='postgres', password='1234', host='127.0.0.1', port='5432')

cursor = conn.cursor()

@app.route('/login/', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        if request.form.get('login'):
            username = request.form.get('username')
            password = request.form.get('password')
            cursor.execute("SELECT * FROM service.users WHERE login=%s AND password=%s", (str(username), str(password)))
            records = list(cursor.fetchall())
            if len(records) == 0:
                return render_template('login.html')
            else:
                return render_template('account.html', full_name=records[0][1], login=records[0][2], password=records[0][3])
        elif request.form.get('registration'):
            return redirect('/registration/')
    return render_template('login.html')

@app.route('/registration/', methods=['POST', 'GET'])
def registration():
    if request.method == 'POST':
        name = request.form.get('name')
        login = request.form.get('login')
        password = request.form.get('password')
        if (len(str(name)) != 0 and len(str(login)) != 0 and len(str(password)) != 0) and (str(name).count(" ") <= 1 and str(login).count(" ") == 0 and str(password).count(" ") == 0):
            cursor.execute("SELECT * FROM service.users WHERE login=%s AND password=%s", (str(login), str(password)))
            record = list(cursor.fetchall())
            if len(record) == 0:
                cursor.execute('INSERT INTO service.users(full_name, login, password) VALUES(%s, %s, %s);', (str(name), str(login), str(password)))
                conn.commit()
                return redirect('/login/')
            else:
                return render_template('registration.html')
        else:
            return render_template('registration.html')
    return render_template('registration.html')