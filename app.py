from os import name
from flask import Flask, render_template, session, request, redirect, url_for, flash, json
import base64
from io import BytesIO
from matplotlib.figure import Figure
import numpy as np
import db_manager
import os

app = Flask(__name__)


try:
    db = db_manager.DataBase()
    question_list = db.get_questions()
    # for question in question_list:
    #     print(question)
except Exception as e:
    print(e)
    # print("Brak DATABASE_URL")
    db = None

app.secret_key = 'key'


@app.route('/')
def quiz():
    session['points'] = 0
    return render_template('quiz.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/problems')
def problems():
    return render_template('problems.html')

@app.route('/quadratics')
def topic1():
    plot1 = quadratic_plots(3, 2, -5)
    plot2 = quadratic_plots(3, 4, 2)
    return render_template('quadratics.html', plot1=plot1, plot2 = plot2)

@app.route('/logarithms')
def topic2():
    return render_template('logarithms.html')

@app.route('/sequences')
def topic3():
    return render_template('sequences.html')


@app.route('/users')
def users():
    list_users = db.select_users_points()
    print(list_users)
    return render_template('users.html', list_users=list_users)

@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form['name']
        password = request.form['password']
        email = request.form['email']
        base_response = db.is_user_in_base(name)
        if base_response == "name not string":
            flash("Błędna nazwa użytkownika")
            return render_template("register.html")
        elif not base_response is None:
            flash("Użytkownik już istnieje")
            return render_template("register.html")
        base_email_response = db.is_email_in_base(email)
        if not base_email_response is None:
            flash("Podany email już został zarejestrowany")
            return render_template("register.html")
        insert_response = db.insert_new_user(name=name, password=password, email=email)
        if insert_response == "email not string" or insert_response == "email not valid":
            flash("Błędny adres email")
        if insert_response == "password not string":
            flash("Błędne hasło")
        if insert_response == "User created":
            flash("Użytkownik poprawnie zarejestrowany")
            return redirect(url_for("login"))
        if not insert_response:
            flash("Nie udało się utworzyć użytkownika")
    return render_template("register.html")
        
@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        name = request.form['name']
        password = request.form['password']
        base_response = db.login_user(name, password)
        if base_response:
            flash("Poprawne dane użytkownika")
            session['user'] = name
            session['max_points'] = db.get_points(name)
            return redirect(url_for('quiz'))
        else:
            flash("Błędne hasło lub login")
    return render_template("login.html")

@app.route('/logout')
def logout():
    session.pop('user', None)
    session.pop('max_points', None)
    flash("Użytkownik został wylogowany")
    return redirect(url_for('quiz'))

@app.route('/quiz', methods=['POST'])
def validate_quiz():
    zad = int(request.form['zad'])
    correct = True if request.form['correct']=='true' else False
    print(session['user'] if 'user' in session else '', zad, 'correct' if correct else 'incorrect')
    if correct:
        session['points'] += 1
        if 'user' in session:
            if session['points'] > session['max_points']:
                session['max_points'] = session['points']
                db.set_points(session['user'], session['points'])
    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


def quadratic_plots(a, b, c):
    fig = Figure()
    ax = fig.subplots()
    delta = b**2 - 4*a*c
    if delta > 0:
        x1 = (-b - delta**0.5)/(2*a)
        x2 = (-b + delta**0.5)/(2*a)
        x = np.linspace(x1 - 0.25*abs(x1-x2), x2 + 0.25*abs(x1-x2), 1000)
        ax.plot(x1, 0, 'ro')
        ax.plot(x2, 0, 'ro')
    else:
        x1 = -b/(2*a)
        x = np.linspace(x1 - 1, x1 + 1, 1000)
    y1 = a*x**2 + b*x + c
    ax.plot(x, y1)
    ax.plot(x, 0*x)
    buf = BytesIO()
    fig.savefig(buf, format='png')
    data = base64.b64encode(buf.getbuffer()).decode('ascii')
    return f'data:image/png;base64,{data}'

@app.errorhandler(404)
def not_found(error):
    print(error)
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run()
