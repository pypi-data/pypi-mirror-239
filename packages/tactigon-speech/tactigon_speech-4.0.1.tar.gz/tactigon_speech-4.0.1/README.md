# Tactigon Speech

![The tactigon team](https://avatars.githubusercontent.com/u/63020285?s=200&v=4)

This package add voice command functionalities to the Tactigon Skin using Bluetooth Low Energy. It is based on the Tactigon Gear.

## Architecture

Tactigon Speech is a class that inherits from the base TSkin class, which can be found in the [Tactigon Gear SDK](https://pypi.org/project/tgear-sdk/).

## Prerequisites
In order to use the Tactigon Gear SDK the following prerequisites needs to be observed:

Tactigon Gear SDK: >=4.1.0

Platforms:
 - Windows 10 (x86-64 CPU with AVX/FMA)
 - macOS >=12.0 (x86-64 CPU with AVX/FMA)

Python version: following versions has been used and tested. It is STRONGLY recommended to use these ones depending on platform.
   - Win10: 3.8.7
   - macOS: 3.8.8

It is recommended to create a dedicated python virtual environment and install the packages into the virtual environment:  
  * `python -m venv venv`
  * `pip install tactigon-speech`

Depending on your installation (Mac users) you may need to use `python3` and `pip3` instead of `python` and `pip` respectively

## Tactigon Gear complete reference
A complete reference to Tactigon Gear SDK and the Tactigon Skin can be found at [Tactigon Gear SDK](https://pypi.org/project/tgear-sdk/)

## Tactigon Speech examples
For a list of example you can go to [Tactigon OS repository](https://github.com/TactigonTeam/Tactigon-OS)