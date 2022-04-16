from flask import Flask, render_template, request
from waitress import serve
import pandas
app = Flask('app')

@app.route('/', methods = ['POST', 'GET'])
def index():
  return render_template("index.html")

@app.route('/generate', methods = ['POST', 'GET'])
def generate():
  if request.method == 'POST':
    return request.form
  
app.run(host='0.0.0.0', port=8080, debug=True)