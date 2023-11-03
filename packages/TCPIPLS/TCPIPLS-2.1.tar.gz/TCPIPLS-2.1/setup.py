from setuptools import setup, find_packages

setup(
    name='TCPIPLS',
    version='2.1',
    description='Python connect to PLC LS',
    long_description_content_type="text/markdown",
    long_description =open('README.md').read(),
    author='Quangcha',
    author_email='duyquangd4.bk@gmail.com',
    packages=find_packages(exclude=['docs', 'example']),
    keywords=['PLC', 'protocol', 'LS electric'],
)
