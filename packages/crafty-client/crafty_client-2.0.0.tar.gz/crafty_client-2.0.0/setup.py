from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="crafty_client",
    version="2.0.0",
    description="A python library for talking to Crafty Controller - a server management panel",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Arcadia Technology, LLC.",
    url="https://gitlab.com/crafty-controller/crafty-client",
    install_requires=[
        "requests",
        "urllib3",
    ],
    packages=["crafty_client", "crafty_client.static"],
)
