from setuptools import setup, find_packages

# read the contents of your README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()


setup(
    name="tesppypi",
    version="1.0.2",
    author="Mihaly",
    author_email="ormraat.pte@gmail.com",
    description="A package working with financial data",
    url="https://github.com/misrori/goldhand",
    license="MIT",
    install_requires=[],
    packages=find_packages(),
    # other arguments omitted
    long_description=long_description,
    long_description_content_type='text/markdown'

)

