=======================
Django Request Position
=======================

Django app to add a "position" field to the request, using GeoIP or GPS data given in the request headers. Some
references about this:

* `A Uniform Resource Identifier for Geographic Locations ('geo' URI) <http://tools.ietf.org/rfc/rfc5870>`_.
* `HTTP Geolocation draft-thomson-geopriv-http-geolocation-00 <http://tools.ietf.org/html/draft-thomson-geopriv-http-geolocation-00>`_.


Quick start
-----------

**1** Install using pip::

    pip install django-belt

**2** Add "request_position" to your INSTALLED_APPS settings like this::

    INSTALLED_APPS += ('request_position',)


**3** Add the middleware::

    MIDDLEWARE += (
        'request_position.middleware.RequestPositionMiddleware',
    )
