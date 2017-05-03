from distutils.core import setup


setup(
    name='jpp',
    version='0.0.2.2',
    packages=['jpp', 'jpp.parser'],
    url='https://github.com/asherbar/json-plus-plus/archive/0.0.2.2.tar.gz',
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
