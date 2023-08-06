import os
from setuptools import setup

def readme(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

def build():
    setup(
        name = "ifttt",
        version = "0.2.1",
        author = "Brian Abelson",
        author_email = "brian@newslynx.org",
        description = "A Pythonic interface for building IFTTT plugins routed over email.",
        license = "MIT",
        keywords = "email, ifttt",
        url = "https://github.com/newslynx/ifttt",
        packages=['ifttt'],
        long_description=readme('README.md'),
        install_requires = ["pytz", "gevent"],
        classifiers=[
            "Development Status :: 3 - Alpha",
            "Topic :: Communications :: Email",
            "License :: OSI Approved :: MIT License",
        ],
    )

if __name__ == '__main__':
    build()