from __future__ import absolute_import, print_function

import sys
from setuptools import setup

python_v = sys.version_info[0:2]

if python_v != (2, 7) and python_v != (3, 4):
    print('This version of Python is unsupported !\nPlease use Python 2.7.x or 3.4.x !')
    sys.exit(1)

name = 'pockyt'
version = '0.5'

setup(
    name=name,
    packages=[name],
    version=version,
    description='automate and manage your pocket collection',
    long_description=open('README.rst').read(),
    author='Arvind Chembarpu',
    author_email='achembarpu@gmail.com',
    url='https://github.com/arvindch/{0}'.format(name),
    license='GPLv3+',
    install_requires=[
        'requests>=2.4',
        'parse>=1.6',
    ],
    download_url='https://github.com/arvindch/{0}/tarball/{1}'.format(name, version),
    keywords=['pocket', 'commandline', 'automation'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Topic :: Utilities',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Natural Language :: English',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
    ],
    entry_points={
        'console_scripts': [
            'pockyt=pockyt.pockyt:main',
        ],
    },
)
