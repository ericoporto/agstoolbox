from codecs import open
from pathlib import Path

from setuptools import setup, find_packages
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
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3 :: Only'
    ],
    keywords=[
        'AGS Toolbox', 'Adventure Game Studio', 'development', 'ags', 'Game Development', 'gamedev'
    ],
    python_requires='>=3.8',
    install_requires=[
        'pyqt6',
        'requests',
        'defusedxml',
        'platformdirs',
        'pefile',
        'shtab'
    ],
    packages=[
        'agstoolbox',
        'agstoolbox.core',
        'agstoolbox.core.ags',
        'agstoolbox.core.cmdline',
        'agstoolbox.core.gh',
        'agstoolbox.core.settings',
        'agstoolbox.core.utils',
        'agstoolbox.core.version',
        'agstoolbox.panels',
        'agstoolbox.system',
        'agstoolbox.wdgts',
        'agstoolbox.wdgts_utils'
    ],
    package_dir={"": "src"},
    scripts=["agstoolbox", "atbx"],
    package_data={
        'agstoolbox': ['data/*.png', 'data/fonts/*.ttf']
    },
)
