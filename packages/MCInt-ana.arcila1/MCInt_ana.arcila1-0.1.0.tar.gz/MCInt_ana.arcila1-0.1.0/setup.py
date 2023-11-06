from setuptools import find_packages, setup

with open('README.md', 'r') as fh:
    description_l= fh.read()

setup(
    name='MCInt_ana.arcila1',
    version='0.1.0',
    packages=find_packages(include= ['MC_Int']),
    description='libreria de integración con Monte Carlo',
    long_description=description_l,
    long_description_content_type='text/markdown',
    author='Ana Maria',
    license='MIT',
    install_requires=['numpy==1.26.1', 'matplotlib==3.5.3', 'scipy==1.7.3'],
    python_requires='>=3.9.12',
    author_email='aarcila01@gmail.com',
    git= 'https://gitlab.com/ana.arcila1/cursofci-2023-2.git'

)