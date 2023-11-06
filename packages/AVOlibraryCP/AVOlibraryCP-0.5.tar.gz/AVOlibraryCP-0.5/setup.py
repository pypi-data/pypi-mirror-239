from setuptools import setup, find_packages

setup(
    name='AVOlibraryCP',
    version='0.5',
    packages=find_packages(),
    description='Solve integral using the montecarlo method',
    author='Alejandro Valencia',
    author_email='alejandro.valenciao1@udea.edu.co',
    license="MIT",
    install_requires=['numpy', 'scipy', 'matplotlib'],
)
