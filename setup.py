from os import path
from setuptools import setup


# read the contents of your README file
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='football-data-connector',
    version='0.9.1',
    url='https://github.com/tony-joseph/football-data-connector',
    license='BSD',
    author='Tony Joseph',
    author_email='tony@tonyj.me',
    description='Python package to connect to football-data.org API',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=['footballdata'],
    include_package_data=True,
    install_requires=[
        'python-dateutil>=2.7.5',
        'requests>=2.20.0',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries',
    ]
)
