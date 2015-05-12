import os

from setuptools import setup, find_packages

def read(*paths):
    """Build a file path from *paths* and return the contents."""
    with open(os.path.join(*paths), 'r') as f:
        return f.read()

setup(
    name='pem',
    version='0.1.0',
    description='Automatically serve Python scripts through a web interface and REST API.',
    long_description=(read('README.md')),
    url='http://github.com/mosesschwartz/scrypture',
    license='MIT',
    author='Moses Schwartz',
    author_email='mosesschwartz@gmail.com',
    py_modules=['scrypture'],
    include_package_data=True,
    packages=find_packages(exclude=['tests*']),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology'
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Framework :: Flask',
#        'Programming Language :: Python :: 3',
#        'Programming Language :: Python :: 3.3',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
