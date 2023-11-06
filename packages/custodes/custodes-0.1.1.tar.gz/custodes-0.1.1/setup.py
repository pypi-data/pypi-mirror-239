import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="custodes",
    version='0.1.1',
    author="aldf",
    author_email="dafiosl@gmail.com",
    description="ok",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/private_repo/uuidentifier",
    packages=setuptools.find_packages(),
    install_requires=['aiohttp', 'rich', 'simauth', 'aio-pika', 'urllib3',
                      'python-dotenv'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
