==========
kotti_quiz
==========

This is an extension to the Kotti CMS that allows you to add a quiz content type to your Kotti site.

`Find out more about Kotti`_

``kotti_quiz`` lets you create quizzes with freetext, single-choice and multi-choice answers.

Setup
=====

To activate the ``kotti_quiz`` add-on in your Kotti site, you need to add an entry to the ``kotti.configurators`` setting in your Paste Deploy config.
If you don't have a ``kotti.configurators`` option, add one.
The line in your ``[app:main]`` section could then look like this::

  kotti.configurators = kotti_quiz.kotti_configure

With this, you'll be able to add quiz items in your site.

Work in progress
================

``kotti_quiz`` is considered alpha software, not yet suitable for use in production environments.
The current state of the project is in no way feature complete nor API stable.
If you really want to use it in your project(s), make sure to pin the exact version in your requirements.
Not doing so will likely break your project when future releases become available.


Development
===========

Contributions to ``kotti_quiz`` are highly welcome.
Just clone its `Github repository`_ and submit your contributions as pull requests.

Testing
-------

|build status|_

``kotti_quiz`` aims to have 100% test coverage.
Please make sure that you add tests for new features and that all tests pass before submitting pull requests.
Running the test suite is as easy as running ``py.test`` from the source directory (you might need to run ``python setup.py dev`` to have all the test requirements installed in your virtualenv).


.. _Find out more about Kotti: http://pypi.python.org/pypi/Kotti
.. _Github repository: https://github.com/sbabrass/kotti_quiz
.. |build status| image:: https://secure.travis-ci.org/sbabrass/kotti_quiz.png?branch=master
.. _build status: http://travis-ci.org/sbabrass/kotti_quiz
