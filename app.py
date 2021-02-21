from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask_mysqldb import MySQL, MySQLdb
from wtforms import SelectField
from flask_wtf import FlaskForm
import mysql.connector
from flask_mysqldb import MySQL
import MySQLdb.cursors




app= Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/office'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'office'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)

db = SQLAlchemy(app)
app.secret_key = "Hello"







@app.route("/", methods = ['GET', 'POST'])
def register():
    if (request.method == 'POST'):
        '''Add entry to the database'''
        name = request.form.get('name')
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        entry = Register(name=name, username=username, password=password, email=email)
        db.session.add(entry)
        db.session.commit()
    return render_template('Register.html')


@app.route("/login", methods = ['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM register WHERE username = %s AND password = %s', (username, password))
        user = cursor.fetchone()
        if user:
            session['log_in'] = True
            session['username'] = user['username']
            msg = 'Logged in successfully !'
            return render_template('roomf.html', msg=msg)

        else:
            msg = 'Incorrect username / password !'
    return render_template('Login.html', msg=msg)



class Room(db.Model):

    room= db.Column(db.String(15), primary_key=True)
    total_capacity= db.Column(db.String(20))
    working_place = db.Column(db.Integer)

class Form(FlaskForm):
    room = SelectField('room', choices=[])

@app.route('/', methods=['GET', 'POST'])
def room():
    form = Form()
    form.room.choices = [room for room in room.query.all()]

    if request.method == 'POST':
        room = Room.query.filter_by(id=form.room.data).first()

    return render_template('roomf.html', form=form)


@app.route('/logout')
def logout():
    session.pop('log_in', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('login'))


app.run(debug=True)