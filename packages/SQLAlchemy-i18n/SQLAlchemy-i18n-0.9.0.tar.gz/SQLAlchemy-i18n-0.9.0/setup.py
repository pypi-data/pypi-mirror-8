"""
SQLAlchemy-i18n
---------------

Internationalization extension for SQLAlchemy models.
"""

from setuptools import setup, Command
import subprocess


class PyTest(Command):
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        errno = subprocess.call(['py.test'])
        raise SystemExit(errno)


extras_require = {
    'test': [
        'pytest>=2.2.3',
        'Pygments>=1.2',
        'Jinja2>=2.3',
        'docutils>=0.10',
        'flexmock>=0.9.7',
        'psycopg2>=2.4.6',
    ]
}


setup(
    name='SQLAlchemy-i18n',
    version='0.9.0',
    url='https://github.com/kvesteri/sqlalchemy-i18n',
    license='BSD',
    author='Konsta Vesterinen',
    author_email='konsta@fastmonkeys.com',
    description='Internationalization extension for SQLAlchemy models.',
    long_description=__doc__,
    packages=['sqlalchemy_i18n'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        'SQLAlchemy>=0.9',
        'SQLAlchemy-Utils>=0.25.3',
        'six>=1.4.1'
    ],
    extras_require=extras_require,
    cmdclass={'test': PyTest},
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
