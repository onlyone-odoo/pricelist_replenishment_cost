===========
Pricelist Replenishment Cost Extension
===========

.. |badge1| image:: https://img.shields.io/badge/maturity-Stable-brightgreen
    :target: https://odoo-community.org/page/development-status
    :alt: Stable
.. |badge2| image:: https://img.shields.io/badge/licence-AGPL--3-blue.png
    :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
    :alt: License: AGPL-3
.. |badge3| image:: https://onlyone.odoo.com/web/image/website/1/logo/OnlyOne%20Soft?unique=dccda5b
    :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
    :alt: License: AGPL-3

|badge1| |badge2| |badge3|

This module extends the functionality of Odoo's pricelist system to support the replenishment cost as a base price for pricelist items, allowing you to define pricing rules based on the product's replenishment cost provided by the `product_replenishment_cost` module.

**Table of contents**

.. contents::
   :local:

Usage
=====

1. Go to *Sales > Configuration > Pricelists* and select or create a pricelist.
2. In the pricelist, add or edit a pricelist item.
3. In the "Based on" field, select "Replenishment Cost" to use the product's replenishment cost as the base price.
4. Configure the computation method (e.g., fixed price, discount, or formula) as needed.
5. Save the pricelist item and use the pricelist in your sales orders to apply pricing based on the replenishment cost.

Known issues / Roadmap
======================

* No known issues at this time.
* Roadmap:
  - Add support for dynamic updates of replenishment cost in pricelist calculations.
  - Provide a configuration option to adjust the currency handling for replenishment cost.

Bug Tracker
===========

* Help Contact

Credits
=======

Authors
~~~~~~~

* Be OnlyOne

Contributors
~~~~~~~~~~~~

* `Be OnlyOne. <https://onlyone.odoo.com/>`_
  
  * Matías Bressanello

Maintainers
~~~~~~~~~~~

This module is maintained by Be OnlyOne