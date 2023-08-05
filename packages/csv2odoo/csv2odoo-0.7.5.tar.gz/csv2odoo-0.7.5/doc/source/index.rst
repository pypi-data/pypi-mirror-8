.. csv2odoo documentation master file, created by
   sphinx-quickstart on Tue Dec 13 10:46:30 2011.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to csv2odoo's documentation!
************************************

`csv2odoo` is a Python converter from the `csv` format to `OpenERP` data record.

`csv2odoo` is an easy way to import records from heterogeneous datas by editing
a simple script as the manner of `OpenERP` data model.
You can specify pre-treatment(s) before any records insertions, you can also,
according to criteria, omit the insertion of an entire record, mofify it or just
create it (CRUD abilities).

Some features of `csv2odoo` include abilities of Python `csv` module to specify
input file configuration. It also include somme abilities of some third party
library according to your needs.


Quick start
===========

.. code-block:: python
    
    #!/usr/bin/env python
    #.. your_script.py
    from csv2odoo import Model, Field, Odoo, Session

    #
    # Configure OpenERP connection
    #

    odoo = Odoo(
        host='198.168.0.1', port=8069,
        user='admin', pwd='admin', dbname='database', 
        lang'fr_FR')

    #
    # Create a new importation instance::
    #

    session = Session(
        'file.csv', delimiter=';', quotechar='"', encoding='utf-8',
        offset=1, limit=10)
    
    #
    # Define your mapping to link both csv and OpenERP::
    #

    # res.partner is unique by siren and will not be updated if exists
    res_partner = Model('res.partner', fields=[
            Field('name', columns=[1]),
            Field('siren', columns=[2]),
            Field('website', columns=[16]),
        ], update=False, search=['siren'])
    
    # res.country is unique by code and name and will not be updated if exists
    res_country = Model('res.country', fields=[ 
            Field('code', columns=[13], default='FR'),
            Field('name', columns=[13], default='FRANCE'),
        ], update=False, search=['code', 'name'])

    # res.partner.address is unique by type and partner_id
    res_partner_contact = Model('res.partner', fields=[

            # Simple fields, some with default value and some unique between records
            Field('zip', columns=[9], default='35000'),
            Field('city', columns=[10], default='RENNES'),
            Field('phone', column=[14]),
            Field('fax', columns=[15]),
            Field('email', columns=[17], unique=True),
            Field('cedex', columns=[68]),

            # Mixing columns (by concatenation or selection)
            Field('street', columns=[7, 6], method='concatenate'),
            Field('street2', columns=[8, 5], method='concatenate'),

            # Model's relations with res.partner which must exists
            Field('country_id', relation=res_country),
            Field('parent_id', relation=res_partner, required=True),

            # Adding a custom value to a missing field in the `csv` file
            Field('type', custom='delivery'),
        ], search=['type', 'partner_id'])

    #
    # Finally join objects to the session which starts the import process
    #

    # There is no particular needs to also inject res.partner model, as it's 
    # already contained as a relation of res.partner.address
    session.bind(odoo, [res_partner_contact, ])

    #
    # Optionaly: show statistics of records's activities during the importation process
    #

    csv2odoo.show_stats()

Download and install
====================

See :ref:`download-install` section.

Documentation
=============

.. toctree::
    :maxdepth: 2

    download_install
    how-to
    apis
    cli
    callbacks
    examples

Supported Python versions
=========================

`csv2odoo` support Python versions 2.6 and 2.7.

License
=======

This software is made available under the LGPLv3 license.

Bugs or suggestions
===================

Please, feel free to report bugs or suggestions in the `Bug Tracker
<https://bitbucket.org/StefMangin/python-csv2odoo/issues?status=new&status=open>`_!

Indices and tables 
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
* :ref:`glossary`
