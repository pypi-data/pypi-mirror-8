#!/usr/bin/env python

from setuptools import setup, find_packages
import inviter2

setup(
    name='django-inviter2',
    version=inviter2.__version__,
    description='Simple email invitations for your Django app',
    long_description=open('README.rst').read(),
    author='Michael J Schultz',
    author_email='mjschultz@gmail.com',
    url='https://github.com/mjschultz/django-inviter2',
    packages=find_packages(),
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Framework :: Django',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    install_requires=[
        "shortuuid >= 0.1",
        "six",
        "Django >= 1.4",
    ],
    include_package_data=True,
    zip_safe=False,
)
