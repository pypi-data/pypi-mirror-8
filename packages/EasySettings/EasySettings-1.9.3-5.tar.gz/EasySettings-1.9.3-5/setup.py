#!/usr/bin/env python
'''
EasySettings Setup

@author: Christopher Welborn
'''

from distutils.core import setup
defaultdesc = 'Easily set and retrieve application settings.'
try:
    import pypandoc
except ImportError:
    print('Pypandoc not installed, using default description.')
    longdesc = defaultdesc
else:
    # Convert using pypandoc.
    try:
        longdesc = pypandoc.convert('README.md', 'rst')
    except EnvironmentError:
        # Fallback to README.txt (may be behind on updates.)
        try:
            with open('README.txt') as f:
                longdesc = f.read()
        except EnvironmentError:
            print('\nREADME.md and README.txt failed!')
            longdesc = defaultdesc


setup(
    name='EasySettings',
    version='1.9.3-5',
    author='Christopher Welborn',
    author_email='cj@welbornprod.com',
    packages=['easysettings'],
    url='http://pypi.python.org/pypi/EasySettings/',
    license='LICENSE.txt',
    description=open('DESC.txt').read(),
    long_description=longdesc,
    keywords=('python module library 2 3 settings easy '
              'config setting configuration applications app'),
    classifiers=[
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
)
