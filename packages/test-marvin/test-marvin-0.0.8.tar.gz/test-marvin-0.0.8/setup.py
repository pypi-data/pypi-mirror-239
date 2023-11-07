import re

import setuptools



def read_file(path):
    with open(path, "r") as handle:
        return handle.read()


def read_version():
    try:
        s = read_file("VERSION")
        m = re.match(r"v(\d+\.\d+\.\d+(-.*)?)", s)
        return m.group(1)
    except FileNotFoundError:
        return "0.0.0"


version = read_version()

setuptools.setup(
    name="test-marvin",
    description="",
    keywords="",
    long_description="""Dummy package""",
    include_package_data=True,
    version=version,
    url="",
    author="Greenhouse AI team",
    author_email="ai@greenhousegroup.com",
    package_dir={"test-marvin": "src/test-marvin"},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
    ],
    install_requires=[],
    setup_requires=["pytest-runner"],
    tests_require=["pytest>=4"],
    packages=setuptools.find_packages("src"),
)
