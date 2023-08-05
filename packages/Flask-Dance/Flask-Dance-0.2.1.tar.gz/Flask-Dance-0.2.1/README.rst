Flask-Dance |build-status| |coverage-status| |pypi| |docs|
==========================================================
Doing the OAuth dance with style using Flask, requests, and oauthlib. Currently,
only OAuth consumers are supported, but this project could easily support
OAuth providers in the future, as well. The `full documentation for this project
is hosted on ReadTheDocs <http://flask-dance.readthedocs.org/>`_, but this
README will give you a taste of the features.

Installation
============

Just the basics::

.. code-block:: bash

    $ pip install Flask-Dance

Or if you're planning on using the built-in `SQLAlchemy`_ support::

.. code-block:: bash

    $ pip install Flask-Dance[models]

Quickstart
==========
For `a few popular OAuth providers`_, Flask-Dance provides pre-set configurations. For
example, to authenticate with Github, just do the following:

.. code-block:: python

    from flask import Flask, redirect, url_for
    from flask_dance.contrib.github import make_github_blueprint, github

    app = Flask(__name__)
    blueprint = make_github_blueprint(
        client_id="my-key-here",
        client_secret="my-secret-here",
        redirect_to="index",
    )
    app.register_blueprint(blueprint, url_prefix="/login")

    @app.route("/")
    def index():
        if not github.authorized:
            return redirect(url_for("github.login"))
        resp = github.get("/user")
        assert resp.ok
        return "You are @{login} on Github".format(login=resp.json()["login"])

The ``github`` object is a `context local`_, just like ``flask.request``. That means
that you can import it in any Python file you want, and use it in the context
of an incoming HTTP request. If you've split your Flask app up into multiple
different files, feel free to import this object in any of your files, and use
it just like you would use the ``requests`` module.

You can also use Flask-Dance with any OAuth provider you'd like, not just the
pre-set configurations. `See the documentation for how to use other OAuth
providers. <http://flask-dance.readthedocs.org/en/latest/consumers.html>`_

.. _a few popular OAuth providers: http://flask-dance.readthedocs.org/en/latest/contrib.html
.. _context local: http://flask.pocoo.org/docs/latest/quickstart/#context-locals

Token Storage
=============
By default, OAuth access tokens are stored in Flask's session object. This means
that if the user ever clears their browser cookies, they will have to go through
the OAuth flow again, which is not good. You're better off storing access tokens
in a database or some other persistent store. If you're using `SQLAlchemy`_,
it's easy: just pass your database model and session to the blueprint.
Flask-Dance even comes with a mixin to help you define your database model,
and it works with User models, too!

.. code-block:: python

    from flask_sqlalchemy import SQLAlchemy
    from flask_dance.models import OAuthMixin

    db = SQLAlchemy()

    class User(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        # ... other columns as needed

    class OAuth(db.Model, OAuthMixin):
        user_id = db.Column(db.Integer, db.ForeignKey(User.id))
        user = db.relationship(User)

    # get_current_user() is a function that returns the current logged in user
    blueprint.set_token_storage_sqlalchemy(OAuth, db.session, user=get_current_user)

Flask-Dance can seamlessly integrate with `Flask-SQLAlchemy`_ for database
integration, `Flask-Login`_ for user management, and `Flask-Cache`_ for caching.
However, none of these other extensions are required. You don't even have to
use `SQLAlchemy`_ at all; if you'd prefer to use a different storage system,
writing a custom integration is easy. `See the documentation for how to
use other token storage systems.
<http://flask-dance.readthedocs.org/en/latest/token-storage.html#custom-storage>`_

.. _SQLAlchemy: http://www.sqlalchemy.org/
.. _Flask-SQLAlchemy: http://pythonhosted.org/Flask-SQLAlchemy/
.. _Flask-Login: https://flask-login.readthedocs.org/
.. _Flask-Cache: http://pythonhosted.org/Flask-Cache/

.. |build-status| image:: https://travis-ci.org/singingwolfboy/flask-dance.svg?branch=master
   :target: https://travis-ci.org/singingwolfboy/flask-dance
   :alt: Build status
.. |coverage-status| image:: https://img.shields.io/coveralls/singingwolfboy/flask-dance.svg
   :target: https://coveralls.io/r/singingwolfboy/flask-dance?branch=master
   :alt: Test coverage
.. |pypi| image:: https://pypip.in/version/Flask-Dance/badge.svg
   :target: https://pypi.python.org/pypi/Flask-Dance/
   :alt: Latest Version
.. |docs| image:: https://readthedocs.org/projects/flask-dance/badge/?version=latest
   :target: http://flask-dance.readthedocs.org/
   :alt: Documentation
