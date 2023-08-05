import os
from setuptools import setup

def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

setup(
    name="geogig-py",
    version="1.0",
    install_requires=['py4j>=0.8', 'requests>=2.2.1'],
    author="Victor Olaya",
    author_email="volaya@boundlessgeo.com",
    description="Python bindings for GeoGig",    
    long_description=(read('README')),
    # Full list of classifiers can be found at:
    # http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 4 - Beta',
    ],
    license="BSD",
    keywords="geogig",
    url='https://github.com/boundlessgeo/geogig-py',
    package_dir={'': 'src'},
    test_suite='test.suite',
    packages=['geogigpy',]
)
