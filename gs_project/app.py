from flask import Flask, render_template
from flask_bootstrap import Bootstrap

from services.main import main

app = Flask(__name__)
Bootstrap(app)

@app.route('/')
def index():
    message = main()
    return render_template('index.html', message=message)
