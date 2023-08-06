Installation
------------

quintagroup.theme.schools can be installed in any of the following ways. 

Installation via diazo panel
============================

* Download zip file at http://plone.org/products/schools-plone-skin/releases/6.2/schools.zip
* Import the theme at the 'Diazo theme' control panel

Installation via buildout
=========================

In the buildout.cfg file of your instance:

* Add ``quintagroup.theme.schools`` to the list of eggs to install, e.g.::

    [buildout]
    ...
    eggs =
        ...
        quintagroup.theme.schools

* Re-run buildout::

    $ ./bin/buildout

* Restart the Zope server::

    $ ./bin/instance restart

Then activate 'Schools Theme' in Plone (Site Setup -> Add-ons).


Installation: development mode
==============================

If you want to customize Schools theme please use the following installation instructions: 

* download ``quintagroup.theme.schools-version.zip`` archive from http://pypi.python.org/pypi/quintagroup.theme.schools
* extract theme archive to get ``quintagroup.theme.schools-version`` folder. Remove version from 
  folder name to have ``quintagroup.theme.schools`` folder
* put ``quintagroup.theme.schools`` folder into ``src`` directory of your buildout
* in buildout.cfg file of your buildout add ``quintagroup.theme.schools`` to the list of eggs you are developing and  to the list of eggs to install::

       [buildout]
       ...
       develop = src/quintagroup.theme.schools
       ...
       eggs =
           ...
           quintagroup.theme.schools
   
* Re-run buildout::

    $ ./bin/buildout

* Start instance in development mode::

    $ ./bin/instance fg

* Install ``Schools Theme`` in Plone (Site Setup -> Add-ons).

Now you can customize Schools Theme by modifying ``quintagroup.theme.schools`` package in ``src`` directory 
of your buildout.