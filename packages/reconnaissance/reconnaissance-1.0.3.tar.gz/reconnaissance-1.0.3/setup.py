from setuptools import setup, find_packages

VERSION = '1.0.3'
DESCRIPTION = 'NexProbe is a Python script designed for conducting comprehensive cyber security reconnaissance activities.'

# Setting up
setup(
    name="reconnaissance",
    version="1.0.3",
    author="Pritam Dash",
    author_email="pritamdash1997@gmail.com",
    description="NexProbe is a Python script designed for conducting comprehensive cyber security reconnaissance activities.",
    packages=find_packages(),
    install_requires=[],  # add any additional packages that
    # needs to be installed along with your package. Eg: 'caer'

    keywords=['python', 'NexProbe'],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ]
)