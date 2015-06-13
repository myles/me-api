import os
import importlib

from flask import Flask, json, jsonify, abort

from utils import CustomJSONEncoder

app = Flask(__name__, instance_relative_config=True)
app.json_encoder = CustomJSONEncoder

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
APP_DATA = os.path.join(APP_ROOT, 'data')

@app.route('/')
def index():
    data = {}
    
    with open(os.path.join(APP_DATA, 'me.json'), 'r') as f:
        data['me'] = json.loads(f.read())
    
    with open(os.path.join(APP_DATA, 'modules.json'), 'r') as f:
        settings = json.loads(f.read())
    
    modules = settings.get('modules', None)
    
    data['routes'] = []
    
    for m in modules:
        data['routes'] += ["/" + m.get('path'),]
    
    res = jsonify(data)
    res.headers['Access-Control-Allow-Origin'] = '*'
    
    return res


@app.route('/<path>')
def module(path):
    with open(os.path.join(APP_DATA, 'modules.json'), 'r') as f:
        modules = json.loads(f.read())['modules']
    
    for i, dic in enumerate(modules):
        if dic['path'] == path:
            module = modules[i]
    
    if not module:
        abort(404)
    
    middleware = importlib.import_module("middleware." + module['type'])
    
    data = middleware.main(app, module.get('data', {}))
    
    res = jsonify(data)
    res.headers['Access-Control-Allow-Origin'] = '*'
    
    return res


@app.route('/<file_name>.txt')
def send_text_file(file_name):
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.errorhandler(404)
def page_not_found(error):
    res = jsonify(status=404, error='not_found')
    res.headers['Access-Control-Allow-Origin'] = '*'
    
    return res, 404


if __name__ == "__main__":
    app.run(debug=True)