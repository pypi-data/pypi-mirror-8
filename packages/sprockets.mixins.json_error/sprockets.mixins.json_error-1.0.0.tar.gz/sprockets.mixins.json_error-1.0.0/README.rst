sprockets.mixins.json_error
===========================
Handler mixin for writing JSON errors

|Version| |Downloads| |Status| |Coverage| |License|

Installation
------------
``sprockets.mixins.json_error`` is available on the
`Python Package Index <https://pypi.python.org/pypi/sprockets.mixins.json_error>`_
and can be installed via ``pip`` or ``easy_install``:

.. code:: bash

  pip install sprockets.mixins.json_error

Documentation
-------------
https://sprocketsmixinsjson_error.readthedocs.org

Requirements
------------
-  `sprockets <https://github.com/sprockets/sprockets>`_

Example
-------
This examples demonstrates how to use ``sprockets.mixins.json_error`` to format
errors as JSON.

.. code:: python

    from sprockets import mixins.json_error
    from tornado import web

    class MyRequestHandler(json_error.JsonErrorMixin,
                           web.RequestHandler):

        def get(self, *args, **kwargs):
            raise web.HTTPError(404, log_message='My reason')


The response from the handler will automatically be formatted as:

.. code:: json

    {
        "message": "My reason",
        "type": "Not Found"
    }


Version History
---------------
Available at https://sprocketsmixinsjson_error.readthedocs.org/en/latest/history.html

.. |Version| image:: https://badge.fury.io/py/sprockets.mixins.json_error.svg?
   :target: http://badge.fury.io/py/sprockets.mixins.json_error

.. |Status| image:: https://travis-ci.org/sprockets/sprockets.mixins.json_error.svg?branch=master
   :target: https://travis-ci.org/sprockets/sprockets.mixins.json_error

.. |Coverage| image:: https://img.shields.io/coveralls/sprockets/sprockets.mixins.json_error.svg?
   :target: https://coveralls.io/r/sprockets/sprockets.mixins.json_error

.. |Downloads| image:: https://pypip.in/d/sprockets.mixins.json_error/badge.svg?
   :target: https://pypi.python.org/pypi/sprockets.mixins.json_error

.. |License| image:: https://pypip.in/license/sprockets.mixins.json_error/badge.svg?
   :target: https://sprocketsmixinsjson_error.readthedocs.org
