from setuptools import setup, find_packages

setup(
    name="TestBuilder",
    version="0.1",
    packages=find_packages(),

    install_requires=[
        "click==6.7",
        "PyYAML==3.13",
        "pandas==0.23.3"
    ],

    author="Asaf Silman",
    author_email="asaf.silman@health.wa.gov.au"
)
