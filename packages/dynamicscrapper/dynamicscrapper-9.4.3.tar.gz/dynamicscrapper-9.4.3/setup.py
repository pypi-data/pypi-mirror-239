from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='dynamicscrapper',
    version='9.4.3',
    author='Saidi Souhaieb',
    author_email='Saidisouhaieb@takiacademyteam.com',
    description='A package to scrap the web dynamically',
    long_description_content_type='text/markdown',
    long_description=readme,
    packages=find_packages(),
    install_requires=requirements,
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
