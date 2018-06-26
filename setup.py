from setuptools import setup


setup(
    name='football-data-connector',
    version='0.9.0',
    url='https://github.com/tony-joseph/football-data-connector',
    license='BSD',
    author='Tony Joseph',
    author_email='tony@tonyj.me',
    description='Python package to connect to football-data.org API',
    packages=['footballdata'],
    include_package_data=True,
    install_requires=[
        'python-dateutil>=2.7.3',
        'requests>=2.19.1',
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
