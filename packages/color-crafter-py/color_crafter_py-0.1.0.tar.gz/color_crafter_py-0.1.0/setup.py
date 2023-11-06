"""Python setup.py for color_crafter_py package"""
import io
import os
from setuptools import find_packages, setup


def read(*paths, **kwargs):
    """Read the contents of a text file safely.
    >>> read("color_crafter_py", "VERSION")
    '0.1.0'
    >>> read("README.md")
    ...
    """

    content = ""
    with io.open(
        os.path.join(os.path.dirname(__file__), *paths),
        encoding=kwargs.get("encoding", "utf8"),
    ) as open_file:
        content = open_file.read().strip()
    return content


def read_requirements(path):
    return [
        line.strip()
        for line in read(path).split("\n")
        if not line.startswith(('"', "#", "-", "git+"))
    ]


setup(
    name="color_crafter_py",
    version=read("color_crafter_py", "VERSION"),
    description="A powerful and easy-to-use Python library for adding colors and styles to text printed on your terminal. Can be used with custom RGB colors. Created by WernerLuiz92",
    url="https://github.com/WernerLuiz92/color_crafter_py/",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    author="WernerLuiz92",
    packages=find_packages(exclude=["tests", ".github"]),
    install_requires=read_requirements("requirements.txt"),
    entry_points={
        "console_scripts": ["color_crafter_py = color_crafter_py.__main__:main"]
    },
    extras_require={"test": read_requirements("requirements-test.txt")},
)
