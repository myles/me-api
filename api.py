import os
import importlib

import yaml

from flask import Flask, json, jsonify, abort, request

from flask.ext.cache import Cache

from utils import CustomJSONEncoder, yamlify

app = Flask(__name__, instance_relative_config=True)

app.root_dir = os.path.dirname(os.path.abspath(__file__))
app.data_dir = os.path.join(app.root_dir, 'data')

app.json_encoder = CustomJSONEncoder
app.static_url_path = os.path.join(app.root_dir, 'templates')

cache = Cache(app, config={'CACHE_TYPE': 'simple'})


@app.route('/')
@cache.cached(timeout=60 * 60 * 1)  # 1 hours
def index():
    data = {}

    with open(os.path.join(app.data_dir, 'me.json'), 'r') as f:
        data['me'] = json.loads(f.read())

    with open(os.path.join(app.data_dir, 'config.json'), 'r') as f:
        config = json.loads(f.read())

    data['routes'] = []

    for route in config.get('modules').keys():
        data['routes'] += [route, ]

    data['routes'].sort()

    if request.args.get('format') == 'yaml':
        res = yamlify(data)
    else:
        res = jsonify(data)

    res.headers['Access-Control-Allow-Origin'] = '*'

    return res


@app.route('/robots.txt')
def send_text_file():
    return app.send_static_file(request.path[1:])


@app.route('/<path:path>')
@cache.cached(timeout=60 * 60 * 2)  # 2 hours
def module(path):
    with open(os.path.join(app.data_dir, 'config.json'), 'r') as f:
        config = json.loads(f.read())

    module = config.get('modules').get("/%s" % path)

    if not module:
        abort(404)

    try:
        middleware = importlib.import_module("middleware.module_" +
                                             module.get('module'))
    except ImportError:
        abort(404)

    data = middleware.main(app, module.get('data', {}))

    if request.args.get('format') == 'yaml':
        res = yamlify(data)
    else:
        res = jsonify(data)

    res.headers['Access-Control-Allow-Origin'] = '*'

    return res


@app.errorhandler(404)
def page_not_found(error):
    res = jsonify(status=404, error='not_found')
    res.headers['Access-Control-Allow-Origin'] = '*'

    return res, 404


if __name__ == "__main__":
    app.run(debug=True)
