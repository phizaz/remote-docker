from __future__ import print_function
from setuptools import setup
from os.path import join, dirname
import re


def get_version_from(file):
    version = re.search(
        '^__version__\s*=\s*\'(.*)\'',
        open(file).read(),
        re.M
    ).group(1)
    return version


version = get_version_from(join(dirname(__file__), 'src', 'remotedocker.py'))

setup(
    name='remote-docker',
    packages=['src', 'src.actions', 'src.actions.lib', 'src.lib'],
    include_package_data=True,
    install_requires=[
        'future',
        'pyyaml',
        'arrow',
        'tabulate',
        'capturer',
        'ptyprocess',
    ],
    entry_points={
        "console_scripts": [
            'remotedocker = src.remotedocker:main',
            'rdocker = src.remotedocker:main',
        ]
    },
    version=version,
    description='Run your script in a docker on another machine as if it were on yours',
    author='Konpat Preechakul',
    author_email='the.akita.ta@gmail.com',
    url='https://github.com/phizaz/remote-docker',  # use the URL to the github repo
    keywords=['remote', 'utility'],  # arbitrary keywords
    classifiers=[],
)
