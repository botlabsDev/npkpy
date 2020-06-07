#!/usr/bin/env python3.8
import setuptools
from datetime import datetime

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="npkPy",
    version=f"{(datetime.now()).strftime('%Y.%m.%d.%H.%M')}",
    description="npkPy is an unpacker tool for MikroTiks custom npk container format",
    author='botlabsDev',
    author_email='npkPy@botlabs.dev',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/botlabsDev/npkpy",
    packages=setuptools.find_packages(),
    python_requires='>=3.6',
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Operating System :: OS Independent",
    ],
    entry_points={
        'console_scripts': [
            "npkPy=npkpy.main:main",
            # "npkDownloader=npkpy.download:main",
        ],
    },
    install_requires=[
    ],
)
