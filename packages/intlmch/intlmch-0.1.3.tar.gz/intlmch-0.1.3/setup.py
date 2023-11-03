from setuptools import setup, find_packages
with open('README.md',"r") as fh:
    description = fh.read() 

setup(
    name='intlmch',
    version='0.1.3',
    packages=find_packages(exclude=['intlmch']),
    description='library ML',
    long_description=description,
    long_description_content_type="text/markdown",
    author='M Luciano', 
    license='MIT',
    install_requires=["numpy","matplotlib","scipy"],
    python_requires='>=3.10.12',
    author_email='luciano.munoz1@udea.edu.co'
    #url = ''
)

    
