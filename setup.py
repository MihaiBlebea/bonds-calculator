from setuptools import setup
from pathlib import Path

HERE = Path(__file__).parent

README = (HERE / "README.md").read_text()

with open("requirements.txt") as f:
    required = f.read().splitlines()

setup(
    name = "bonds",
    version = "0.1.1",
    author = "Mihai Blebea",
    author_email = "mihaiserban.blebea@gmail.com",
    description="Bonds calculator using data rom WiseAlpha",
	long_description=README,
	long_description_content_type="text/markdown",
	url="https://github.com/MihaiBlebea/bonds-calculator",
    packages = ["src"],
    install_requires = required,
    entry_points = {
        "console_scripts": [
            "bonds = src.__main__:main"
        ]
    })