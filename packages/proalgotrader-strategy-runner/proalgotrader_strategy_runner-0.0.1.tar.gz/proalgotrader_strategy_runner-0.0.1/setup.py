import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    include_package_data=True,
    name="proalgotrader_strategy_runner",
    version="0.0.1",
    description="ProAlgoTrader Strategy Runner",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/krunaldodiya/proalgotrader_strategy_runner",
    author="Krunal Dodiya",
    author_email="kunal.dodiya1@gmail.com",
    packages=setuptools.find_packages(),
    install_requires=[
        "fastapi",
        "uvicorn",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
