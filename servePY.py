"""
Serves the website using flask
for local dev. In production, use
Nginx.
"""
import os

from flask import Flask

app = Flask(__name__, static_url_path='/', static_folder='serve')

@app.route('/')
def index():
  return app.send_static_file('index.html')

# Handle 404
@app.errorhandler(404)
def page_not_found(e):
  return app.send_static_file('404.html'), 404