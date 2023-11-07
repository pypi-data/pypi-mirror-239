import re

import setuptools


setuptools.setup(
    name="test-marvin",
    description="",
    keywords="",
    long_description="""Dummy package""",
    include_package_data=True,
    version="v0.0.1",
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
