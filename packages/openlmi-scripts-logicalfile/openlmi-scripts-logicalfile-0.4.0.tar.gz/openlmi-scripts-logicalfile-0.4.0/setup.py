#!/usr/bin/env python

from setuptools import setup, find_packages

try:
    long_description = open('README.md', 'rt').read()
except IOError:
    long_description = ''

setup(
    name='openlmi-scripts-logicalfile',
    version='0.4.0',
    description='LMI command for system logical file administration.',
    long_description=long_description,
    author='Jan Synacek',
    author_email='jsynacek@redhat.com',
    url='https://github.com/openlmi/openlmi-scripts',
    download_url='https://github.com/openlmi/openlmi-scripts/tarball/master',
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

    namespace_packages=['lmi', 'lmi.scripts' ],
    packages=['lmi', 'lmi.scripts', 'lmi.scripts.logicalfile'],
    include_package_data=True,

    entry_points={
        'lmi.scripts.cmd': [
            'file = lmi.scripts.logicalfile.lf_cmd:Lf',
            ],
        },
    )
