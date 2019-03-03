from distutils.core import setup

readme = open('README.md').read()

setup(
    name='panek_db',
    version='1.0.0',
    author='Aleksander Philips',
    author_email='aleksander.philips at gmail.com',
    packages=['panek'],
    url='https://github.com/burchardtist/panek_db',
    license='MIT',
    description='Object Relation Mapper for python objects kept in the memory.',
    long_description=readme,
)
