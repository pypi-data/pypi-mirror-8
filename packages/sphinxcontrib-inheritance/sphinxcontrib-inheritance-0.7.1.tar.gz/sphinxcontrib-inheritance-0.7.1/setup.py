# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open('README') as stream:
    long_desc = stream.read()

requires = [
    'path.py',
    'Sphinx>=1.3b1',
    ]

setup(
    name='sphinxcontrib-inheritance',
    version='0.7.1',
    url='https://bitbucket.org/nantic/sphinxcontrib-inheritance',
    download_url='http://pypi.python.org/pypi/sphinxcontrib-inheritance',
    license='BSD',
    author='NaN·tic',
    author_email='info@nan-tic.com',
    description='Documentation inheritance functionality for Sphinx',
    long_description=long_desc,
    zip_safe=False,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Documentation',
        'Topic :: Utilities',
    ],
    platforms='any',
    packages=find_packages(),
    include_package_data=True,
    install_requires=requires,
    namespace_packages=['sphinxcontrib'],
)

