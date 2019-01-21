#!/usr/bin/env python

from setuptools import setup

setup(
    name='OBL',
    packages=["OBL","OBL.structs","OBL.structs.osm","OBL.structs.wm","OBL.planner"], 
    version='0.1.0', 
    description='Bridge to different OSM functionalities', 
    package_dir={'': '.'},
    author='Lakshadeep Naik',
    author_email='lakshadeep.naik@gmail.com',
    install_requires=['utm','overpass','Pillow','pyyaml']
    )
