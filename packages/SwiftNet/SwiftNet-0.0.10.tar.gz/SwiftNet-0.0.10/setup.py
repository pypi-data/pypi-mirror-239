from setuptools import find_packages, setup

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="SwiftNet",
    version="0.0.10",
    description="Simple Package for creating multilayer Neural Nets ",
    package_dir={"": "SwiftNet"},
    packages=find_packages(where="SwiftNet"),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/badapple21/SwiftNet",
    author="Michael Noel",
    author_email="mjn2024@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent",
    ],
    install_requires=["numpy", "flask", "python-mnist"],
    python_requires=">=3.10",
)
