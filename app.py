from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html', content='Quiz')


@app.route('/zagadnienie')
def problem():
    return render_template('index.html', content='Wybrane zagadnienie matematyczne')


@app.route('/about')
def about():
    return render_template('index.html', content='O nas...')


if __name__ == '__main__':
    app.run()
