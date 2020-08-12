import setuptools
from pathlib import Path

# Read the contents of README file
source_root = Path(".")
with (source_root / "README.md").open(encoding="utf-8") as f:
    long_description = f.read()

# Read the requirements
with (source_root / "requirements.txt").open(encoding="utf8") as f:
    requirements = f.readlines()

setuptools.setup(
    name='fds_profiling',  
    version='0.1',
    author="Harsh Singhal",
    description="Generate profile report",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=requirements,
    packages=setuptools.find_packages("src"),
    package_dir={"": "src"},
    
    include_package_data=True,
    
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
     ],
 )
