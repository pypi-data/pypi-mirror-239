from setuptools import setup, find_packages

setup(
    name='AVOlibraryCP',
    version='0.1',
    author='Alejandro Valencia',
    author_email='alejandro.valenciao1@udea.edu.co',
    description='Solve integral using the montecarlo method',
    url='https://url_de_tu_libreria.com',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'requests',
        # Agrega aquí todas las dependencias que requiere tu librería
    ],
)
