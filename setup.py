import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="paramak",
    version="0.2.5",
    author="The Paramak Development Team",
    author_email="mail@jshimwell.com",
    description="Create 3D fusion reactor CAD models based on input parameters",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ukaea/paramak",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
