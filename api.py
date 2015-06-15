import os
import importlib

from flask import Flask, json, jsonify, abort
from flask.ext.cache import Cache

from utils import CustomJSONEncoder

app = Flask(__name__, instance_relative_config=True)

app.root_dir = os.path.dirname(os.path.abspath(__file__))
app.data_dir = os.path.join(app.root_dir, 'data')

app.json_encoder = CustomJSONEncoder
app.template_folder = os.path.join(app.root_dir, 'templates')

cache = Cache(app, config={'CACHE_TYPE': 'simple'})


@app.route('/')
def index():
    data = {}
    
    with open(os.path.join(app.data_dir, 'me.json'), 'r') as f:
        data['me'] = json.loads(f.read())
    
    with open(os.path.join(app.data_dir, 'modules.json'), 'r') as f:
        settings = json.loads(f.read())
    
    modules = settings.get('modules', None)
    
    data['routes'] = []
    
    for m in modules:
        data['routes'] += ["/" + m.get('path'),]
    
    res = jsonify(data)
    res.headers['Access-Control-Allow-Origin'] = '*'
    
    return res


@app.route('/<string:filename>.txt')
def send_text_file(filename):
    return app.send_static_file(filename + '.txt')


@app.route('/<string:path>')
@cache.cached(timeout=60*60*60)
def module(path):
    with open(os.path.join(app.data_dir, 'modules.json'), 'r') as f:
        modules = json.loads(f.read())['modules']
    
    module = None
    
    for i, dic in enumerate(modules):
        if dic['path'] == path:
            module = modules[i]
    
    if not module:
        abort(404)
    
    middleware = importlib.import_module("middleware.module_" + module['type'])
    
    data = middleware.main(app, module.get('data', {}))
    
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