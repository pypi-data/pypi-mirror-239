Pytest-Plugin
==============
frysk optionally can be installed with pytest support. If the user chooses to do so,
various features and benefits provided by pytest and its plugins will be also available
for the frysk tests.

E.g.:

* The pytest test collection mechanisms
* Expression based test selection using the :code:`-k` flag
* The test reporting of pytest
* Parallel test execution (using pytest-xdist)
* `And a lot more <https://docs.pytest.org/en/7.2.x/reference/plugin_list.html>`_

How to install the pytest plugin
--------------------------------
In order to install frysk with pytest support, the extra **pytest-plugin**,
needs to be enabled. How this can be achieved depends or your package
management tool. Here are some examples:

* :code:`pip install 'frysk[pytest-plugin]'`
* :code:`poetry add -E "pytest-plugin" frysk`


How to run frysk tests with pytest
----------------------------------
Once you installed frysk with pytest, it will use pytest mechanisms to collect your frysk tests.
So usually a simple :code:`pytest` does the trick.

.. attention::

    In case you want to prevent pytest from running any frysk test just pass :code:`-p no:frysk` to the pytest cli.
