Pelican Git
===========

Pelican Git is a library that makes it easy to embed GitHub files in your Pelican_ blogs using simple syntax.

Installation
------------

To install pelican-git, simply:

.. code-block:: bash

    $ pip install pelican-git

Then add a bit of code to your blog configuration:

.. code-block:: python

    PLUGINS = [
        # ...
        'pelican_git',
        # ...
    ]

Usage
-----

In your articles, just add lines to your posts that look like:

.. code-block:: html

    [git:repo=yourname/yourrepo,file=somefile,branch=master,hash=xxxxxxx]

`branch` and `hash` are optional. If you don't specify `branch`, it will be `master`. If you specify `hash` it will overwrite the `branch` setting.

The generated code will embed `css` and `html` content directly into a `div` and replace the original tag. This is faster and cleaner than using `javascript` to rewrite the page content like what gist_it_ does.

Settings
--------

``GIT_CACHE_ENABLED`` - Specifies whether to cache the git files on disk or not. Default is ``False``. (Optional)

Testing
---------

.. code-block:: bash

    $ make install
    $ make test


Authors
---------

Ha.Minh_

Inspired by pelican_gist_

Changelog
---------

- 0.1.0 - Initial version


License
-------

Uses the `MIT`_ license.


.. _Pelican: http://blog.getpelican.com/
.. _MIT: http://opensource.org/licenses/MIT
.. _pelican_gist: https://github.com/streeter/pelican-gist
.. _gist_it: https://github.com/minhhh/gist-it
.. _Ha.Minh: http://minhhh.github.io
