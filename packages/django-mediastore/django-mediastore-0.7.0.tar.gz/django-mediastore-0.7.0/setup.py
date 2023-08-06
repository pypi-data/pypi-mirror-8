#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages


class UltraMagicString(object):
    '''
    Taken from
    http://stackoverflow.com/questions/1162338/whats-the-right-way-to-use-unicode-metadata-in-setup-py
    '''

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return self.value

    def __unicode__(self):
        return self.value.decode('UTF-8')

    def __add__(self, other):
        return UltraMagicString(self.value + str(other))

    def split(self, *args, **kw):
        return self.value.split(*args, **kw)


long_description = UltraMagicString(u'\n\n'.join((
    file('README.rst').read(),
    file('CHANGES.rst').read(),
)))

packages = find_packages('.')
packages = [p for p in packages if p.startswith('mediastore.')]
packages = ['mediastore'] + packages

setup(
    name = 'django-mediastore',
    version = '0.7.0',
    url = 'https://bitbucket.org/gregmuellegger/django-mediastore',
    license = 'BSD',
    description = '',
    long_description = long_description,
    author = UltraMagicString('Gregor Müllegger'),
    author_email = 'gregor@muellegger.de',
    classifiers=(
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ),
    packages = packages,
    include_package_data = True,
    zip_safe = False,
    install_requires = [
        'setuptools',
        'django-sortedm2m',
        'django-taggit',
        'django-templatequery',
    ],
    tests_require = [],
    test_suite = 'runtests.runtests',
)
