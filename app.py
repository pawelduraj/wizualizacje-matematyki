from flask import Flask, render_template
import base64
from io import BytesIO
from matplotlib.figure import Figure
import numpy as np

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html', content='quiz')


@app.route('/<content>')
def page(content):
    return render_template('index.html', content=content)

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

def quadratic_plots(a, b, c):
    fig = Figure()
    ax = fig.subplots()
    delta = b**2 - 4*a*c
    if delta > 0:
        x1 = (-b - delta**(0.5))/(2*a)
        x2 = (-b + delta**(0.5))/(2*a)
        x = np.linspace(x1 - 0.25*abs(x1-x2), x2 + 0.25*abs(x1-x2), 1000)
        ax.plot(x1, 0, 'ro')
        ax.plot(x2, 0, 'ro')
    else:
        x1 = -b/(2*a)
        x = np.linspace(x1 - 1, x1 + 1, 1000)
    y1 = a*x**2 + b*x + c
    ax.plot(x, y1)
    ax.plot(x, 0*x)
    fig.patch.set_facecolor('#e8eaf6')
    buf = BytesIO()
    fig.savefig(buf, format='png')
    data = base64.b64encode(buf.getbuffer()).decode('ascii')
    return f'data:image/png;base64,{data}'

if __name__ == '__main__':
    app.run()
