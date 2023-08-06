======================
eWay Payment for Oscar
======================

.. image:: https://travis-ci.org/snowball-one/django-oscar-eway.png?branch=master
    :target: https://travis-ci.org/snowball-one/django-oscar-eway?branch=master

.. image:: https://coveralls.io/repos/snowball-one/django-oscar-eway/badge.png?branch=master
    :target: https://coveralls.io/r/snowball-one/django-oscar-eway?branch=master


**Disclaimer:** The integration to the eWay API defined in this project is *incomplete* and
currently only provides the `Token Payment`_ using `eWay's Rapid 3.0 API`_. We
haven't had the need or time to provide any other part(s) of the API, yet.
Contributions to extend the functionality are more than welcome.


Installation
------------

You can install ``django-oscar-eway`` directly from github by running::

    $ pip install django-oscar-eway

After you have successfully installed it, you should add the app to your
``INSTALLED_APPS``::

    INSTALLED_APPS = (
        ...
        'eway',
    )

and provide the eWay-specific settings in your ``settings.py``::

    EWAY_API_KEY = "YOUR API KEY"
    EWAY_PASSWORD = "YOUR API PASSWORD"
    EWAY_USE_SANDBOX = True
    EWAY_CURRENCY = "AUD"

To obtain access to their developer sandbox, head over to their `developer
site`_ and create an account.

Finally, you have to apply the migrations provided by the package to your
project's database. These are necessary for logging of eWay communication
during the payment process and will make tracking down errors easier::

    $ ./sandbox/manage.py migrate eway


Integrate eWay In The Checkout
------------------------------

The simplest way to integrate your project's checkout with eWay is to use the
``EwayPaymentDetailMixin`` to extend your ``PaymentDetailView``. All you need
to do is create a new ``PaymentDetailView`` in your checkout app, import the
mixin and add it to the view class. It should now look similar to this::

    from oscar.apps.checkout.views import PaymentDetailsView as OscarPaymentDetailsView
    from eway.rapid.mixins import EwayPaymentDetailMixin

    class PaymentDetailsView(EwayPaymentDetailMixin, OscarPaymentDetailsView):
        template_name = 'checkout/payment_details.html'

In addition to that you need to hook up the view that is called by the eWay
response redirect. A default URL can be defined by adding the following line to
your URL patterns::

    urlpatterns = patterns('',
        ...
        url(r'^checkout/eway/', include('eway.rapid.urls')),
        ...
    )

Now it's time to try it out and see if it works :)


Further Documentation
---------------------

This package is still in its early stages. We'll try and provide more
documentation soon. Until then, feel free to raise an issue or ask questions
on the `django-oscar mailing list`_.


Contributing
------------

Your need more functionality, found a bug or simply want to help us make this
package better? Create a fork, make your changes and open a pull request. We'll
be thankful for it!


License
-------

The package is released under the new BSD license.


.. _`Oscar`: http://github.com/tangentlabs/django-oscar
.. _`eWay`: http://www.eway.com.au
.. _`Token Payment`: http://www.eway.com.au/developers/api/token
.. _`eWay's Rapid 3.0 API`: http://www.eway.com.au/developers/api
.. _`developer site`: http://www.eway.com.au/developers/partners/become-a-partner
.. _`django-oscar mailing list`: https://groups.google.com/forum/#!forum/django-oscar


=========
Changelog
=========

0.2.0
-----

* Add support for Oscar v0.7 and v0.8
* Add support for Django 1.7 when using Oscar 0.8. Earlier versions of Oscar
  are not supported because Django 1.7 support is only available starting with
  Oscar 0.8.


0.1.1
-----

* Add tests for migrations using PostgreSQL and MySQL databases on Travis
* Add a fix for MySQL when renaming tables in migration ``0004`` which fails
  if constraints on the foreign keys are not dropped before renaming them. This is
  details in ticket #466 for South: http://south.aeracode.org/ticket/466
* Fix dependency with Oscar's ``basket`` app in eway migration.
* Rename deprecated tables in migration due to PostgreSQL issue with uppercase
  names.


0.1.0
-----

* Initial version of the project.


