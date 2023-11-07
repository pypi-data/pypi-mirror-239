from setuptools import find_packages, setup

with open("README.md","r") as fh:
    description_l=fh.read()

setup(
    name="fbMonteCarlo",
    version='0.1.0',
    packages=find_packages(include=["fabianMontecarlo"]),  #nombre con el que vamos a importar la librería, es el nombre de la carpeta donde está contenido el __init__.py
    description="libreria-integral-montecarlo",
    long_description=description_l,
    long_description_content_type="text/markdown",
    author="Fabian",
    license="MIT",
    install_requires=["numpy==1.26.1","scipy==1.11.3","matplotlib==3.8.1"],
    python_requires=">=3.10.12",
    author_email="fyamith.tovar@udea.edu.co"
)