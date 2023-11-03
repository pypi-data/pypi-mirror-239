from setuptools import setup, find_packages

setup(
    name="kwslogger",
    version="0.1.1",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=[
        "requests",
        "colorama",
        "pytz",
    ],
    author="kWAY",
    author_email="admin@kwayservices.top",
    description="This is my own logging library!",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/kWAYTV/kwslogger",
)
