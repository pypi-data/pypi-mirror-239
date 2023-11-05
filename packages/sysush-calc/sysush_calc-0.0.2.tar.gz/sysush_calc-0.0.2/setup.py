import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sysush_calc",
    version="0.0.2",
    author="zhouyang",
    author_email="",
    description="A demo for up load python library to pypi",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/zhouyang209117/sysush_calc",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    )
)