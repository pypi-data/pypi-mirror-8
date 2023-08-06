===============================
Xapo SDK & Tools
===============================

.. image:: https://badge.fury.io/py/xapo_sdk.png
    :target: http://badge.fury.io/py/xapo_sdk

.. image:: https://travis-ci.org/xapo/python-sdk.svg
        :target: https://travis-ci.org/xapo/python-sdk

.. image:: https://pypip.in/d/xapo_sdk/badge.png
        :target: https://pypi.python.org/pypi/xapo_sdk


Xapo's bitcoin sdk & tools

This is the Python version of the Xapo's Widget Tools. These tools allow you (Third Party Application, TPA) to easily embed tools like Payments Buttons, Donation Buttons and other kind of widgets as DIV or iFrame into your web application using your language of choice. In this way, tedious details like encryption and HTML snippet generation are handled for you in a simple and transparent way.


* Free software: BSD license
* Documentation: http://xapo-sdk.readthedocs.org.


Features
--------

* *Iframe* and *Div* HTML widgets snippet generator.



History
-------

0.2.1 (2014-11-04)
---------------------

* Added xapo_api module, including the credit api v0 (this is about to change soon in the incoming v1 api).
* Introduced xapo_tool.PaymentType constants.

0.2.0 (2014-11-01)
---------------------

* Having a TPA is not longer mandatory to provide a micro payments widget. Parameters app_id and app_secret are now optional. 

0.0.1 (2014-10-18)
---------------------

* First release on PyPI.
* Includes:
    * iframe widget
    * div widget

