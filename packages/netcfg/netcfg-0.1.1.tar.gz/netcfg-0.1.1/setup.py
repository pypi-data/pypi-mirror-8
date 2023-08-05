#!/usr/bin/env python

import os

from setuptools import setup, find_packages

VERSION = '0.1.1'

if __name__ == '__main__':
    setup(
        name='netcfg',
        version=VERSION,
        description="Network configuration of Docker containers.",
        long_description=open(os.path.join(os.path.dirname(__file__), 'README.rst')).read(),
        author='wlan slovenija',
        author_email='open@wlan-si.net',
        url='https://github.com/wlanslovenija/netcfg',
        license='AGPLv3',
        packages=find_packages(exclude=('*.tests', '*.tests.*', 'tests.*', 'tests')),
        package_data={},
        scripts=['scripts/netcfg'],
        classifiers=[
            'Development Status :: 4 - Beta',
            'Intended Audience :: System Administrators',
            'License :: OSI Approved :: GNU Affero General Public License v3',
            'Operating System :: POSIX :: Linux',
            'Programming Language :: Python',
        ],
        include_package_data=True,
        zip_safe=False,
        install_requires=[
            'docker-py>=0.5.0',
            'pyzmq>=14.0.1',
            'ipaddr>=2.1.10',
        ],
    )
