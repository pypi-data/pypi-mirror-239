
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="agmap",                     
    version="0.0.1",                        
    author="Gautam Datla",                     
    description="Audible ASIN to goodreads mapping ",
    long_description=long_description,      
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),    
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],                                      
    python_requires='>=3.6',                
    py_modules=["agmap"],             
    package_dir={'':'src'},    
    install_requires=[]                 
)