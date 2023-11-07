# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

packages = find_packages()
print(packages)

setup(
    name="sign-language-datasets",
    packages=packages,
    version="0.2.0",
    description="TFDS Datasets for sign language",
    author="Amit Moryossef",
    author_email="amitmoryossef@gmail.com",
    url="https://github.com/sign-language-processing/datasets",
    keywords=[],
    install_requires=["typing-extensions", "python-dotenv", "tqdm", "pose-format", "tfds-nightly", "tensorflow",
                      "numpy", "pympi-ling", "Pillow", "opencv-python==4.5.5.64"],
    tests_require=['pytest', 'pytest-cov'],
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3.6",
    ],
    include_package_data=True,
)
