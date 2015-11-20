[![Build Status](https://travis-ci.org/myles/me-api.svg?branch=master)](https://travis-ci.org/myles/me-api) [![Build status](https://ci.appveyor.com/api/projects/status/1csgiwudvkikblh2?svg=true)](https://ci.appveyor.com/api/projects/status/1csgiwudvkikblh2/branch/master?svg=true) [![Requirements Status](https://requires.io/github/myles/me-api/requirements.svg?branch=master)](https://requires.io/github/myles/me-api/requirements/?branch=master)

# me-api

An extensible, personal API with custom integrations (a clone of [danfang](https://github.com/danfang)'s [me-api](https://github.com/danfang/me-api) written in Python).

## Development

You will need the following requirments:

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

### Workflow

I am using [git-flow](https://github.com/nvie/gitflow) to manage the development workflow. The branch `master` is current production code running on <http://api.mylesbraithwaite.com/> and the branch `develop` is current staging code running on <http://staging.api.mylesbraithwaite.com/>.

## Deploy

I am using [Heroku](https://heroku.com/) for the production and staging web sites. Travis CI handles all the deploys if they pass the tests.

### Staging

If the test past then Travis CI will deploy to the staging branch.

### Production

Use git-flow to create a new release branch:

	$ git flow release start <version>

Update the `README.md` file status images to point to the master branch and increment the version number in `api.py`.

When you are finished, finish and sigh the release branch:

	$ git flow release finish -s <version>

Then just push the master branch and Travis CI will take care of the rest:

	$ git push origin master
	$ git push --tags
