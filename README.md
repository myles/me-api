[![Build Status](https://travis-ci.org/myles/me-api.svg?branch=master)](https://travis-ci.org/myles/me-api)

# me-api

An extensible, personal API with custom integrations (a clone of [danfang](https://github.com/danfang)'s [me-api](https://github.com/danfang/me-api) written in Python).

## Development

You will need the following:

* Python 2.7.10+
* [pip](https://pip.pypa.io/en/stable/)
* [virtualenvwrapper](https://virtualenvwrapper.readthedocs.org/en/latest/)

Create a python virtual envourment:

	$ mkvirtualenv com_mylesbraithwaite_api
	(com_mylesbraithwaite_api) $

Install the python requirments:

	(com_mylesbraithwaite_api) $ pip install --upgrade -r requirements.txt

Run the project:

	(com_mylesbraithwaite_api) $ python api.py