from setuptools import setup, find_packages

setup(
    name='AVOlibraryCP',
    version='0.2',
    author='Alejandro Valencia',
    author_email='alejandro.valenciao1@udea.edu.co',
    description='Solve integral using the montecarlo method',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'requests',
    ],
)
