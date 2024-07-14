from setuptools import setup

setup(
    name='pyls',
    version='1.0',
    py_modules=['pyls'],
    entry_points={
        'console_scripts': [
            'pyls=pyls:main',
        ],
    },
    author='Ajay Kumar Ch',
    author_email='ajaykumarch1979@gmail.com',
    description='A simple command line tool',
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    tests_require=['pytest'],
)
