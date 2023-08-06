sphinxcontrib-gravatar is a Sphinx extension for Gravatar

|travis| |coveralls| |downloads| |version| |license|

Features
========
* Provide ``gravatar icon`` for your document.

Set up
======
Make environment with pip::

  $ pip install sphinxcontrib-gravatar

Usage
=====
setup conf.py with::

  # set extension
  extensions += ['sphinxcontrib.gravatar']

  # define gravatar users
  gravatar_users = (
      ('tell-k', {'email': 'ffk2005@gmail.com' }),
  )

write gravatar role::

  .. gravatar:: tell-k

  # If you wanted to write in the text. you can use "Substitution References".

  .. |tell-k-gravatar| gravatar:: tell-k

  my gravatar image |tell-k-gravatar|.

and run::

    $ make html

Option
============

TODO more documented.

conf.py options::

  gravatar_default_size = 30
  gravatar_default_image = "http://www.gravatar.com/avatar/205e460b479e2e5b48aec07710c08d50"
  gravatar_default_rating = "pg"
  gravatar_default_target = "http://github.com/tell-k/"
  gravatar_force_default = True
  gravatar_force_refresh = True
  gravatar_unlink = True
  gravatar_default_class = "custom-classname"

  gravatar_users = (
      ('tell-k', {
          'email': 'ffk2005@gmail.com',
          'default': 'http://www.gravatar.com/avatar/205e460b479e2e5b48aec07710c08d50',
          'force_default': True,
          'unlink': True,
          'target': "http://github.com/tell-k/",
          'rating': "pg",
          'class': u"custom-classname",
          'alt': "alternative text",
      }),
  )

Directive options::

 .. gravatar:: tell-k
    :size: 200
    :default: mm
    :target: http://github.com/tell-k
    :rating: pg
    :class: test-gravatar
    :alt: altnativetext


Requirement
===========
* Python 2.7 or later.
* Sphinx 1.2.x or later.

Using
===========
* `Gravatar APIs <http://en.gravatar.com/site/implement/>`_ .

License
=======
* sphinxcontrib-gravatar Licensed under the BSD License.

See the LICENSE file for specific terms.

.. |travis| image:: https://travis-ci.org/tell-k/sphinxcontrib-gravatar.svg?branch=master
    :target: https://travis-ci.org/tell-k/sphinxcontrib-gravatar

.. |coveralls| image:: https://coveralls.io/repos/tell-k/sphinxcontrib-gravatar/badge.png
    :target: https://coveralls.io/r/tell-k/sphinxcontrib-gravatar
    :alt: coveralls.io

.. |downloads| image:: https://pypip.in/d/sphinxcontrib-gravatar/badge.png
    :target: http://pypi.python.org/pypi/sphinxcontrib-gravatar/
    :alt: downloads

.. |version| image:: https://pypip.in/v/sphinxcontrib-gravatar/badge.png
    :target: http://pypi.python.org/pypi/sphinxcontrib-gravatar/
    :alt: latest version

.. |license| image:: https://pypip.in/license/sphinxcontrib-gravatar/badge.png
    :target: http://pypi.python.org/pypi/sphinxcontrib-gravatar/
    :alt: license


Authors
=======

* tell-k <ffk2005 at gmail.com>

History
=======

0.1.2(Jan 1, 2015)
---------------------
* Exclude test code from installed packages

0.1.1(Dec 31, 2014)
---------------------
* Drop Python-3.2 support. #1
* Support wheel format.

0.1.0(Oct 2, 2014)
---------------------
* First release


