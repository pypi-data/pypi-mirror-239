from io import open
from setuptools import setup
from pathlib import Path
from typing import List


"""
:authors: Elisha Flacon
:license: BSD 3-Clause License, see LICENSE file
:copyright: (c) 2023 Elisha Flacon
"""


VERSION = '0.0.2'

HERE = Path(__file__).parent.resolve()

NAME = 'reepsy'

AUTHOR = 'Elisha Flacon'
DESCRIPTION = 'Reepsy - simple library which solves classification pictures problem with machine learning'
LONG_DESCRIPTION = Path(HERE, 'README.md').read_text(encoding='utf-8')

URL = 'https://github.com/ElishaFlacon/reepsy'
DOWNLOAD_URL = 'https://github.com/ElishaFlacon/reepsy/archive/main.zip'

REQUIRES_PYTHON = '>=3.8'
LICENSE = 'BSD 3-Clause'


# def _readlines(*names: str, **kwargs) -> List[str]:
#     encoding = kwargs.get('encoding', 'utf-8')
#     lines = Path(__file__).parent.joinpath(*names).read_text(encoding=encoding).splitlines()
#     return list(map(str.strip, lines))


# def _extract_requirements(file_name: str):
#     return [line for line in _readlines(file_name) if line and not line.startswith('#')]


# def _get_requirements(req_name: str):
#     requirements = _extract_requirements(req_name)
#     return requirements


setup(
    name=NAME,
    version=VERSION,
    author=AUTHOR,

    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',

    url=URL,
    download_url=DOWNLOAD_URL,

    python_requires=REQUIRES_PYTHON,

    license=LICENSE,

    packages=['reepsy'],
    include_package_data=True,
    install_requires=['torch', 'torchvision', 'torchaudio'],

    classifiers=[
        'License :: OSI Approved :: BSD License',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ]
)
