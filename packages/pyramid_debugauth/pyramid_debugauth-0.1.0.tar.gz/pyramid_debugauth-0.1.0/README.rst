=================
Pyramid_debugauth
=================

Debug Authentication Policy for Pyramid. Provide a simple and standard way to
define the pyramid principals from the HTTP client.

.. warning::

   (Obviously) This pyramid is totally unsafe for production and should be
   restricted to debug usage / development phase.

* PyPI: https://pypi.python.org/pypi/pyramid_debugauth
* Bitbucket: https://bitbucket.org/Ludia/pyramid_debugauth
* Bugs: https://bitbucket.org/Ludia/pyramid_debugauth/issues


Installation
============

Install using setuptools, e.g. (within a virtualenv)::

  $ pip install pyramid_debugauth


Setup
=====

Once ``pyramid_debugauth`` is installed, you can define a authentication policy
with ``config.set_authentication_policy``.

In your Pyramid project:

.. code-block:: python

   from pyramid.authorization import ACLAuthorizationPolicy
   from pyramid_debugauth import DebugAuthenticationPolicy

   config = Configurator(.....)
   config.set_authentication_policy(DebugAuthenticationPolicy())
   config.set_authorization_policy(ACLAuthorizationPolicy())


Usage
=====

The DebugAuthenticationPolicy allows a client to impersonate any user and
specify any number of principals desired using the standard *Authorization*
http header and a non-standard auth-scheme *Debug* (:rfc:`7235`):

   ``Authorization: Debug user_id [principal_1] [principal_2] ...``

With common http clients:

   $ curl http://localhost:6543 -H 'Authorization: Debug bob admin'

   $ http http://localhost:6543 'Authorization: Debug bob admin'


Or using a non-standard *authorization* query parameter:

   ``http://localhost:6543/protected?authorization=debug%20user_id%20principal_1

With common http clients:

   $ curl http://localhost:6543?authorization%20debug%20bob%20admin

   $ http http://localhost:6543?authorization\ debug\ bob\ admin


Development
===========

Running tests::

   $ virtualenv venv
   $ . venv/bin/activate
   (venv)$ pip install -r requirements-test.txt
   (venv)$ nosetests
