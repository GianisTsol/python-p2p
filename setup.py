import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pythonp2p",
    version="1.5",
    author="GianisTsol",
    author_email="giannisetsolakis@gmail.com",
    description="A peer to peer network able to transfer data and files",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/GianisTsol/python-p2p",
    project_urls={
        "Bug Tracker": "https://github.com/GianisTsol/python-p2p/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "pythonp2p"},
    packages=setuptools.find_packages(where="pythonp2p"),
    python_requires=">=3.6",
)
