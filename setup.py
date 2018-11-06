#!/usr/bin/env python

from setuptools import setup

setup(
    name='osm_bridge', 
    version='0.1.0', 
    description='Bridge to different OSM functionalities', 
    package_dir={'': '.'},
    author='Lakshadeep Naik',
    author_email='lakshadeep.naik@gmail.com'
    install_requires=['utm'],
#    dependency_links=['http://github.com/Lakshadeep/overpass-api-python-wrapper/tarball/master#egg=overpass-0.6.1']
    )
