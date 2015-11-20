from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import time
import datetime

import six

try:
    from urlparse import urlparse, urlunparse
except ImportError:
    from urllib.parse import urlparse, urlunparse

from flask import json
from flask.json import JSONEncoder
from flask.globals import current_app, request

from ripozo.adapters import AdapterBase

from instagram import models as instagram_models


class CustomJSONEncoder(JSONEncoder):

    def default(self, obj):

        if isinstance(obj, time.struct_time):
            return datetime.datetime.fromtimestamp(time.mktime(obj))

        if isinstance(obj, datetime.date):
            return obj.isoformat()

        if isinstance(obj, datetime.datetime):
            return obj.isoformat()

        if isinstance(obj, datetime.time):
            return obj.isoformat()

        if isinstance(obj, instagram_models.ApiModel):
            return obj.__dict__

        return JSONEncoder.default(self, obj)


def remove_utm(url):
    parsed_url = list(urlparse(url))
    parsed_url[4] = '&'.join(
        [x for x in parsed_url[4].split('&') if not x.startswith('utm_')]
    )
    utmless_url = urlunparse(parsed_url)

    return utmless_url


class JSONRipozoAdapter(AdapterBase):
    """
    Just a plain old JSON dump of the properties.
    Nothing exciting.

    Format:

    .. code-block:: javascript

        <resource_name>: {
            field1: "value"
            field2: "value"
            relationship: {
                relationship_field: "value"
            }
            list_relationship: [
                {
                    relationship_field: "value"
                }
                {
                    relationship_field: "value"
                }
            ]
        }
    """
    _CONTENT_TYPE = 'application/json'
    formats = ['json', _CONTENT_TYPE]
    extra_headers = {'Content-Type': _CONTENT_TYPE}

    @property
    def formatted_body(self):
        """
        :return: The formatted body that should be returned.
            It's just a ``json.dumps`` of the properties and
            relationships
        :rtype: unicode
        """
        response = dict()
        parent_properties = self.resource.properties.copy()
        self._append_relationships_to_list(response,
                                           self.resource.related_resources)
        self._append_relationships_to_list(response,
                                           self.resource.linked_resources)
        response.update(parent_properties)
        return json.dumps({self.resource.resource_name: response})

    @staticmethod
    def _append_relationships_to_list(rel_dict, relationships):
        """
        Dumps the relationship resources provided into
        a json ready list of dictionaries.  Side effect
        of updating the dictionary with the relationships

        :param dict rel_dict:
        :param list relationships:
        :return: A list of the resources in dictionary format.
        :rtype: list
        """
        for resource, name, embedded in relationships:
            if name not in rel_dict:
                rel_dict[name] = []
            if isinstance(resource, (list, tuple)):
                for res in resource:
                    rel_dict[name].append(res.properties)
                continue
            rel_dict[name].append(resource.properties)

    @classmethod
    def format_exception(cls, exc):
        """
        Takes an exception and appropriately formats
        the response.  By default it just returns a json dump
        of the status code and the exception message.
        Any exception that does not have a status_code attribute
        will have a status_code of 500.

        :param Exception exc: The exception to format.
        :return: A tuple containing: response body, format,
            http response code
        :rtype: tuple
        """
        status_code = getattr(exc, 'status_code', 500)
        body = json.dumps(dict(status=status_code, message=six.text_type(exc)))
        return body, cls.formats[0], status_code

    @classmethod
    def format_request(cls, request):
        """
        Simply returns request

        :param RequestContainer request: The request to handler
        :rtype: RequestContainer
        """
        return request
