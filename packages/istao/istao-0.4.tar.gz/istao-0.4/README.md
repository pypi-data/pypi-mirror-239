<p align="center">
    <img src="https://github.com/Tao-Linux/Tao-ISO/blob/main/assets/tao.svg?raw=true" width=25% height=25%>
</p>

<h1 align="center">Python Library: istao</h1>

<p align="center">Library for Tao Python applications to check if the intended operating system is being used</p>

<p align="center">
    <a href="https://www.gnu.org/licenses/gpl-3.0.en.html"><img alt="GPLv3 License" src="https://img.shields.io/badge/License-GPLv3-red.svg"></a>
</p>

## Installation

You may either install a pre-built version of the package or build it yourself.

### Downloading a pre-built package

Pre-built packages are available on [PyPI](https://pypi.org/project/istao) (for Windows and macOS) and in [Tao-Repo](https://github.com/Tao-Linux/Tao-Repo).

### Building the package manually

To build the package manually, follow these steps:

1. Install needed dependencies:

```bash
sudo pacman -S --needed python python-build python-colorama python-distro
```

3. Clone this repository:

```bash
git clone https://github.com/Tao-Linux/python-istao.git
```

3. Navigate to the repository directory:

```bash
cd python-istao
```

4. Build the package:

```bash
python -m build
```

After the above command finishes, there should be package files in the `dist/` directory.

*Looking for the `pacman` version of this package? That's in [python-istao-PKGBUILD](https://github.com/Tao-Linux/python-istao-PKGBUILD).*

## Usage in Python

The library is intended to check if the operating system being used is Tao Linux. If it is not, it will exit, displaying an error.

First, import the package:

```python
import istao
```

Then call the check function (usually at the very beginning of a given script):

```python
istao.check()
```

## License

This repository is licensed under the [GPLv3 License](https://www.gnu.org/licenses/gpl-3.0.en.html). If you have found that Tao has violated any licenses or copyrights, please don't hesitate to open an issue on the repository/repositories that do so, and we will do our best to respond in a timely manner.
