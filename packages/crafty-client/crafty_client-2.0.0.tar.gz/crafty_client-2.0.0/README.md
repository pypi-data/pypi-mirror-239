# Crafty-Client

## About

Crafty Client is a pypi (pip) package for interfacing with the [Crafty server control panel](https://gitlab.com/crafty-controller/crafty-4).

## Install

Make sure you have python3 installed on your system with the pip package manager.

#### For Windows environments
```bash
pip install crafty-client
```

#### For linux (apt/yum/rpm/etc.) environments
```bash
pip3 install crafty-client
```

## Usage

Example:
```python
from crafty_client import Crafty4

URL = "https://127.0.0.1:8443"    # The location of the crafty-web webserver
API_TOKEN = "<place token here>"  # Your crafty Web API token, printed in the console at installation.

crafty = Crafty4(URL, API_TOKEN)

print(crafty.list_mc_servers())
```