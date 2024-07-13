from setuptools import setup, find_packages

setup(
    name='pyls',
    version='1.0',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'pyls = pyls:main'
        ]
    },
    python_requires='>=3.6',
)
