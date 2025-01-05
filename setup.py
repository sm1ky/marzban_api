from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="marzban",
    version="0.4.0",
    packages=find_packages(),
    install_requires=[
        "httpx>=0.23.0",
        "pydantic>=1.10.0",
        "paramiko>=3.5.0",
        "sshtunnel>=0.4.0",
        "datetime>=5.5",
    ],
    author="Artem",
    author_email="contant@sm1ky.com",
    description="Асинхронная библиотека Python для взаимодействия с MarzbanAPI | Поддерживает работу через HTTPS/SSH",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sm1ky/marzban_api",
    project_urls={
        "Homepage": "https://github.com/sm1ky/marzban_api",
        "Documentation [EN]": "https://github.com/sm1ky/marzban_api/blob/development/.readme/README_en.md", 
        "Documentation [RU]": "https://github.com/sm1ky/marzban_api/blob/development/.readme/README_ru.md", 
        "Source": "https://github.com/sm1ky/marzban_api",
        "Developer": "https://t.me/sm1ky"
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9',
)
