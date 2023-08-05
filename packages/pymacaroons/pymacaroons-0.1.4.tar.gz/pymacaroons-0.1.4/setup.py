import os

from setuptools import find_packages, setup


version = __import__('macaroons').__version__


def read_file(*paths):
    here = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(here, *paths)) as f:
        return f.read()

# Get long_description from index.rst:
long_description = read_file('docs', 'index.rst')
long_description = long_description.strip().split('split here', 1)[0]

setup(
    name='pymacaroons',
    version=version,
    description='Macaroon library for Python',
    author='Evan Cordell',
    author_email='evan.cordell@localmed.com',
    url='',
    license='MIT',
    packages=find_packages(exclude=['tests', 'tests.*']),
    include_package_data=True,
    long_description=long_description,
    install_requires=[
        'six>=1.7.3',
        'libnacl>=1.3.5',
        'streql>=3.0.2',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Security :: Cryptography',
        'Topic :: Security'
    ],
)
