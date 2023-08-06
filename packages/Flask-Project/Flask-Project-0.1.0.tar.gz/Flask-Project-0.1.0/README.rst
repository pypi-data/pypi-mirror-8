Flask-Project
===========

.. image:: http://img.shields.io/pypi/v/flask-project.svg
   :target: https://pypi.python.org/pypi/flask-project
   :alt: Latest Version
.. image:: http://img.shields.io/badge/license-MIT-blue.svg
   :target: https://github.com/hyperwood/Flask-Project/blob/master/LICENSE
   :alt: The MIT License
   
Flask web project template generator. Inspired by Flask-Boost.

Installation
------------

::

    pip install Flask-Project

Usage
-----------------

create project
~~~~~~~~~~~~

::

    flask-project new <template_name> <project_name>

Install requirements
~~~~~~~~~~~~~~~~~~~~

``cd`` to project root path, run:
 
::

    virtualenv venv
    . venv/bin/active
    pip install -r requirements.txt

prepare database
~~~~~~~~~~~~~

Create database and update ``SQLALCHEMY_DATABASE_URI`` in ``config/development.py`` as needed.

Then init tables::

    python manage.py prepare_db
    python manage.py add_user -uhyperwood -ehyperwood.yw@gmail.com -ppassword -rAdministrator

Run app
~~~~~~~

Run local server::

    ./test_run.sh

