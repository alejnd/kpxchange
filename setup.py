from setuptools import setup, find_packages

setup(
    name='kpx',
    version='1.0',
    author ="Alejandro Murciano",
    author_email='alejnd@gmail.com',
    url='https://github.com/alejnd/kpxechange',
    long_description=__doc__,
    packages=find_packages(),
    py_modules=['run','config'],
    install_requires=['flask'],
    zip_safe=False,
)
