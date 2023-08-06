"""
Five One One 
-------------

A python API to consume transit data from http://511.org. 
"""

from setuptools import setup
from pip.req import parse_requirements
 
install_reqs = parse_requirements("requirements.txt")
requirements = [str(ir.req) for ir in install_reqs]
 
setup(
    name='fiveoneone',
    version='0.2',
    license='MIT',
    author='Ramiro Berrelleza',
    author_email='rberrelleza@gmail.com',
    description='A python API to consume transit data from http://511.org.',
    url='https://github.com/rberrelleza/511-transit',
    packages=['fiveoneone'],
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    install_requires=requirements,
    entry_points={
    },
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)