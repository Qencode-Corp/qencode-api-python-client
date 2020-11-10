# Quickstart

## Installation

You don't need the source code unless you want to modify the package itself.
If you just want to use the package:

```sh
pip install --upgrade qencode
```

# Contributing

To modify the package, install [poetry](https://python-poetry.org/docs/#installation)
and checkout the source:

```sh
cd your-workspace-folder
git clone https://github.com/qencode-dev/qencode-api-python-client
cd qencode-api-python-client
poetry shell
poetry install
```

## Usage

```python
import qencode

client = qencode.Client(api_key=API_KEY)
client.create()

task = client.create_task()
```

## Documentation

Documentation is available at <https://docs.qencode.com>
