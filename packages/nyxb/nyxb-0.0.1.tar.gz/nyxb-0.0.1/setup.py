from setuptools import setup, find_packages

setup(
    name='nyxb',
    version='0.0.1',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'nyxb = cli:main',
        ],
    },
    install_requires=[],
)
