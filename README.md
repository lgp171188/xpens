Xpens
=====

An expense logging application written in Python/Django.

Pre-requisites
--------------

 - Any fairly modern GNU/Linux operating system. Mac OS X/ Windows might work as well, provided you know how to tweak them for the below steps.
 - Python 2.7.x (recommended), will work on 2.6.x as well.
 - PostgreSQL server (any recent version supported by Django)
 - Python headers (needed only while running buildout for building some eggs)
 - PostgreSQL headers (for building psycopg2 egg)

Installation
------------

 - Download the source code of Xpens and extract it or clone this repository using Git.
 - Navigate to the top-level ```xpens/``` directory containing the LICENSE and this README file.
 - Run ```python bootstrap.py```. This will download and install [Buildout][1] and then configure the environment deploying Xpens.
 - If the previous command succeeded without any errors, from the same directory run ```bin/buildout```. This will install the dependencies of Xpens, including [Django][2] and other eggs.
 - Navigate into the ```xpens/xpens/``` folder.
 - Copy the ```settings_template.py``` to ```settings.py```.
 - Fill in the missing data in the ```settings.py``` like the database configuration, ```SECRET_KEY``` and save the file.
 - Navigate back to the top-level ```xpens/``` directory and run ```bin/django syncdb```. This will create the tables required by Xpens in the PostgreSQL database. Also create the superuser account when prompted. This account will be used in the Xpens application.
 - Run the Django development server using ```bin/django runserver```. This will start the server on ```locahost:8000```. Note that this works fine only for running Xpens locally to develop on it. Using Django's development server in production is not recommended.
 - Open your favorite browser and navigate to ```localhost:8000``` to access the Xpens application.

### TODO
 - Document how to deploy Xpens in production.


  [1]: http://www.buildout.org/
  [2]: http://www.djangoproject.com/
