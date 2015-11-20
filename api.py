#!/usr/bin/python

import os
from importlib import import_module

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


def get_json_file(filename):
    with open(os.path.join(app.data_dir, filename), 'r') as f:
        return json.loads(f.read())


class IndexViewSet(ResourceBase):
    resource_name = ''

    @apimethod(methods=['GET'])
    def index(cls, request, *args, **kwargs):
        data = {}

        data['me'] = get_json_file('me.json')

        config = get_json_file('config.json')

        data['routes'] = []

        for route in config.get('modules').keys():
            data['routes'] += ["%s/%s/" % (dispatcher.url_prefix, route)]

        data['routes'].sort()

        return cls(properties=data)


class ModuleViewSet(ResourceBase):
    resource_name = ''
    pks = ('module_name',)

    @apimethod(methods=['GET'])
    def view(cls, request, *args, **kwargs):
        config = get_json_file('config.json')

        module_name = request.get('module_name')

        try:
            middleware = import_module("middleware.module_" +
                                       module_config.get('module'))
        except ImportError:
            abort(404)

        data = middleware.main(app, module_config.get('data', {}))

        return cls(properties=data)


class SubModuleViewSet(ResourceBase):
    resource_name = ''
    pks = ('module_name', 'sub_module_name')

    @apimethod(methods=['GET'])
    def view(cls, request, *args, **kwargs):
        config = get_json_file('config.json')

        module_name = request.get('module_name')
        sub_module_name = request.get('sub_module_name')

        module_config = config.get('modules').get(module_name)
        module_children = module_config.get('children')

        sub_module_confg = module_children.get(sub_module_name)

        try:
            middleware = import_module("middleware.module_" +
                                       sub_module_confg.get('module'))
        except ImportError:
            abort(404)

        data = middleware.main(app, module_config.get('data', {}))

        return cls(properties=data)


@app.route('/robots.txt')
def send_text_file():
    return app.send_static_file(request.path[1:])


@app.errorhandler(404)
def page_not_found(error):
    print type(error)
    res = jsonify(status=404, error=error.description)
    res.headers['Access-Control-Allow-Origin'] = '*'

    return res, 404


dispatcher.register_resources(IndexViewSet, ModuleViewSet, SubModuleViewSet)


if __name__ == "__main__":
    app.run(debug=True)
