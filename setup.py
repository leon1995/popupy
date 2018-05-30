import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="popupy",
    version="1",
    author="Leon",
    author_email="leon.home@arcor.de",
    description="Get Country Population with an API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/leon1995/popupy",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)