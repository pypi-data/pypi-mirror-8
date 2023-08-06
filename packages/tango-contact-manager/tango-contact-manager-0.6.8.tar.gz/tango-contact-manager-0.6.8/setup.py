# -*- coding: utf-8 -*-
from distutils.core import setup
from setuptools import find_packages

setup(
    name='tango-contact-manager',
    version='0.6.8',
    author=u'Tim Baxter',
    author_email='mail.baxter@gmail.com',
    url='https://github.com/tBaxter/tango-contact-manager',
    license='LICENSE',
    description="""Provides contact forms and any other user submission form you might want.
        Create user submission forms on the fly, straight from the Django admin.
        """,
    long_description=open('README.md').read(),
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True
)
