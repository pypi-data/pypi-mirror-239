from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

# with open('requirements.txt') as f:
#     requirements = f.read().splitlines()

setup(
    name='dynamicscrapper',
    version='10.0.3',
    author='Saidi Souhaieb',
    author_email='Saidisouhaieb@takiacademyteam.com',
    description='A package to scrap the web dynamically',
    long_description_content_type='text/markdown',
    long_description=readme,
    packages=find_packages(),
    install_requires=["attrs==23.1.0",
                      "certifi==2023.7.22",
                      "click==8.1.7",
                      "h11==0.14.0",
                      "idna==3.4",
                      "outcome==1.3.0.post0",
                      "PySocks==1.7.1",
                      "selenium==4.15.1",
                      "sniffio==1.3.0",
                      "sortedcontainers==2.4.0",
                      "trio==0.23.0",
                      "trio-websocket==0.11.1",
                      "urllib3==2.0.7",
                      "wsproto==1.2.0"
                      ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)


# install_requires=[
#         'PyYAML',
#         'pandas==0.23.3',
#         'numpy>=1.14.5',
#         'matplotlib>=2.2.0,,
#         'jupyter'
#     ]
