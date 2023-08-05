===============
Buildbot GitLab
===============

.. image:: https://pypip.in/v/buildbot-gitlab/badge.png
    :target: https://pypi.python.org/pypi/buildbot-gitlab
.. image:: https://pypip.in/d/bumpr-gitlab/badge.png
    :target: https://pypi.python.org/pypi/buildbot-gitlab

The Buildbot GitLab plugin provides an easy to install and configure enhancement for Buildbot.

Installation
============

You can download and install the latest version of this software from the Python package index (PyPI) as follows:

.. code-block:: console

    pip install --upgrade buildbot-gitlab


Usage
=====

Buildbot Gitlab uses a RESTful API to manage multiple projects. The project name and containing folder used in Gitlab
is stored within a .json file, which is then parsed during the BuildMaster startup in order to generate builders for
each project.


TO DO: More info to follow...

Tests
=====

Included with the API are unit tests which can be run as part of the Buildbot test procedure.
The tests can be run via the following command:

.. code-block:: console

    PYTHONPATH=. trial buildbot.test

Which should be executed from within the buildbot directory.

Additionally rather than running the entire Buildbot test suite, the tests specific to Buildbot Gitlab can be run with
the following commands

.. code-block:: console

    PYTHONPATH=. trial buildbot.test.unit.test_gitlab_api

    PYTHONPATH=. trial buildbot.test.unit.test_gitlab_resources

The tests can also be run using Pythons Unit testing framework (PyUnit) instead of twisted trial with the following command:

.. code-block:: console

    PYTHONPATH=. python -m unittest -v buildbot.test.unit.test_gitlab_api

    PYTHONPATH=. python -m unittest -v buildbot.test.unit.test_gitlab_resources

Note that the gitlab_resources tests requires buildbot & twisted packages to be present, as these provide the functionality
for fake web requests used by the resource tests. The API tests function independently of other packages.