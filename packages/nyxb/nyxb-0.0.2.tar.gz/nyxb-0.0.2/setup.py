from setuptools import setup, find_packages

setup(
    name='nyxb',
    version='0.0.2',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'nyxb = nyxb_cli.cli:main',
        ],
    },
    install_requires=[],
)
