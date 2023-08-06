#! /usr/bin/env python
# Authors: Olivier Grisel <olivier.grisel@ensta.org>
#          MinRK
# LICENSE: MIT
from setuptools import setup

try:
    # For dogfooding only
    import wheelhouse_uploader.cmd
    cmdclass = vars(wheelhouse_uploader.cmd)
except ImportError:
    cmdclass = {}


setup(
    name="wheelhouse-uploader",
    version="0.7.0",
    description="Upload wheels to any cloud storage supported by Libcloud",
    maintainer="Olivier Grisel",
    maintainer_email="olivier.grisel@ensta.org",
    license="MIT",
    url='http://github.com/ogrisel/wheelhouse-uploader',
    packages=[
        'wheelhouse_uploader',
    ],
    install_requires=[
        "setuptools>=0.9",  # required for PEP 440 version parsing
        "futures",
        "apache-libcloud",
    ],
    classifiers=[
        'License :: OSI Approved',
        'Programming Language :: Python',
        'Topic :: Software Development',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Operating System :: Unix',
        'Operating System :: MacOS',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
     ],
     cmdclass=cmdclass,
)
