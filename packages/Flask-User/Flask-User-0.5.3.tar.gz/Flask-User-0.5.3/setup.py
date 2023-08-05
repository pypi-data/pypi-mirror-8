"""

.. image:: https://travis-ci.org/lingthio/Flask-User.png?branch=master
    :target: https://travis-ci.org/lingthio/Flask-User

.. comment .. image:: https://pypip.in/v/Flask-User/badge.png
.. comment     :target: https://pypi.python.org/pypi/Flask-User

.. comment .. image:: https://coveralls.io/repos/lingthio/Flask-User/badge.png?branch=master
.. comment     :target: https://coveralls.io/r/lingthio/Flask-User?branch=master

.. comment .. image:: https://pypip.in/d/Flask-User/badge.png
.. comment     :target: https://pypi.python.org/pypi/Flask-User

.. comment .. image:: https://pypip.in/license/Flask-User/badge.png
.. comment     :target: https://pypi.python.org/pypi/Flask-User

Customizable User Account Management for Flask
----------------------------------------------

Many web applications require User Account Management features such as **Register**, **Confirm email**,
**Login**, **Change username**, **Change password** and **Forgot password**.

Some also require **Role-based Authorization** and **Internationalization**.

Wouldn't it be nice to have a package that would offer these features **out-of-the-box**
while **retaining full control over the workflow and presentation** of this process?

Flask-User aims to provide such a ready-to-use **AND** fully customizable solution:

* **Reliable**
* **Secure**
* **Fully customizable**
* **Ready to use**
* **Role-based Authorization**
* **Internationalization**
* **Well documented**
* Tested on Python 2.6, 2.7 and 3.3

Demo
----
| `Flask-User Demo <https://flask-user-demo.herokuapp.com/>`_
| (If you're the first visitor in the last hour, this may take a few seconds to load)

Documentation
-------------
`Flask-User Documentation <https://pythonhosted.org/Flask-User/>`_

Revision History
----------------
`Flask-User Revision History <http://pythonhosted.org//Flask-User/index.html#revision-history>`_

Contact Information
-------------------
Ling Thio - ling.thio [at] gmail.com

Acknowledgements
----------------
This project would not be possible without the use of the following amazing offerings:

* `Flask <http://flask.pocoo.org/>`_
* `Flask-Babel <http://babel.pocoo.org/>`_
* `Flask-Login <https://flask-login.readthedocs.org/en/latest/>`_
* `Flask-Mail <http://pythonhosted.org/flask-mail/>`_
* `SQLAlchemy <http://www.sqlalchemy.org/>`_ and `Flask-SQLAlchemy <http://pythonhosted.org/Flask-SQLAlchemy/>`_
* `WTForms <http://wtforms.readthedocs.org/en/latest/>`_ and `Flask-WTF <https://flask-wtf.readthedocs.org/en/latest/>`_

Alternative Flask extensions
----------------------------
* `Flask-Login <https://flask-login.readthedocs.org/en/latest/>`_
* `Flask-Security <https://pythonhosted.org/Flask-Security/>`_

"""

from __future__ import print_function
from setuptools import setup

setup(
    name='Flask-User',
    version='0.5.3',
    url='http://github.com/lingthio/Flask-User',
    license='BSD License',
    author='Ling Thio',
    author_email='ling.thio@gmail.com',
    description='Customizable User Account Management for Flask: Register, Confirm email, Login, Change username, Change password, Forgot password and more.',
    long_description=__doc__,
    keywords='Flask User Registration Email Username Confirmation Password Reset',
    packages=['flask_user'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        'passlib',
        'py-bcrypt',
        'pycrypto',
        'Flask',
        'Flask-Babel',
        'Flask-Login',
        'Flask-Mail',
        'Flask-SQLAlchemy',
        'Flask-WTF',
    ],
    test_suite="flask_user.tests.run_tests",
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Flask',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: Dutch',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Security',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
