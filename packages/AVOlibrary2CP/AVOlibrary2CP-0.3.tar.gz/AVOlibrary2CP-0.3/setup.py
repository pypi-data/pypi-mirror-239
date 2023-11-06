from setuptools import setup, find_packages

setup(
    name='AVOlibrary2CP',
    version='0.3',
    packages=find_packages(),
    description='Curve fitting for COVID-19 data using Gaussian kernel smoother',
    author='Alejandro Valencia',
    author_email='alejandro.valenciao1@udea.edu.co',
    license="MIT",
    install_requires=['numpy','scipy', 'matplotlib'],
)
