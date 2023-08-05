import sys
import os
import glob
from setuptools import setup

if sys.version_info.major == 3:
    base_dir = 'py3'
else:
    assert sys.version_info.major == 2
    assert sys.version_info.minor >= 7
    base_dir = 'py2'

setup(
    name='asyncoro',
    version='3.0.3',
    description='Python framework for concurrent, distributed, asynchronous network programming with coroutines, asynchronous completions and message passing.',
    long_description=open('README.rst').read(),
    keywords='concurrent, distributed, asynchronous network programming',
    url='http://asyncoro.sourceforge.net',
    package_dir={'':base_dir},
    py_modules=['asyncoro', 'disasyncoro', 'asyncfile', 'discoro'],
    scripts=[os.path.join(base_dir, 'discoro.py')],
    # data_files=[('asyncoro_examples', glob.glob('examples/*.py'))],
    author='Giridhar Pemmasani',
    author_email='pgiri@yahoo.com',
    license='MIT',
    platforms='any',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.1',
        'Topic :: Scientific/Engineering',
        'Topic :: Software Development :: Libraries',
        ]
    )
