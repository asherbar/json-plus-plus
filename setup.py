from distutils.core import setup

VERSION = '0.0.1'


setup(
    name='jpp',
    version=VERSION,
    packages=['jpp', 'jpp.parser', 'jpp.cli_test'],
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
