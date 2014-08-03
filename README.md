Xpens
=====

An expense logging application written in Python/Django.

Pre-requisites
--------------

 - Any fairly modern GNU/Linux operating system.
 - Python 2.7.x (recommended), will work on 2.6.x as well.
 - GCC and other related build tools.
 - PostgreSQL server with headers (any recent version supported by Django)
 - Python headers (needed only while running buildout for building some eggs)
 - PostgreSQL client library (libpq) and headers (for building psycopg2 egg)
 - Xpens should work on Mac OS X and Windows provided you know how to tweak
   them for the above requirements. Xpens has been tested on Windows under
   Cygwin.

Installation
------------

 - Download the source code of Xpens and extract it or clone this repository
   using Git.
 - Navigate to the top-level ```xpens/``` directory containing the LICENSE
   and this README file.
 - Run ```python bootstrap.py```. This will download and install [Buildout][1]
   and then configure the environment for running Xpens.
 - If the previous command succeeded without any errors, from the same
   directory run ```bin/buildout```. This will install the dependencies of
   Xpens, including [Django][2] and other eggs.
 - Navigate into the ```xpens/xpens/``` folder.
 - Copy the ```settings_template.py``` to ```settings.py```.
 - Fill in the missing data in the ```settings.py``` like the database
   configuration, ```SECRET_KEY``` and save the file.
 - In case you don't want to use psycopg or PostgreSQL, feel free to modify
   the database engine to whatever suits you and it should work just fine.
 - Navigate back to the top-level ```xpens/``` directory and run
   ```bin/django syncdb```. This will create the tables required by Xpens in
   the PostgreSQL database. Also create the superuser account when prompted.
   This account will be used in the Xpens application.
 - Run the Django development server using ```bin/django runserver```. This
   will start the server on ```locahost:8000```. Note that this works fine
   only for running Xpens locally to develop on it. Using Django's development
   server in production is not recommended.
 - Open your favorite browser and navigate to ```localhost:8000``` to access
   the Xpens application. Login using the user account created before.

Upgrading
---------

 - Since Xpens is in active development, there might be database breakages
   when upgrading between versions from Git since there is no migration
   framework used. So you will have to manually make the database changes
   to be able to run Xpens without any errors.
 - Migration will be implemented after Django 1.7 is released since it has
   in-built migration.

### TODO
 - Document how to deploy Xpens in production.


  [1]: http://www.buildout.org/
  [2]: http://www.djangoproject.com/
