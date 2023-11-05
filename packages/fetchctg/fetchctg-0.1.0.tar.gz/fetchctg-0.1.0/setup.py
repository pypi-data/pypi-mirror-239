import pathlib
import setuptools
#from setuptools import setup, find_packages

setuptools.setup(
    name='fetchctg',
    version='0.1.0',
    author='Akshay Chougule',
    author_email='akshay6023@gmail.com',
    description='A package that can fetch formatted adverse events data from clinicaltrials.gov',
    long_description=pathlib.Path("README.md").read_text(),
    long_description_content_type="text/markdown",
    python_requires=">=3.6",
    license='GPL',
    project_urls={
        "source":"https://github.com/AksChougule/ctg-fetch",
        },
    classifiers=[
            "Intended Audience :: Science/Research",
            "Development Status :: 3 - Alpha",
            "Operating System :: OS Independent",
            "Programming Language :: Python :: 3.7",
            "Programming Language :: Python :: 3.8",
            "Programming Language :: Python :: 3.9",
            "Programming Language :: Python :: 3.10"
        ],
    install_requires=["pandas","numpy","requests","datetime"],
    packages=setuptools.find_packages(),
    include_package_data=True,
)
