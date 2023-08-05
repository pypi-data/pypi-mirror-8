Messaging ToolKit (mtk)
===================

This software provides a Python package for messaging. The only messaging protocol currently supported is AMQP 0.9.1. This software was originally written because I wasn't happy with the Python client libraries that were available for use with `RabbitMQ <http://www.rabbitmq.com>`_. I didn't like their client interfaces, dependencies, and the bugs I found when using them. There are quite a few more `RabbitMQ Python client libraries <http://www.rabbitmq.com/devtools.html>`_ available now and I suggest you also evaluate them before picking a library that meets your needs.

License
----------

This software is licensed under Version 2.0 of the Apache License.

Installation
--------------

This software can be configured using pip, setuptools, or if you are participating in `XSEDE <http://www.xsede.org>`_, via RPM packages.

pip Installation
-------------------

You may need to install `pip` on your system. There is a package named `python-pip` that a system administrator can install or you can install it as a normal user by downloading and running the `get-pip.py <http://pip.readthedocs.org/en/latest/installing.html>`_ script.

If you are not a system administrator or you wish to install this software outside of the shared Python directories, you may wish to create a Python `virtual environment <http://virtualenv.readthedocs.org/en/latest/>`_. Don't forget to add the virtual environment to your shell environment before running pip.

To install via `pip`, you may need to install simply execute:

    $ pip install mtk

easy_install Installation
-------------------------------

You can also install MTK via `easy_install` by:

    $ easy_install mtk

Contact Information
--------------------------

This software is maintained by `Warren Smith <https://bitbucket.org/wwsmith>`_ and you can contact him on bitbucket via a message. If you have problems with this software you are welcome to submit an `issue <https://bitbucket.org/wwsmith/mtk/issues>`_.