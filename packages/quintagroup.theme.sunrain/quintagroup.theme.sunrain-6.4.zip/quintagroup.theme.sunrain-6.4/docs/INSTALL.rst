Installation
------------

quintagroup.theme.sunrain can be installed in any of the following ways. 

Installation via diazo panel
============================

* Download zip file at http://plone.org/products/sunrain-plone-theme/releases/6.2/sunrain.zip
* Import the theme at the 'Diazo theme' control panel

Installation via buildout
=========================

In the buildout.cfg file of your instance:

* Add ``quintagroup.theme.sunrain`` to the list of eggs to install::

    [buildout]
    ...
    eggs =
        ...
        quintagroup.theme.sunrain

* Re-run buildout::

    $ ./bin/buildout

* Restart the Zope server::

    $ ./bin/instance restart

Then activate 'Sun and Rain Theme' in Plone (Site Setup -> Add-ons).


Installation: development mode
==============================

If you want to customize SunRain theme please use the following installation instructions: 

* download ``quintagroup.theme.sunrain-version.zip`` archive from http://pypi.python.org/pypi/quintagroup.theme.sunrain
* extract theme archive to get ``quintagroup.theme.sunrain-version`` folder. Remove version from 
  folder name to have ``quintagroup.theme.sunrain`` folder
* put ``quintagroup.theme.sunrain`` folder into ``src`` directory of your buildout
* in buildout.cfg file of your buildout add ``quintagroup.theme.sunrain`` to the list of eggs you are developing and  to the list of eggs to install::

       [buildout]
       ...
       develop = src/quintagroup.theme.sunrain
       ...
       eggs =
           ...
           quintagroup.theme.sunrain
   
* Re-run buildout::

    $ ./bin/buildout

* Start instance in development mode::

    $ ./bin/instance fg

* Install ``Sun and Rain Theme`` in Plone (Site Setup -> Add-ons).

Now you can customize SunRain Theme by modifying ``quintagroup.theme.sunrain`` package in ``src`` directory 
of your buildout.