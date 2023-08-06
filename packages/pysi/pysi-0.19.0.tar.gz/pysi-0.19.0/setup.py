#!/usr/bin/env python
import os
import sys
from setuptools import setup

VERSION = '0.19.0'
PACKAGE = 'pysi'

if __name__ == '__main__':
    if sys.argv[-1] == 'publish':
        os.system('python setup.py sdist upload')
        sys.exit(1)

    # Compile the list of packages available, because distutils doesn't have
    # an easy way to do this.
    packages, data_files = [], []
    root_dir = os.path.dirname(__file__)
    if root_dir:
        os.chdir(root_dir)

    for dirpath, dirnames, filenames in os.walk(PACKAGE):
        for i, dirname in enumerate(dirnames):
            if dirname in ['.', '..']:
                del dirnames[i]
        if '__init__.py' in filenames:
            pkg = dirpath.replace(os.path.sep, '.')
            if os.path.altsep:
                pkg = pkg.replace(os.path.altsep, '.')
            packages.append(pkg)
        elif filenames:
            prefix = dirpath[len(PACKAGE) + 1:] # Strip package directory + path separator
            for f in filenames:
                data_files.append(os.path.join(prefix, f))


    setup(
        version = VERSION,
        description = 'Fast and simple micro web framework',
        author = 'Imbolc',
        author_email = 'imbolc@imbolc.name',
        url = 'http://bitbucket.org/imbolc/pysi/',
        long_description = open('README.rst').read(),
        name = PACKAGE,
        packages = packages,
        package_data = {'pysi': data_files},
        license = "MIT",
        keywords = "web framework",
        classifiers=[
            'Development Status :: 4 - Beta',
            'Environment :: Web Environment',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: BSD License',
            'Operating System :: OS Independent',
            'Programming Language :: Python',
            'Topic :: Software Development :: Libraries :: Application Frameworks',
            'Topic :: Software Development :: Libraries :: Python Modules',
        ],
        install_requires=['asjson', 'simplejson', 'jinja2'],
    )
