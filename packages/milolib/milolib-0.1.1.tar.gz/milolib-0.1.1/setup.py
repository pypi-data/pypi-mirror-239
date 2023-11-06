from setuptools import setup, find_packages

with open("README.md","r") as fh:
    description_l = fh.read()

setup(
    name='milolib',
    version='0.1.1',
    packages=find_packages(include=['milolib']),
    description='Libreria de suma',
    long_description=description_l,
    long_description_content_type="text/markdown",
    author='Milo',
    license='MIT',
    install_requires=["numpy==1.26.1"],
    python_requires='>=3.10.12',
    author_email = "camilo.londonov@udea.edu.co",
    url = "https://gitlab.com/camilo.londonov"

)