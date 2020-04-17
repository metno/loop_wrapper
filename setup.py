import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="loop_wrapper",
    version="3.5.0",
    author="Thomas Lavergne",
    author_email="thomas.lavergne@met.no",
    description="A job-control tool to iterate scripts on ranges of dates.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/metno/loop_wrapper",
    packages=setuptools.find_packages(),
    scripts=["loop_wrapper"],
    project_urls={
        "Documentation": "https://loop-wrapper.readthedocs.io",
        "Source Code": "https://github.com/metno/loop_wrapper",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "Operating System :: OS Independent",
        "Intended Audience :: Science/Research",
        "Topic :: Utilities",
    ],
    python_requires='>=3.6',
)
