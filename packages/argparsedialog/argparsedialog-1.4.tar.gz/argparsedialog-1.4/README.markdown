# argparsedialog

Python library converting argparse to wizzard using dialog.

## Requirements

- Python 3.0 or later
- pythondialog

## Installation

Installation of Python module `argparsedialog` is very simple by PyPI:

    $ sudo pip install argparsedialog

Or you can install development version by extracting archive and run:

    $ sudo make install

## Documentation

Use it as `argparse.ArgumentParser`:

```python
from argparsedialog import ArgumentParser

parser = ArgumentParser(description='Description for help.')
parser.add_argument('--value', dest='value', help='Help of argument --value.')
args = parser.parse_args()
print(args)
```

Just during call of `parse_args` it will show dialog(s) to user instead of having to pass arguments from command line.

Look for more examples in `example.py`.

Why this project? Because some one likes command line arguments, someone likes wizzards. So why not generate wizzard by argument parser and support easily both. :-)

## TODO

 * Would be great to support pass some arugments from command line and for rest of them ask by wizzard.
