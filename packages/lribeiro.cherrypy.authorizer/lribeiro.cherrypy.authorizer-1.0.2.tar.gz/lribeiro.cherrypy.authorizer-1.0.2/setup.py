from codecs import open
from os import path
import sys

from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand


class PyTest(TestCommand):
    
    def initialize_options(self):
        TestCommand.initialize_options(self)

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        #import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main('tests/')
        sys.exit(errno)


here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='lribeiro.cherrypy.authorizer',
    version='1.0.2',
    description='Extensible session based authentication and claims based authorization tool for CherryPy',
    long_description=long_description,
    url='http://bitbucket.org/livioribeiro/cherrypy-authorizer',
    author='Livio Ribeiro',
    author_email='livioribeiro@outlook.com',
    license='BSD License',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: CherryPy',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Internet :: WWW/HTTP :: Session',
    ],
    keywords=['authentication', 'authorization', 'access control', 'cherrypy'],
    packages=find_packages(exclude=['tests']),
    namespace_packages=['lribeiro', 'lribeiro.cherrypy'],
    include_package_data=True,
    install_requires=[
        'CherryPy',
    ],
    tests_require=[
        'pytest',
        'requests'
    ],
    cmdclass={'test': PyTest},
)