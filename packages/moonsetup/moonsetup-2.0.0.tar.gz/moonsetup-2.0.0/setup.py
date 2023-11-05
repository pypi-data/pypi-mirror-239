from setuptools import setup, find_packages

setup(
    name="moonsetup",
    version="2.0.0",
    author="toxinsfx",
    description="A library to make setup or check version of your program",
    long_description="Check full description on github: https://github.com/toxinsfx/MoonSetup",
    url="https://github.com/toxinsfx/MoonSetup",
    packages=find_packages(),
    install_requires=[
        "requests"
    ]
)
