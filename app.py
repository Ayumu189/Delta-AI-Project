from flask import Flask, render_template
from chatbotapp import main

app = Flask(__name__)

@app.route("/")
def index():
    response = main("toyota")
    return render_template('index.html', response=response)

@app.route("/hello")
def hello():
    return "climate change"
