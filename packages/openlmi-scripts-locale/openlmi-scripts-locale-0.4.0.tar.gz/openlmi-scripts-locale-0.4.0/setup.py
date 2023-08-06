#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from setuptools import setup

try:
    long_description = open('README.md', 'rt').read()
except IOError:
    long_description = ''

setup(
    name='openlmi-scripts-locale',
    version='0.4.0',
    description='LMI command for system locale administration.',
    long_description=long_description,
    author=u'Vitezslav Crhonek',
    author_email='vcrhonek@redhat.com',
    url='https://github.com/openlmi/openlmi-locale',
    download_url='https://github.com/openlmi/openlmi-locale/tarball/master',
    platforms=['Any'],
    license="BSD",
    classifiers=[
        'License :: OSI Approved :: BSD License',
        'Operating System :: POSIX :: Linux',
        'Topic :: System :: Systems Administration',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Intended Audience :: Developers',
        'Environment :: Console',
    ],

    install_requires=['openlmi-tools >= 0.9.1'],

    namespace_packages=['lmi', 'lmi.scripts'],
    packages=['lmi', 'lmi.scripts', 'lmi.scripts.locale'],
    include_package_data=True,

    entry_points={
        'lmi.scripts.cmd': [
            # All subcommands of lmi command should go here.
            # See http://pythonhosted.org/openlmi-scripts/script-development.html#writing-setup-py
            'locale = lmi.scripts.locale.cmd:Locale',
            ],
        },
    )
