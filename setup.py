from distutils.core import setup

with open('requirements.txt') as req_fp:
    requirements = req_fp.read().split('\n')

setup(
    name='jpp',
    version='0.0.2',
    packages=['jpp'],
    url='https://github.com/asherbar/json-plus-plus/archive/0.0.2.tar.gz',
    license='MIT',
    author='asherbar',
    author_email='asherbare@gmail.com',
    description='An extension of JSON with an emphasis on reusability',
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'jpp=jpp.cli:main',
        ],
    },
)
