from setuptools import find_packages, setup

PACKAGE_NAME = "pforacle"

setup(
    name="pforacle",
    version="0.0.6",
    description="This package contains prompt flow tools for querying Oracle databases.",
    packages=find_packages(),
    install_requires=[
        'oracledb'
    ],
    entry_points={
        "package_tools": ["query = oracle.tools.utils:list_package_tools"],
    },
    include_package_data=True,   # This line tells setuptools to include files from MANIFEST.in
)