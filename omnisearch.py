from flask import Flask, render_template, request, jsonify
import json
from omnicore import dosearch, enhancedsearch, moduleobject, getchunk

print("[omnisearch] Creating listings for modules...")
options_searchers = []
options_filters = []
options_sorters = []
searchers =  moduleobject["searchers"]
filters = moduleobject["filters"]
sorters = moduleobject["sorters"]
for module in searchers:
    options_searchers.append({"id": module["id"], "name": module["name"]})
for module in filters:
    options_filters.append({"id": module["id"], "name": module["name"]})
for module in sorters:
    options_sorters.append({"id": module["id"], "name": module["name"]})

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html", options_searchers=options_searchers, options_filters=options_filters, options_sorters=options_sorters, options_json=json.dumps({"searchers": options_searchers, "filters": options_filters, "sorters": options_sorters}))

@app.route('/search')
def search():
    return render_template("search.html")

@app.route('/api/search')
def api_search():
    return jsonify(dosearch(request.args.get("query"), request.args.get("config")))

@app.route('/api/enhanced_search')
def api_enhanced_search():
    return jsonify(enhancedsearch(request.args.get("query"), request.args.get("config")))

@app.route('/api/get_chunk/<chunk>')
def get_chunk(chunk):
    return jsonify(getchunk(chunk))

if __name__ == "__main__":
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(port=8000, host="0.0.0.0")