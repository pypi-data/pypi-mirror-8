trytond-customs-value
=====================

This module adds a `customs value` field to Product Variants where the
customs value of a product can be recorded. Since most businesses have the
retail price (or list price) as the customs value, the default behavior is
to use the list price as the customs value.

.. image:: https://secure.travis-ci.org/openlabs/trytond-customs-value.png?branch=develop
  :target: https://travis-ci.org/openlabs/trytond-customs-value.

.. image:: https://coveralls.io/repos/openlabs/trytond-customs-value./badge.png
  :target: https://coveralls.io/r/openlabs/trytond-customs-value.

.. image:: https://pypip.in/download/openlabs_customs_value/badge.svg
    :target: https://pypi.python.org/pypi/openlabs_customs_value/
    :alt: Downloads

.. image:: https://pypip.in/version/openlabs_customs_value/badge.svg
    :target: https://pypi.python.org/pypi/openlabs_customs_value/
    :alt: Latest Version

.. image:: https://pypip.in/license/openlabs_customs_value/badge.svg
    :target: https://pypi.python.org/pypi/openlabs_customs_value/
    :alt: License

Screenshots
-----------

To be uploaded

Why use this module
-------------------

This module was built to be a supporting module for the shipping modules
of Openlabs that integrates with carriers like FedEx, UPS and USPS. When
generating international shipment labels, the carriers expect customs
value to be electronically transferred to them.

Why not just use list price ?
-----------------------------

This works for most businesses. This is indeed the default behavior of
this module.

On the other hand, if you are wholesaler, you may not want
the retail list price being sent as the customs value for the product.
