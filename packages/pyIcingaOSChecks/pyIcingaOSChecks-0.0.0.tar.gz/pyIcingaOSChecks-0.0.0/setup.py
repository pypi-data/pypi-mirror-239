from setuptools import setup, find_packages


setup(
    name='pyIcingaOSChecks',
    description='Icinga2 Check OS Checks for pyIcingaFramework',
    long_description='Icinga2 checks for local OS',
    author='Paul Denning',
    include_package_data=True,
    packages=find_packages(exclude=['tests', 'tests.*']),
    install_requires=[
        "pyIcingaFramework",
        "psutil",
    ],
    keywords=['icinga2', 'nagios'],
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
    ],
)