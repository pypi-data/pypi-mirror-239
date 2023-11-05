from setuptools import setup, find_packages

setup(
    name='bcp_in',
    version='0.1',
    packages=find_packages(),
    install_requires=[],
    author='inabeo',
    description='A simple wrapper around the bcp utility, focused on inserting data to the SQL Server db',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/inabeo/bcp_in',
)
