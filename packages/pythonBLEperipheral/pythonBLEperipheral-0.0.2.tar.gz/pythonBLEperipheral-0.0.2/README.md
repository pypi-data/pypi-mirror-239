# python-ble-peripheral


## Description

This project delivers a library of Python based modules with which to build Bluetooth Low Energy (BLE) peripheral role applications. It is based on the [prior work of Douglas Otwell](https://github.com/Douglas6/cputemp), with small additions to satisfy personal requirements.

## Prerequisites

- Python 3
- bluez (>= 5.50)
- pip3


## Installation

To install directly from the PyPI repository, run:
```
    python3 -m pip install pythonBLEperipheral 
```

If installing from the source code directory, run:
```
    python3 -m pip install .
```

When run as an ordinary user, these commands install into the user's individual home directory system (under .local/lib/python3.x/site-packages/ for Linux systems). If a global installation is desired (available to all users), run the installation command as root.

Some Debian based Linux systems (including Raspberry Pi) may complain when installing with pip (preferrring official Debian packages). There have not yet been problems reported when using instead (with or without sudo):
```
    python3 -m pip install --break-system-packages pythonBLEperipheral
```
In this case a system wide installation places the module into /usr/local/lib/python3.x/dist-packages/


## Usage

As the cputemp example shows
```
    from pythonBLEperipheral.advertisement import Advertisement
    from pythonBLEperipheral.service import Application, Service, Characteristic, Descriptor

```

## Support

- [this project's _issues_](https://gitlab.com/chris.willing/python-ble-peripheral/-/issues)

- [original _Douglas 6_ project _issues_](https://github.com/Douglas6/cputemp/issues)

## Contributing

Please suggest any additions to this project by creating a [new _Issues_ topic](https://gitlab.com/chris.willing/python-ble-peripheral/-/issues).

## Authors

Thanks to Douglas Otwell for the overwhelming bulk of the code on which this project is based.

## License
MIT (http://opensource.org/licenses/MIT)

