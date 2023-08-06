from setuptools import setup

setup(
    name='confluent_client',
    version='1.0',
    author='Jarrod Johnson',
    author_email='jbjohnso@us.ibm.com',
    url='http://xcat.sf.net/',
    packages=['confluent'],
    install_requires=['confluent_common>=0.1.0'],
    scripts=['bin/confetty'],
)
