from setuptools import find_packages, setup

with open('./README.md','r') as fn:
    description_1 = fn.read()

setup(
    name='Bono2FdoJar',
    version='0.1.0',
    packages=find_packages(include=['Bono2FdoJar']),
    description='Liberia para calcular integrales con el método de Montecarlo y suavizar curvas con usando un kernel gaussiano',
    long_description=description_1,
    long_description_content_type = 'text/markdown',
    author='Fernando Jaramillo',
    license= 'MIT',
    install_requirements=["numpy","matplolib"],
    python_requirements='3.11.6',
    author_email='juanf.jaramillo@udea.edu.co',
    url='https://gitlab.com/juanf.jaramillo1/curso-fci-2023-2.git'
    
)