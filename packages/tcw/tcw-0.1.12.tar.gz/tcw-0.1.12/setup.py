from setuptools import setup, find_packages

with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(
    name='tcw',
    version='0.1.12',
    author='J Leary',
    author_email='tinycontestwinners@gmail.com',
    description='tiny contest winners application',
    long_description=long_description,
    long_description_content_type='text/markdown',
    include_package_data=True,
    packages=find_packages(),
    package_data = {
        '': ['*.html'],
    },
    install_requires=[
        'flask==2.3.3',
        'flask-wtf==1.2.1',
        'sqlalchemy==1.4.50',
        'markdown',
    ],
)
