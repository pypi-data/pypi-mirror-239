# python-ble-peripheral


## Description

This project delivers a library of Python based modules with which to build Bluetooth Low Energy (BLE) peripheral role applications. It is based on the [prior work of Douglas Otwell](https://github.com/Douglas6/cputemp), with small additions to satisfy personal requirements.

## Prerequisites

- Python 3
- bluez (>= 5.50)


## Installation

If installing from this directory, run:
```
    python3 -m pip install .
```
If installing directly from the PyPi repository, run:
```
    python3 -m pip install python-ble-peripheral 
```
When run as an ordinary user, these commands install into the user's individual home directory system. If a global installation is desired (available to all users), run the installation command as root.

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

