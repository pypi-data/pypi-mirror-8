===============================
Docker Links
===============================

.. image:: https://badge.fury.io/py/docker_links.png
    :target: http://badge.fury.io/py/docker_links

.. image:: https://travis-ci.org/wlonk/docker_links.png?branch=master
        :target: https://travis-ci.org/wlonk/docker_links

.. image:: https://pypip.in/d/docker_links/badge.png
        :target: https://pypi.python.org/pypi/docker_links


Parse Docker links into values useful for Django settings.

* Free software: BSD license
* Documentation: https://docker_links.readthedocs.org.

Usage
-----

Docker links provide environment variables for processes that look like this:: 

    DB_PORT_5432_TCP=tcp://172.17.0.5:5432

That's nice, but not quite right for, say, use in a Django settings file.

So this provides a function that reads an environment variable, and updates it
with overrides you specify::

    BROKER_URL = docker_links.docker_link('AMQP_PORT_6379_TCP', overrides={
        "scheme": "redis",
        "path": "/0",
    })
