#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from setuptools import setup

try:
    long_description = open('README.md', 'rt').read()
except IOError:
    long_description = ''

setup(
    name='openlmi-scripts-realmd',
    version='0.4.0',
    description='This command allows for basic management of the system Active Directory or Kerberos domain membership.',
    long_description=long_description,
    author=u'Tomas Smetana',
    author_email='tsmetana@redhat.com',
    url='https://github.com/openlmi/openlmi-realmd',
    download_url='https://github.com/openlmi/openlmi-realmd/tarball/master',
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
    packages=['lmi', 'lmi.scripts', 'lmi.scripts.realmd'],
    include_package_data=True,

    entry_points={
        'lmi.scripts.cmd': [
            'realmd = lmi.scripts.realmd.cmd:Realmd',
            ],
        },
    )
