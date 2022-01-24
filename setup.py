from setuptools import setup
from codecs import open
from os import path


setup(
    name='agstoolbox',
    version='0.1.0',
    description='A Toolbox for managing AGS Editor versions.',
    author='erico',
    author_email='eri0onpm@gmail.com',
    license='MIT',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License'
    ],
    keywords='AGS Toolbox',
    install_requires=['pyqt6'],
    packages=["agstoolbox"],
    package_dir={"": "src"},
    scripts=["agstoolbox"]
)
