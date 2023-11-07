import setuptools

# Load the long_description from README.md
with open("README.md", "r") as fh:
    long_description = fh.read()

# with open('requirements.txt', 'r') as f:
    # required = f.read().splitlines()

setuptools.setup(
    name="projectedlmc",
    version="0.0.4",
    author="",
    author_email="",
    description="A short package based on gpytorch implementing the Projected LMC model",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://qwerty6191.github.io/projected-lmc/",
    packages=setuptools.find_packages(),
    # py_modules=['projected_lmc'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    install_requires=['gpytorch', 'linear_operator', 'scikit_learn'],
    # install_requires=required,
)
