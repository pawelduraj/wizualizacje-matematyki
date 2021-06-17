from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html', content='quiz')


@app.route('/<content>')
def page(content):
    return render_template('index.html', content=content)


if __name__ == '__main__':
    app.run()
