`Raptorize` WSGI Middleware
===========================

Fact:  every WSGI app is better with a velociraptor.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. image:: https://github.com/ralphbean/raptorizemw/raw/master/raptorizemw/resources/raptor.png

Installation
------------

You could install it yourself with `pip`::

    $ pip install raptorizemw

Or you could add ``raptorizemw`` to the list of required packages in the
``setup.py`` file of your project.

Usage in Pyramid
----------------

Edit ``myapp/__init__.py`` and replace the ``return config.make_wsgi_app()``
line with the following::

    import raptorizemw
    app = config.make_wsgi_app()
    app = raptorizemw.make_middleware(app)
    return app

Restart your app, but watch out for raptors!

Usage in Flask
--------------

Edit ``yourapp.py`` and replace the ``app.run()`` line with the following::

    import raptorizemw
    app.wsgi_app = raptorizemw.make_middleware(app.wsgi_app)
    app.run()

ZOMG!

Usage in TurboGears 2
---------------------

Simply edit ``myapp/config/middleware.py`` and add the following to
``make_app(...)``::

    # Wrap your base TurboGears 2 application with custom middleware here
    import raptorizemw
    app = raptorizemw.make_middleware(app)


Usage in a PasteDeploy pipeline
-------------------------------

You can also add raptors into your PasteDeploy pipeline like so::

    [pipeline:main]
    pipeline = 
        raptorize
        my-app

    [filter:raptorize]
    use = egg:raptorizemw
    enterOn = konami-code
    delayTime = 3000
    random_chance = 0.25
    only_on_april_1st = True

    [app:myapp]
    ...

Essentially, you're able to specify ``raportizemw`` as a filter within your
WSGI pipeline, and configure options accordingly as per the `Configuration`_
section below.

Configuration
-------------

``make_middleware(...)`` and ``RaptorizeMiddleware.__init__(...)`` both take
a number of configuration keywords:

 - ``enterOn`` can be one of two actions: 'timer' or 'konami-code'.  If 'timer'
   is specified, then the raptor is shown on page load.  If 'konami-code', then
   the raptor is shown if the page-viewing user enters the sacred sequence.
   Default is 'timer'.
 - ``delayTime`` must be an ``int`` and is the number of milliseconds until the
   raptor is shown.  Default is 2000.
 - ``random_chance`` must be a float between 0.0 and 1.0 representing a 'percent
   chance' to load the raptor.  A value of 1.0 means the raptor will be injected
   every time; a value of 0.0 means it will never be injected; a value of 0.5
   will result in a 50% chance of raptors.  Default is 1.0.
 - ``only_on_april_1st`` should be a ``bool`` value that will restrict raptors
   only to April Fool's day. The configuration will coerce Boolean-like strings
   (such as ``t``, ``true``, ``y``, ``yes``, ``on`` and ``1``) into a suitable
   format if provided in this manner (such as through a text-based pipeline
   configuration). Default is ``False``.

For example::

    app = raptorizemw.make_middleware(
        app,
        enterOn='konami-code',
        delayTime=500,
        random_chance=0.5,
        only_on_april_1st=True
    )

will result in 50% of pages loaded with raptors on April Fool's Day only.  These
raptors will only be displayed if the user also enters the konami code, and
quite quickly, after only a half a second.

Credits
-------

This WSGI-fication of the raptorize jquery plugin was written
by `Ralph Bean <http://threebean.org>`_.  Real credit goes to the people over at
ZURB who authored the `original jquery plugin
<http://www.zurb.com/playground/jquery-raptorize>`_.

Get the source
--------------

The code and bug tracker live over at http://github.com/ralphbean/raptorizemw.
Please fork and improve!
