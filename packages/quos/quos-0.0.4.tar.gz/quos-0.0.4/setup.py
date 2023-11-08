import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="quos",
    version="0.0.4",
    author="Lalit Patel",
    author_email="llsr@att.net",
    description="Quos package for simulating quantum computing based on oscillatory quota",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lapyl/quos",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        'matplotlib',
        'networkx',
    ],
    package_data = {
        "quos": ["icons/**/*", "iconx/**/*"],
    },
)