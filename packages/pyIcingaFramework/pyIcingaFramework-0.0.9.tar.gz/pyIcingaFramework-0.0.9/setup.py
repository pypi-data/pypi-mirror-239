from setuptools import setup, find_packages


setup(
    name='pyIcingaFramework',
    description='Icinga2 Check Framework library',
    long_description='# Icinga2 Check Framework',
    version='0.0.9',
    author='Paul Denning',
    include_package_data=True,
    packages=find_packages(exclude=['tests', 'tests.*']),
    install_requires=[],
    keywords=['icinga2', 'nagios'],
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
    ],

    entry_points={'console_scripts': ['pyIcingaCheck=pyIcingaFramework.ic2check:apicli',
                                      'pyIcingaChecksnmp=pyIcingaFramework.ic2check:snmpcli']}
)
