from setuptools import find_packages, setup


with open("README.md" , "r") as fh:
    description_l = fh.read()
setup(
    name="ebofcis2",
    version="0.1.0",
    packages=find_packages(include=["ebofcis2"]),
    description="Libreria que contiene dos clases\
        Una para realizar integrales por método de montecarlo\
        y otra para realizar un ajuste de curva suavizado\
        con el método de kernel gaussiano",
    long_description=description_l,
    long_description_content_type="text/markdown",
    author=" Emmanuel Botero  ",
    license="MIT",
    install_requires=["sympy==1.12" , "tqdm==4.66.1" ,"numpy==1.26.1" , "pandas==2.1.2" , "matplotlib==3.8.1"],
    python_requires=">=3.10.12",
    author_email="emmanuel.botero@udea.edu.co"

)