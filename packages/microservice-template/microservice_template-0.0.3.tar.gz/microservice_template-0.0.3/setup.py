from setuptools import setup, find_packages

VERSION = '0.0.3'
DESCRIPTION = 'Microservicetemplate'
LONG_DESCRIPTION = 'Template for Simple Flask Microservices'

# Setting up
setup(
    name="microservice_template",
    version=VERSION,
    author="Pixelfehler",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
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