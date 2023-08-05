..  -*- coding: utf-8 -*-
.. :Progetto:  metapensiero.sqlalchemy.proxy
.. :Creato:    gio 30 apr 2009 10:01:20 CEST
.. :Autore:    Lele Gaifax <lele@metapensiero.it>
.. :Licenza:   GNU General Public License version 3 or later
..

===============================
 metapensiero.sqlalchemy.proxy
===============================

Expose SQLAlchemy's queries and their metadata to a webservice
==============================================================

This package contains a few utilities to make it easier applying some filtering to a stock
query and obtaining the resultset in various formats.

An helper decorator explicitly designed for Pylons is included: it provides a `property` like
syntax to attach either a ProxiedQuery or a plain Python function to a Controller, handling
``GET``, ``POST`` or ``DEL`` request methods.

Since version 1.7 there are some Pyramid specific subclasses that help using the proxies within
a Pyramid view as well as a `expose` decorator that simplify their implementation.


Usage with Pyramid
------------------

First of all, there are some setup steps to follow:

1. Include the package in the configuration file::

    [app:main]
    use = egg:ph.data

    ...

    pyramid.includes =
        metapensiero.sqlalchemy.proxy.pyramid
        pyramid_tm

   This is not strictly needed, but it will override the standard ``json`` renderer with one
   that uses ``nssjson``, to handle the datetime type.

2. Configure the ``expose`` decorator, for example adding something like the following snippet
   to the ``.../views.py`` source::

    from .models import DBSession

    # Configure the `expose` decorator
    expose.create_session = staticmethod(lambda req: DBSession())

Then you can add views to expose either an entity or a plain select::

    @view_config(route_name='users', renderer='json')
    @expose(User, metadata=dict(
        password=dict(hidden=True, password=True, width=40),
        is_anonymous=False,
        ))
    def users(request, results):
        return results

    sessions_t = Session.__table__

    @view_config(route_name='sessions', renderer='json')
    @expose(select([sessions_t], sessions_t.c.iduser == bindparam('user_id')))
    def sessions(request, results):
        return results

The decorated function may be a generator instead, which has the opportunity of freely
manipulate either the arguments received from the request, or the final result, or both as
follows::

    @expose(User, metadata=dict(
        password=dict(hidden=True, password=True, width=40),
        is_anonymous=False,
        ))
    def complex():
        # Receive request and params
        request, params = (yield)
        log.debug('REQUEST: %r', request)

        # Adjust parameters
        params['new'] = True

        if 'something' in params:
            # Inject other conditions
            something = params.pop('something')
            conditions = (User.c.foo == something,)
            result = yield params, conditions
        else:
            # Go on, and receive the final result
            result = yield params

        # Fix it up
        result['COMPLEX'] = 'MAYBE'

        yield result

Browse SoL__ sources for real usage examples.

__ https://bitbucket.org/lele/sol/src/master/src/sol/views/data.py
