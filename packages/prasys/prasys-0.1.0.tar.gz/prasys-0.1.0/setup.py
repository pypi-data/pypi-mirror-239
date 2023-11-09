from setuptools import setup, find_packages

setup(
    name="prasys",
    version="0.1.0",
    description="The project is for calculating and plotting performance and risk analysis for a portfolio of assets.",
    author="Edward Wall",
    author_email="ewallj@gmail.com",
    packages=find_packages(include=["prasys", "prasys.*"]),
    install_requires=[
        "pandas",
        "numpy",
        "matplotlib",
        "seaborn",
    ],
    extras_require={
        "dev": [
            "pytest",
            "black",
            "pytest-cov",
        ]
    },
)
