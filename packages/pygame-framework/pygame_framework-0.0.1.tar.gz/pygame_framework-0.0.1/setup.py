# -*- coding: utf-8 -*


import setuptools

with open("README.md", "r") as fh:
    description = fh.read()

    setuptools.setup(
        name="pygame_framework",
        version="0.0.1",
        author="Petr Koráb",
        author_email="xpetrkorab@gmail.com",
        packages=["pygame_framework"],
        description="something for my project",
        long_description=description,
        long_description_content_type="text/markdown",
        url="https://github.com/PetrKorab/Animated-Word-Cloud-in-Economics",
        python_requires='>=3.8, <3.9',
        license='OSI Approved :: Apache Software License'
    )