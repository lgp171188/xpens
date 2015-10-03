Xpens
=====

An expense logging application written in Python/Django.

Pre-requisites
--------------

 - Any fairly modern GNU/Linux operating system.
 - Python 2.7.x/3.4 or newer.
 - GCC and other related build tools.
 - PostgreSQL server with headers (any recent version supported by Django)
 - Python headers (needed only while installing some of the dependencies)
 - PostgreSQL client library (libpq) and headers (for building psycopg2 egg)
 - JPEG and Freetype libraries with headers. This is required by ```Pillow```
   which is used by ```django-simple-captcha``` which generates the captcha
   on the registration page. In Debian/Ubuntu, the packages to be installed
   are ```libjpeg8-dev``` and ```libfreetype6-dev```.
 - Xpens should work on Mac OS X and Windows provided you know how to tweak
   them for the above requirements.

Installation
------------

 - Download the source code of Xpens and extract it or clone this repository
   using Git.
 - Navigate to the top-level ```xpens/``` directory containing the LICENSE
   and this README file.
 - It is recommended to perform the following steps after creating a virtualenv
   environment and activating it. This will install all the dependencies of
   Xpens in an isolated, local python environment without affecting the
   system python. If not, you will have to prefix the commands with a
   ```sudo``` or execute them as a root user.
 - Run ```pip install -r requirements.txt```. This will install all the
   dependencies required to deploy Xpens. In case you want to develop Xpens,
   run ```pip install -r requirements/local.txt```.
 - Navigate into the ```xpens/xpens/``` folder.
 - Copy the ```settings_template.py``` to ```settings.py```.
 - Fill in the missing data in the ```settings.py``` like the database
   configuration, ```SECRET_KEY``` and save the file.
 - In case you don't want to use psycopg2 or PostgreSQL, feel free to modify
   the database engine to whatever suits you and it should work just fine. In
   case you change the database engine, replace ```psycopg2``` with the
   name of the database driver that you want to use in
   ```requirements/common.txt``` and then install it by running
   ```pip install -r requirements.txt``` from the top-level directory.
 - Navigate to the ```xpens/``` sub-directory in the top-level ```xpens```
   directory and run ```python manage.py migrate```. This will create the
   tables required by Xpens in the database and apply the unapplied migrations,
   if any. Also create the superuser account when prompted. This account
   will be used to login to the Xpens application.
 - Running in development mode
   - Run the Django development server using ```python manage.py runserver```.
     This will start the server on ```locahost:8000```. Note that this works fine
     only for running Xpens locally to develop on it. Using Django's development
     server in production is not recommended.
   - Open your favorite browser and navigate to ```localhost:8000``` to access
     the Xpens application. Login using the user account created before.
 - Deploying in production
   - Copy ```settings_template_production.py``` to ```settings.py``` and edit it
     as described in the following steps.
   - Configure the ```ADMINS``` setting.
   - Set ```DEBUG``` setting to ```False``` to disable debug mode in production.
   - Collect all the static files to the ```STATIC_ROOT``` location
     specified in ```settings.py``` by running the command
     ```python manage.py collectstatic```. This location has to be served under
     the ```STATIC_URL``` path, by the web server.
   - Run ```python manage.py check --deploy``` to view the security recommendations
     for running Xpens in production. Configure whatever is relevant to your
     production environment.
   - If using apache2 webserver with mod_wsgi, please check out
     ```deploy/apache2_mod_wsgi.conf``` file for an example configuration. For
     more details, please read the mod_wsgi and Django documentation.

Upgrading
---------

 - When you update Xpens from its git repository, be aware of the following things:
   - If there are any changes to the requirements, you will have to run
     the ``pip install`` commands like described in the installation section
     from the top-level ```xpens/``` directory to install/update the dependencies.
   - If there are any changes to ```settings_template.py``` (or
     ```settings_template_production.py``` if you are deploying Xpens in production),
     you will have to merge them with the ```settings.py``` in your environment.
   - If there are new apps added to the ```INSTALLED_APPS``` variable in
     ```settings_template.py``` or any new models added, you will have to run
     ```python manage.py syncdb``` to update the database, after doing the previous
     step.
   - Since Xpens is in active development, there might be changes to the
     database schema  when upgrading between versions from Git. So do run
     ```python manage.py migrate``` to apply the database migrations before trying to
     run or deploy Xpens.


Contributing
------------

Please read CONTRIBUTING.md

  [1]: http://www.djangoproject.com/
