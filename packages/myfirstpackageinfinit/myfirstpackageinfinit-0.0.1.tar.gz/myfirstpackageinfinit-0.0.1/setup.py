from setuptools import find_packages, setup

setup(
    name='myfirstpackageinfinit',
    packages=find_packages(),
    version='0.0.1',
    description='Azure Python library',
    author='Infinity Team',
    install_requires=[],
    python_requires='>=3.6',  # example version, adjust according to your compatibility
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",  # replace with your License
        "Operating System :: OS Independent",
    ],
    keywords="rabbitmq, messaging, queue, producer, consumer",
)
