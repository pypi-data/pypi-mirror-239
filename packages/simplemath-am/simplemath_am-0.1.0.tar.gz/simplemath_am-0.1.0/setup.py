from setuptools import setup, find_packages

setup(
    name='simplemath_am',
    version='0.1.0',
    author='Aleksa Mihajlovic',
    author_email='mihajlovic.aleksa@gmail.com',
    packages=find_packages(),
    url='http://pypi.python.org/pypi/simplemath/',
    license='LICENSE.txt',
    description='A simple math package',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    install_requires=[
        # Any dependencies, if you have them, go here.
    ],
)
