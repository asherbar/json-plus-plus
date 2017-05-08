import os
from distutils.core import setup

VERSION = '0.0.2.3'

CURR_DIR = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(CURR_DIR, '__version__.py'), 'w') as version_fp:
    version_fp.write('__version__ = {}\n'.format(VERSION))


setup(
    name='jpp',
    version=VERSION,
    packages=['jpp', 'jpp.parser'],
    url='https://github.com/asherbar/json-plus-plus/archive/{}.tar.gz'.format(VERSION),
    license='MIT',
    author='asherbar',
    author_email='asherbare@gmail.com',
    description='An extension of JSON with an emphasis on reusability',
    install_requires=['ply'],
    entry_points={
        'console_scripts': [
            'jpp=jpp.cli:main',
        ],
    },
)
