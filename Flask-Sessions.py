#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask import Flask, session, render_template, request, flash
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.flask_sesions
users_db = db.users

app = Flask(__name__)
app.secret_key = 'a'  # Secert Key for encrypt de cookies


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        if 'loged' in session:  # verificamos que existe la clave Loged
            if session['loged']:
                res = users_db.find_one({'email': session['email']})
                session['div'] = res['div']
                return render_template('index.html', session=session)
        else:
            return render_template('index.html')

    elif request.method == 'POST':

        if 'div' in request.form:
            res = users_db.find_one({'email': session['email']})
            if res:

                session['div'][request.form['div'].replace('#', '')] = request.form['color_div']

                users_db.update({'email': session['email']},
                                {'$set': {'div': session['div']}})

                return render_template('index.html', session=session)

        else:
            res = users_db.find_one({'email': request.form['email']})
            if res:

                if res['pass'] == request.form['pass']:
                    session['loged'] = True
                    session['user'] = res['user']
                    session['email'] = res['email']
                    session['div'] = res['div']
                    return render_template('index.html', session=session)
                else:
                    flash('Usuario no existe o password invalido!')
                    return render_template('index.html', session=session)

            else:
                flash('The user don\'t exists or worng password!!!')
                return render_template('index.html', session=session)


@app.route('/logout')
def logout():
    session.clear()
    return render_template('index.html', session=session)


@app.route('/signup', methods=['GET', 'POST'])
def singup():
    if request.method == 'GET':
        if 'loged' in session:  # verificamos que existe la clave Loged
            if session['loged']:
                return render_template('index.html', session=session)
        else:
            return render_template('signup.html')
    elif request.method == 'POST':

        res = users_db.find_one({'email': request.form['email']})
        if res is None:
            users_db.insert_one({
                'email': request.form['email'],
                'user': request.form['name'],
                'pass': request.form['pass'],
                'div': {'div1': 'yellow',
                        'div2': 'yellow',
                        'div3': 'yellow',
                        'div4': 'yellow'}})

            session['loged'] = True
            session['user'] = request.form['name']
            session['email'] = request.form['email']
            session['div'] = {'div1': 'yellow',
                              'div2': 'yellow',
                              'div3': 'yellow',
                              'div4': 'yellow'}

            return render_template('index.html', session=session)
        else:

            flash('Email ya Registrado!!!')
            return render_template('signup.html', session=session)


@app.route('/save_session', methods=['POST'])
def save_session():
    if request.method == 'POST':
        res = users_db.find_one({'email': session['email']})
        if res:
            session['div'][request.form['div'].replace('#', '')] = request.form['color_div']
            users_db.update({'email': session['email']},
                            {'$set': {'div': session['div']}})

            return 'Guardado'
        else:
            return render_template('index.html', session=session)


if __name__ == '__main__':
    app.run()
