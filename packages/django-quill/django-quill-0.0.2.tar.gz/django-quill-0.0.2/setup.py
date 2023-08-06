import os
import sys

from setuptools import setup

if sys.argv[-1] == 'publish':
    os.system('make build')
    os.system('python setup.py sdist upload')
    os.system('python setup.py bdist_wheel upload')
    sys.exit()

import quill

with open('README.md', 'r') as readme_file:
    readme = readme_file.read()

os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-quill',
    version=quill.__version__,
    author='Ryan Senkbeil',
    author_email='ryan.senkbeil@gsdesign.com',
    description='Reusable components for the Django admin.',
    long_description=readme,
    packages=['quill'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Internet :: WWW/HTTP',
    ]
)
