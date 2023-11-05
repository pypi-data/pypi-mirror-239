import io
import os
from setuptools import find_packages, setup
import middel


def read(*paths, **kwargs):
    content = ""
    with io.open(
            os.path.join(os.path.dirname(__file__), *paths),
            encoding=kwargs.get("encoding", "utf8"),
    ) as open_file:
        content = open_file.read().strip()
    return content


setup(
    name="middel",
    version=middel.__version__,
    description="Middle/Modern English Translator CLI - Written in Python.",
    url="https://github.com/johnnystarr/middel",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    author="Johnny Starr",
    packages=find_packages(exclude=["tests", ".github"]),
    install_requires=[

    ],
    entry_points={
        'console_scripts': [
            'middel = middel:cli',
        ],
    },
)
