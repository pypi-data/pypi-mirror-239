from setuptools import setup, find_packages


setup(
    name='pyIcingaAPIChecks',
    description='Icinga2 Check API Checks for pyIcingaFramework',
    long_description="# Icinga2 Check API Checks for pyIcingaFramework",
    version='0.0.5',
    author='Paul Denning',
    include_package_data=True,
    packages=find_packages(exclude=['tests', 'tests.*']),
    install_requires=[
        "pyIcingaFramework",
    ],
    keywords=['icinga2', 'nagios'],
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
    ],
)