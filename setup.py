#!/usr/bin/env python

import multiprocessing  # noqa
import os
import sys

from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand


tests_require = (
    'pytest',
    'pytest-django'
)


install_requires = (
    'Django>=3.2,<5.1',
)


class DjangoTest(TestCommand):
    DIRNAME = os.path.dirname(__file__)
    APPS = ('tests',)

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        from django.conf import settings

        db_engine = os.environ.get('DJANGO_DB_ENGINE', 'sqlite')
        if db_engine == 'mysql':
            db_settings = {
                'ENGINE': 'django.db.backends.mysql',
                'NAME': os.environ['DJANGO_DB_NAME'],
                'USER': os.environ['DJANGO_DB_USER'],
            }
        elif db_engine == 'postgres':
            db_settings = {
                'ENGINE': 'django.db.backends.postgresql_psycopg2',
                'NAME': os.environ['DJANGO_DB_NAME'],
                'USER': os.environ['DJANGO_DB_USER'],
            }
        elif db_engine == 'sqlite':
            db_settings = {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': os.path.join(self.DIRNAME, 'database.db'),
            }
        else:
            raise ValueError("Unknown DB engine: %s" % db_engine)

        # Common settings.
        settings.configure(
            DEBUG=True,
            DATABASES={'default': db_settings},
            CACHES={'default': {'BACKEND': 'django.core.cache.backends.dummy.DummyCache'}},
            INSTALLED_APPS=self.APPS)

        import django
        import pytest
        django.setup()
        sys.exit(pytest.main(["tests/"]))


setup(
    name='django-livefield',
    version='4.1.0',
    description='Convenient soft-deletion support for Django models',
    long_description=(
        open('README.rst').read() + '\n\n' +
        open('CHANGELOG.rst').read() + '\n\n' +
        open('AUTHORS.rst').read()),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Framework :: Django :: 3.2',
        'Framework :: Django :: 4.0',
        'Framework :: Django :: 4.1',
        'Framework :: Django :: 4.2',
        'Framework :: Django :: 5.0',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
    ],
    keywords='python django soft-delete',
    url='https://github.com/hearsaycorp/django-livefield',
    author='Hearsay Social',
    author_email='opensource@hearsaysocial.com',
    license='MIT',
    package_dir={'': 'src'},
    packages=find_packages('src'),
    install_requires=install_requires,
    tests_require=tests_require,
    cmdclass={'test': DjangoTest},
)
