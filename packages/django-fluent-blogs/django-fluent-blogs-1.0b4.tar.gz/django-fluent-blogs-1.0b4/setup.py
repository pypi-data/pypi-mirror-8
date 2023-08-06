#!/usr/bin/env python
from setuptools import setup, find_packages
from os import path
import codecs
import os
import re
import sys


# When creating the sdist, make sure the django.mo file also exists:
if 'sdist' in sys.argv or 'develop' in sys.argv:
    try:
        os.chdir('fluent_blogs')

        from django.core.management.commands.compilemessages import Command
        command = Command()
        command.execute(stdout=sys.stderr, verbosity=1)
    except ImportError:
        # < Django 1.7
        from django.core.management.commands.compilemessages import compile_messages
        compile_messages(sys.stderr)
    finally:
        os.chdir('..')


def read(*parts):
    file_path = path.join(path.dirname(__file__), *parts)
    return codecs.open(file_path, encoding='utf-8').read()


def find_version(*parts):
    version_file = read(*parts)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", version_file, re.M)
    if version_match:
        return str(version_match.group(1))
    raise RuntimeError("Unable to find version string.")


setup(
    name='django-fluent-blogs',
    version=find_version('fluent_blogs', '__init__.py'),
    license='Apache License, Version 2.0',

    install_requires=[
        'django-fluent-contents>=1.0c3',
        'django-fluent-utils>=1.1.1',      # DRY utility code
        'django-categories>=1.0.0',
        'django-tag-parser>=1.1',
        'django-parler>=1.0',
    ],
    requires=[
        'Django (>=1.4)',
    ],
    extras_require = {
        'taggit': ['taggit', 'taggit-autosuggest'],
        'blogpage': ['django-fluent-pages>=0.9b4'],
    },
    description='A blog engine with flexible block contents (based on django-fluent-contents).',
    long_description=read('README.rst'),

    author='Diederik van der Boor',
    author_email='opensource@edoburu.nl',

    url='https://github.com/edoburu/django-fluent-blogs',
    download_url='https://github.com/edoburu/django-fluent-blogs/zipball/master',

    packages=find_packages(),
    include_package_data=True,

    zip_safe=False,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
