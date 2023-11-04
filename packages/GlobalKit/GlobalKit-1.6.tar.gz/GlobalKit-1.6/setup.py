from setuptools import setup, find_packages

with open('README.md', 'r') as readme:
    documentation = readme.read()

setup(
    name='GlobalKit',
    packages=find_packages(),
    requires=[],
    include_package_data=True,
    version='1.6',
    author='CrazyFlyKite',
    author_email='karpenkoartem2846@gmail.com',
    url='https://github.com/CrazyFlyKite/GlobalKit/',
    description='Get alphabets from various languages and a set of functions for text manipulation',
    long_description=documentation,
    long_description_content_type='text/markdown'
)
