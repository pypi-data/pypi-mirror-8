# -*- encoding:utf-8 -*-
from setuptools import setup, find_packages

setup(
    name='pass-manager',
    version='1.2.0',
    author='petitviolet',
    author_email='violethero0820@gmail.com',
    packages=find_packages(),
    description = 'Simple CLI Password Manager',
    long_description = 'Please show help (pass-manager -h)',
    url = 'https://github.com/petitviolet/pass-manager',
    license = 'MIT',
    # scripts = ['src/pass_manager.py'],
    platforms = ['Mac OS X'],
    # platforms = ['POSIX', 'Windows', 'Mac OS X'],
    entry_points={
        'console_scripts': 'pass-manager = src.pass_manager:main'
    },
    zip_safe=False,
    install_requires = ['crypto'],
    classifiers=[
          'Environment :: Console',
          'Intended Audience :: Developers',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          'Topic :: Utilities'
    ]
)
