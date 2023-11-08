from setuptools import find_packages, setup

with open('README.md','r') as fh:
    description_l = fh.read()


setup(
    name = 'GTAlib_MonteCarlo',
    version = '0.1.2',
    packages = find_packages(include = ['GTAlib_MonteCarlo']),
    description='Libreria para calcular la integral definida sobre de un intérvalo de una funcion',
    long_description = description_l,
    long_description_content_type = 'text/markdown',
    author='German',
    license = 'MIT',
    install_requires = ['numpy==1.26.1'],
    python_requires = '>=3.11.6',
    author_email = 'german.torres@udea.edu.co',
    url = 'https://gitlab.com/gtorresa312/trabajos-en-clase.git'
    
)