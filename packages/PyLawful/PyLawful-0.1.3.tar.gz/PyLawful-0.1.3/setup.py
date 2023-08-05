from distutils.core import setup

setup(
    name='PyLawful',
    version='0.1.3',
    author='Mike Leske',
    author_email='mike.leske@gmail.com',
    packages=['PyLawful'],
    url='http://pypi.python.org/pypi/PyLawful/',
    license='LICENSE.txt',
    description='Allow activating SNMP-based LI on routers.',
    long_description=open('README.rst').read(),
    install_requires=[
        "pysnmp >= 4.2.5",
    ],
)