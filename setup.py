import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='fds_profiling',  
    version='0.1',
    author="Harsh Singhal",
    description="Generate profile report",
    long_description=long_description,
    long_description_content_type="text/markdown",
    
    packages=setuptools.find_packages(),
    
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
     ],
 )
