from setuptools import setup, find_packages

from doclib.version import __version__
from doclib.cli.main import name, desc

setup(
    name=name,
    version=__version__,
    description=desc,
    license='MIT',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'doclib = doclib.cli:main'
        ],
        'doclib_commands': [
            'project = doclib.cli.commands:Project',
            'category = doclib.cli.commands:Category'
            # 'document = doclib.cli.commands:Document'
        ]
    },
    install_requires=[
        'argcomplete'
    ]
)
