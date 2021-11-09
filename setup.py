import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="darc_experiment_toolbox",
    version="0.0.2",
    author="Benjamin T. Vincent",
    author_email="b.t.vincent@dundee.ac.uk",
    description="Delayed And Risky Choice Toolbox",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/drbenvincent/darc_toolbox",
    keywords=[
        "delay discounting",
        "risky choice",
        "psychological experiments",
        "bayesian",
        "adaptive design",
        "inference",
    ],
    packages=setuptools.find_packages(),
    install_requires=["badapted==0.0.3", "matplotlib", "numpy", "pandas", "scipy"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    include_package_data=True,
)
