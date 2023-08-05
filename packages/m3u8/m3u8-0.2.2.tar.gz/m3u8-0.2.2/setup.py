from os.path import dirname, abspath, join, exists
from setuptools import setup

long_description = None
if exists("README.rst"):
    long_description = open("README.rst").read()

install_reqs = [req for req in open(abspath(join(dirname(__file__), 'requirements.txt')))]

setup(
    name="m3u8",
    author='Globo.com',
    author_email='videos3@corp.globo.com',
    version="0.2.2",
    zip_safe=False,
    include_package_data=True,
    install_requires=install_reqs,
    packages=["m3u8"],
    url="https://github.com/globocom/m3u8",
    description="Python m3u8 parser",
    long_description=long_description
    )
