from setuptools import setup, find_packages

with open('README.md', 'r') as fh:
    description_l = fh.read()
setup(
    name='salopylib',
    version='0.2.0',
    packages=find_packages(include=['salopylib']),
    description='libreria de integracion por montecarlo y ajuste de datos',
    long_description=description_l,
    long_description_content_type='text/markdown',
    author='Salo <3',
    license='MIT',
    install_requires=['numpy==1.26.1','matplotlib==3.8.1','pandas==2.1.2','sympy==1.12'],
    python_requires='>=3.11.2',
    author_email='salome.osoriom@udea.edu.co',
    url='https://www.instagram.com/salo_mei343/'
)
