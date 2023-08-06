pytest-flask
============

A set of `py.test <http://pytest.org>`_ fixtures to test Flask
extensions and applications.

Features
--------

Plugin provides some fixtures to simplify app testing:

- ``client`` - an instance of ``app.test_client``,
- ``client_class`` - ``client`` fixture for class-based tests,
- ``config`` - you application config,
- ``accept_json``, ``accept_jsonp``, ``accept_any`` - accept headers
  suitable to use as parameters in ``client``.

To pass options to your application use the ``pytest.mark.app`` marker:

.. code:: python

    @pytest.mark.app(debug=False)
    def test_app(app):
      assert not app.debug, 'Ensure the app not in debug mode'

During tests execution the application has pushed context, e.g. ``url_for``,
``session`` and other context bound objects are available without context
managers:

.. code:: python

    def test_app(client):
        assert client.get(url_for('myview')).status_code == 200

Response object has a ``json`` property to test a view that returns
a JSON response:

.. code:: python

    @api.route('/ping')
    def ping():
        return jsonify(ping='pong')

    def test_api_ping(client):
        res = client.get(url_for('api.ping'))
        assert res.json == {'ping': 'pong'}

Quick Start
-----------

To start using a plugin define you application fixture in ``conftest.py``:

.. code:: python

    from myapp import create_app

    @pytest.fixture
    def app():
        app = create_app()
        return app

And run your test suite:

.. code:: bash

    $ pip install pytest-flask
    $ py.test

Contributing
------------

Don't hesitate to create a `GitHub issue
<https://github.com/vitalk/pytest-flask/issues>`_ for any **bug** or
**suggestion**.



