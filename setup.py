from codecs import open
from pathlib import Path

from setuptools import setup
import re


with open('src/agstoolbox/__init__.py', 'r') as fd:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
                        fd.read(), re.MULTILINE).group(1)


this_directory = Path(__file__).parent
long_description = (this_directory / "README.rst").read_text()

setup(
    name='agstoolbox',
    version=version,
    description='Utility to help manage Adventure Game Studio Projects and Editors.',
    long_description=long_description,
    url='https://github.com/ericoporto/agstoolbox',
    download_url='https://github.com/ericoporto/agstoolbox/tarball/' + version,
    author='erico',
    author_email='eri0onpm@gmail.com',
    license='MIT',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License'
    ],
    keywords=['AGS Toolbox', 'Adventure Game Studio', 'development', 'ags', 'Game Development',
              'gamedev'],
    install_requires=['pyqt6', 'requests', 'defusedxml', 'platformdirs', 'pefile'],
    packages=["agstoolbox"],
    package_dir={"": "src"},
    scripts=["agstoolbox", "atbx"],
    package_data={
        'agstoolbox': ['data/*.png']
    },
)
