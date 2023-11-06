from setuptools import setup, find_packages

VERSION = '0.0.6'
DESCRIPTION = 'Microservicetemplate'

from pathlib import Path
this_directory = Path(__file__).parent
LONG_DESCRIPTION = (this_directory / "README.md").read_text()

# Setting up
setup(
    name="microservice_template",
    version=VERSION,
    author="Pixelfehler",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    packages=["microservice_template"],
    install_requires=['flask', 'flask-cors'],
    keywords=['python', 'microservice'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)