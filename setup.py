from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="marzban",
    version="0.1.2",
    packages=find_packages(),
    install_requires=[
        "httpx>=0.23.0",
        "pydantic>=1.10.0"
    ],
    author="Artem",
    author_email="contant@sm1ky.com",
    description="Асинхронная библиотека Python для взаимодействия с MarzbanAPI",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sm1ky/marzban_api",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9',
)