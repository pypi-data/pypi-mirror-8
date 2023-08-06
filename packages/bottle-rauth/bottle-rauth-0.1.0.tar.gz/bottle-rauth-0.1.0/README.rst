Bottle-RAuth
############

.. _description:

Bottle-RAuth -- Short description.

.. _badges:

.. image:: http://img.shields.io/travis/klen/bottle-rauth.svg?style=flat-square
    :target: http://travis-ci.org/klen/bottle-rauth
    :alt: Build Status

.. image:: http://img.shields.io/coveralls/klen/bottle-rauth.svg?style=flat-square
    :target: https://coveralls.io/r/klen/bottle-rauth
    :alt: Coverals

.. image:: http://img.shields.io/pypi/v/bottle-rauth.svg?style=flat-square
    :target: https://pypi.python.org/pypi/bottle-rauth

.. image:: http://img.shields.io/pypi/dm/bottle-rauth.svg?style=flat-square
    :target: https://pypi.python.org/pypi/bottle-rauth

.. image:: http://img.shields.io/gratipay/klen.svg?style=flat-square
    :target: https://www.gratipay.com/klen/
    :alt: Donate

.. _documentation:

**Docs are available at https://bottle-rauth.readthedocs.org/. Pull requests
with documentation enhancements and/or fixes are awesome and most welcome.**

.. _contents:

.. contents::

.. _requirements:

Requirements
=============

- python >= 2.6

.. _installation:

Installation
=============

**Bottle-RAuth** should be installed using pip: ::

    pip install bottle-rauth

.. _usage:

Usage
=====

::

    import bottle

    from bottle_rauth import RAuthPlugin

    app = bottle.Bottle()
    app.install(RAuthPlugin(github={
        'type': 'oauth2',
        'client_id': 'e3e297bb9f506cbea557',
        'client_secret': 'd113380beb8f1ed8a77b688e2b81b76c9be00d09',
        'authorize_url': 'https://github.com/login/oauth/authorize',
        'access_token_url': 'https://github.com/login/oauth/access_token',
        'base_url': 'https://api.github.com/',
    }))


    @app.route('/')
    def index():
        return '<a href="/github">Login with github</a>'


    @app.route('/github', provider='github')
    def github(rauth):
        info = rauth.get('user').json()
        info['token'] = rauth.access_token
        return info

    if __name__ == '__main__':
        app.run(port=5000)


.. _bugtracker:

Bug tracker
===========

If you have any suggestions, bug reports or
annoyances please report them to the issue tracker
at https://github.com/klen/bottle-rauth/issues

.. _contributing:

Contributing
============

Development of Bottle-RAuth happens at: https://github.com/klen/bottle-rauth


Contributors
=============

* klen_ (Kirill Klenov)

.. _license:

License
=======

Licensed under a `BSD license`_.

.. _links:

.. _BSD license: http://www.linfo.org/bsdlicense.html
.. _klen: https://github.com/klen
