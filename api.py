#!/usr/bin/python

import os
import importlib

from flask import Flask, json, jsonify, abort, request

from flask.ext.cache import Cache
from flask_ripozo import FlaskDispatcher

from ripozo import apimethod, ResourceBase

from utils import CustomJSONEncoder, JSONRipozoAdapter

app = Flask(__name__, instance_relative_config=True)

dispatcher = FlaskDispatcher(app, url_prefix='/v1')
dispatcher.register_adapters(JSONRipozoAdapter)

app.root_dir = os.path.dirname(os.path.abspath(__file__))
app.data_dir = os.path.join(app.root_dir, 'data')

app.json_encoder = CustomJSONEncoder
app.static_url_path = os.path.join(app.root_dir, 'templates')

cache = Cache(app, config={'CACHE_TYPE': 'simple'})


class IndexViewSet(ResourceBase):
    resource_name = ''

    @apimethod(methods=['GET'])
    def index(cls, request, *args, **kwargs):
        data = {}

        with open(os.path.join(app.data_dir, 'me.json'), 'r') as f:
            data['me'] = json.loads(f.read())

        with open(os.path.join(app.data_dir, 'config.json'), 'r') as f:
            config = json.loads(f.read())

        data['routes'] = []

        for route in config.get('modules').keys():
            data['routes'] += [dispatcher.url_prefix + route, ]

        data['routes'].sort()

        return cls(properties=data)


class ModuleViewSet(ResourceBase):
    resource_name = ''
    pks = ('module_name',)

    @apimethod(methods=['GET'])
    def view(cls, request, *args, **kwargs):
        with open(os.path.join(app.data_dir, 'config.json'), 'r') as f:
            config = json.loads(f.read())

        module_name = request.get('module_name')

        module_config = config.get('modules').get("/" + module_name)

        try:
            middleware = importlib.import_module("middleware.module_" +
                                                 module_config.get('module'))
        except ImportError:
            abort(404)

        data = middleware.main(app, module_config.get('data', {}))

        return cls(properties=data)


@app.route('/robots.txt')
def send_text_file():
    return app.send_static_file(request.path[1:])


@app.errorhandler(404)
def page_not_found(error):
    res = jsonify(status=404, error='not_found')
    res.headers['Access-Control-Allow-Origin'] = '*'

    return res, 404

dispatcher.register_resources(IndexViewSet, ModuleViewSet)

if __name__ == "__main__":
    app.run(debug=True)
