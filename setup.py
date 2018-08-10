from setuptools import setup, find_packages

setup(
    name="testbuilder",
    version="0.2.3",
    packages=find_packages(),
    description="A python testing framework for frontend testing",

    package_data = {
        '': ['*.csv', '*.yaml'],
    },

    install_requires=[
        "click==6.7",
        "PyYAML==3.13",
        "pandas==0.23.3",
        "selenium==3.13.0"
    ],

    project_urls={
        "Source": "https://github.com/AsafSilman/testbuilder",
    },

    classifiers=[
        "Topic :: Software Development :: Testing",
        "Programming Language :: Python :: 3.7"
    ],

    author="Asaf Silman",
    author_email="asaf.silman@health.wa.gov.au"
)

