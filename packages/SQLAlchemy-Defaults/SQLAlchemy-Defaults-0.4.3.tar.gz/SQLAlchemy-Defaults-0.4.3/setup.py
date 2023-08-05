"""
SQLAlchemy-Defaults
-------------------

Smart SQLAlchemy defaults for lazy guys, like me.
"""

import os
import re
import sys
from setuptools import setup


PY3 = sys.version_info[0] == 3
HERE = os.path.dirname(os.path.abspath(__file__))


def get_version():
    filename = os.path.join(HERE, 'sqlalchemy_defaults', '__init__.py')
    with open(filename) as f:
        contents = f.read()
    pattern = r"^__version__ = '(.*?)'$"
    return re.search(pattern, contents, re.MULTILINE).group(1)


extras_require = {
    'test': [
        'pytest==2.2.3',
        'Pygments>=1.2',
        'Jinja2>=2.3',
        'docutils>=0.10',
        'flexmock>=0.9.7',
        'psycopg2>=2.4.6',
        'PyMySQL==0.6.1',
    ]
}


setup(
    name='SQLAlchemy-Defaults',
    version=get_version(),
    url='https://github.com/kvesteri/sqlalchemy-defaults',
    license='BSD',
    author='Konsta Vesterinen',
    author_email='konsta@fastmonkeys.com',
    description=(
        'Smart SQLAlchemy defaults for lazy guys, like me.'
    ),
    long_description=__doc__,
    packages=['sqlalchemy_defaults'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        'six',
        'SQLAlchemy>=0.7.8',
    ],
    extras_require=extras_require,
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
