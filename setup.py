import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

requires = [
    'django==1.8.2',
    'psycopg2',
    'django-nvd3==0.7.4',
    'pillow',
    'django-simple-captcha',
    'python-dateutil',
    'pytz'
    ]

setup(name='xpens',
      version='0.4',
      description='An expense logging application written in Python/Django',
      long_description='An expense logging application written in Python/Django',
      license = 'AGPLv3+',
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Django",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        ],
      author='L. Guruprasad',
      author_email='lgp171188@gmail.com',
      url='https://github.com/lgp171188/xpens/',
      keywords='web wsgi django expense',
      packages=find_packages(),
      install_requires=requires,
      )
