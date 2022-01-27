from codecs import open
from setuptools import setup
import re


with open('src/agstoolbox/__init__.py', 'r') as fd:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
                        fd.read(), re.MULTILINE).group(1)

setup(
    name='agstoolbox',
    version=version,
    description='A Toolbox for managing AGS Editor versions.',
    url='https://github.com/ericoporto/agstoolbox',
    download_url='https://github.com/ericoporto/agstoolbox/tarball/' + version,
    author='erico',
    author_email='eri0onpm@gmail.com',
    license='MIT',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License'
    ],
    keywords='AGS Toolbox',
    install_requires=['pyqt6', 'requests', 'defusedxml', 'platformdirs'],
    packages=["agstoolbox"],
    package_dir={"": "src"},
    scripts=["agstoolbox", "atbx"],
    package_data={
        'agstoolbox': ['data/*.png']
    },
)
