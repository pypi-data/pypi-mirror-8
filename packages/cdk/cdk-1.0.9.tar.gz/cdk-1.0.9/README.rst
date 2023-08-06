Courseware Development Kit (CDK)
================================

.. image:: https://travis-ci.org/twitter/cdk.png?branch=master
    :target: https://travis-ci.org/twitter/cdk

Use CDK to write documents in `AsciiDoc <http://www.methods.co.nz/asciidoc/>`_ and produce elegant single-file slidedecks as html.

Please see the docs at http://cdk.readthedocs.org/en/latest/

Installation & Usage
--------------------

::

    sudo pip install cdk # if you don't have pip try sudo easy_install cdk
    cdk --generate=sample.asc # generate a sample presentation
    cdk sample.asc  # compile it to html
    open sample.html # use a browser

Contact
--------

In the remote possibility that there exist bugs in this code, please report them to:
https://github.com/twitter/cdk/issues

Authors
--------

* Simeon Franklin (@simeonfranklin)

License
--------

Copyright 2013 Twitter, Inc and other contributors

Licensed under the Apache License, Version 2.0: http://www.apache.org/licenses/LICENSE-2.0
