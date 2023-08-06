==============
Python Jenkins
==============

Python Jenkins is a python library that wraps the Jenkins REST interface.
We like to use it to automate our Jenkins servers. Here are some of the
things you can use it for:

* Create new jobs
* Copy existing jobs
* Delete jobs
* Update jobs
* Get a job's build information
* Get Jenkins master version information
* Get Jenkins plugin information
* Start a build on a job
* Create nodes
* Enable/Disable nodes
* Get information on nodes
* and many more..

To install::

    $ sudo python setup.py install

Online documentation:

* http://python-jenkins.readthedocs.org/en/latest/

Developers
==========
Bug report:

* https://bugs.launchpad.net/python-jenkins

Cloning:

* https://git.openstack.org/stackforge/python-jenkins

Patches are submitted via Gerrit at:

* https://review.openstack.org/

Please do not submit GitHub pull requests, they will be automatically closed.

More details on how you can contribute is available on our wiki at:

* http://docs.openstack.org/infra/manual/developers.html

Writing a patch
===============

We ask that all code submissions be flake8_ clean.  The
easiest way to do that is to run tox_ before submitting code for
review in Gerrit.  It will run ``flake8`` in the same
manner as the automated test suite that will run on proposed
patchsets.

Installing without setup.py
===========================

Then install the required python packages using pip_::

    $ sudo pip install python-jenkins

.. _flake8: https://pypi.python.org/pypi/flake8
.. _tox: https://testrun.org/tox
.. _pip: https://pypi.python.org/pypi/pip



