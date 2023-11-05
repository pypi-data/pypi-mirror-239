from setuptools import setup, find_packages

# Long Description 
def read(name):
    with open(name, "r") as fd:
        return fd.read()
    

setup(
        name='bioinfolearn',
        packages = ['bioinfolearn'],
        version='0.1',
        author="Mdslauddin",
        author_email="mdslauddin285@gmail.com",
        description="Bioinformatics Learn",
        long_description=read("README.md"),
        keywords=["computational biology", "Bioinformatics", "Python", "biology tool"],
        
        python_requires='>=3.9',
        install_requires=['riyazi','numpy'],
        
        
        url="",
        download_url = "", 
        license="MIT",
     classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
       
)
 
    