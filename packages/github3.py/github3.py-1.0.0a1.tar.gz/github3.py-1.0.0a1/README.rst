.. image::
    https://raw.github.com/sigmavirus24/github3.py/develop/images/gh3-logo.png

github3.py is a comprehensive, actively developed and extraordinarily stable 
wrapper around the GitHub API (v3).

See HISTORY.rst for any "breaking" changes.

Installation
------------

::

    $ pip install github3.py

Dependencies
------------

- requests_  by Kenneth Reitz
- uritemplate.py_ by Ian Cordasco

.. _requests: https://github.com/kennethreitz/requests
.. _uritemplate.py: https://github.com/sigmavirus24/uritemplate

Contributing
------------

Please read the `CONTRIBUTING`_ document.

.. _CONTRIBUTING: https://github.com/sigmavirus24/github3.py/blob/develop/CONTRIBUTING.rst

Testing
~~~~~~~

You can run either ``pip install -r dev-requirements.txt`` to install the 
following before testing or simply ``make test-deps``. It is suggested you do 
this in a virtual enviroment. These need to be installed for the tests to run.

- betamax_
- coverage_ by Ned Batchelder
- mock_ by Michael Foord

.. _betamax: https://github.com/sigmavirus24/betamax
.. _coverage: http://nedbatchelder.com/code/coverage/
.. _mock: http://mock.readthedocs.org/en/latest/

License
-------

Modified BSD license_

.. _license: https://github.com/sigmavirus24/github3.py/blob/develop/LICENSE

Examples
--------

See the docs_ for more examples.

.. _docs: http://github3py.readthedocs.org/en/latest/index.html#more-examples

Testing
~~~~~~~

Install the dependencies from requirements.txt e.g.:

::

    make tests

Author
------

Ian Cordasco (sigmavirus24)

Contact Options
---------------

- Feel free to use the `github3.py`_ tag on StackOverflow for any questions 
  you may have
- If you dislike StackOverflow it is preferred that you send an email to 
  github3.py@librelist.com
- You may also contact (via email) the author directly with 
  questions/suggestions/comments or if you wish to include sensitive data.

.. _github3.py: http://stackoverflow.com/questions/tagged/github3.py
