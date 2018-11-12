#!/usr/bin/env python

from setuptools import setup

setup(
    name='osm_bridge', 
    version='0.1.0', 
    description='Bridge to different OSM functionalities', 
    package_dir={'': '.'},
    author='Lakshadeep Naik',
    author_email='lakshadeep.naik@gmail.com',
    install_requires=['utm','overpass>=0.7.0'],
    dependency_links=['git+http://github.com/Lakshadeep/overpass-api-python-wrapper.git#egg=overpass-0.7.0']
    )
