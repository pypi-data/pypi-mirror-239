from setuptools import setup, find_packages
with open('README.md',"r") as fh:
    description = fh.read() 

setup(
    name='testsumm',
    version='0.1.0',
    packages=find_packages(exclude=['testsumm']),
    description='library ML',
    long_description=description,
    long_description_content_type="text/markdown",
    author='Luciano M', 
    license='MIT',
    install_requires=["numpy==1.26.1","pandas==2.1.1"],
    python_requires='>=3.10.12',
    author_email='luciano.munoz1@udea.edu.co'
    #url = ''
)


    
    
