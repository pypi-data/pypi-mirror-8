#!/usr/bin/env python2
from setuptools import setup

with open('README.rst') as readme:
    long_description = readme.read()


setup(
    name='sstp-server',
    version='0.1.1',
    description='Secure Socket Tunneling Protocol (SSTP) VPN tunel server.',
    author='Sorz',
    author_email='orz@sorz.org',
    url='https://github.com/sorz/sstp-server',
    packages=['sstpd'],
    data_files=[('', ['README.rst'])],
    entry_points="""
    [console_scripts]
    sstpd = sstpd:main
    """,
    install_requires=[
        'twisted', 'service_identity', 'argparse', 'py2-ipaddress'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 2 :: Only',
        'Topic :: Internet',
        'Topic :: Internet :: Proxy Servers',
        'License :: OSI Approved :: MIT License'
    ],
    long_description=long_description
)

