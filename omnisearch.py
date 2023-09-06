from flask import Flask, render_template, request, jsonify
import json
from omnicore import dosearch

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/search')
def search():
    return render_template("search.html")

@app.route('/api/search')
def api_search():
    return jsonify(dosearch(request.args.get("query"), request.args.get("config")))

if __name__ == "__main__":
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(port=8000, host="0.0.0.0")