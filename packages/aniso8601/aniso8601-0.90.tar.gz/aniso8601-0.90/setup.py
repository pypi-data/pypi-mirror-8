import sys

try:
    from setuptools import setup
except ImportError:
    from distutils import setup

if sys.version_info[0] == 2:
    base_dir = 'python2'
elif sys.version_info[0] == 3:
    base_dir = 'python3'

readme = open('README.rst', 'r')
README_TEXT = readme.read()
readme.close()

setup(
    name='aniso8601',
    version='0.90',
    description='A library for parsing ISO 8601 strings.',
    long_description=README_TEXT,
    author='Brandon Nielsen',
    author_email='nielsenb@jetfuse.net',
    url='https://bitbucket.org/nielsenb/aniso8601',
    packages=['aniso8601'],
    package_dir={
        'aniso8601' : base_dir + '/aniso8601',
    },
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
