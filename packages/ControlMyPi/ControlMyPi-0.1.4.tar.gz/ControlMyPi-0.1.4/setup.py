from setuptools import setup

setup(
    name='ControlMyPi',
    version='0.1.4',
    author='Jeremy Blythe',
    author_email='jerbly@controlmypi.com',
    packages=['controlmypi'],
    url='http://www.controlmypi.com/',
    license='LICENSE.txt',
    description='Client library for ControlMyPi scripts.',
    install_requires=[
        "sleekxmpp>=1.1.11",
         "dnspython>=1.10.0",
         "pyasn1>=0.1.5",
         "pyasn1_modules>=0.0.4"
    ],
    long_description=open('README.txt').read(),
)