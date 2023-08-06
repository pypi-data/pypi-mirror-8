#!/usr/bin/env python

from setuptools import setup, find_packages

try:
    long_description = open('README.md', 'rt').read()
except IOError:
    long_description = ''

setup(
    name='openlmi-scripts-storage',
    version='0.4.0',
    description='LMI command for system storage administration.',
    long_description=long_description,
    author='Jan Safranek',
    author_email='jsafrane@redhat.com',
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
    packages=[
        'lmi',
        'lmi.scripts',
        'lmi.scripts.storage',
        'lmi.scripts.storage.cmd',
    ],
    include_package_data=True,

    entry_points={
        'lmi.scripts.cmd': [
            'storage = lmi.scripts.storage.storage_cmd:Storage',
            ],
        },
    )
