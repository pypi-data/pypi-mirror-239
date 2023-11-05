# RGBpy

RGBpy it is python text-style ✅ not python textile! 🤔 it actually print your text on terminal in different kind of colors, including logging.

[![Downloads Month Badge](https://static.pepy.tech/badge/rgbpy/month)](https://pypi.org/project/rgbpy)
[![Downloads Week Badge](https://static.pepy.tech/badge/rgbpy/week)](https://pypi.org/project/rgbpy)
[![License Badge](https://img.shields.io/pypi/l/rgbpy.svg)](https://pypi.org/project/rgbpy)
[![Supported Wheel Badge](https://img.shields.io/pypi/wheel/rgbpy.svg)](https://pypi.org/project/rgbpy)
[![Supported Versions Badge](https://img.shields.io/pypi/pyversions/rgbpy.svg)](https://pypi.org/project/rgbpy)
[![Contributors](https://img.shields.io/github/contributors/usmanmusa1920/rgbpy.svg)](https://github.com/usmanmusa1920/rgbpy/graphs/contributors)

# Simple use of rgbpy

First we recommend creating a virtual environment `python -m venv venv` and then activate it `source venv/bin/activate`

Once that finish now install the library using

```sh
    pip install rgbpy
```

Wait for the installation to finish, basically the library was uploaded using `sdist` (Source Distribution) and `bdist_wheel` (Built Distribution).

To print text with color using python print, instead of using `print` function, use any of the following functions (purple, blue, cyan, green, yellow, red, normal, bold, underline, log_style)

```python
    >>> from rgbpy import (purple, blue, cyan, green, yellow, red, normal, bold, underline)

    >>> purple('I am purple in color')
    >>> blue('I am blue in color')
    >>> cyan('I am cyan in color')
    >>> green('I am green in color')
    >>> yellow('I am yellow in color')
    >>> red('I am red in color')
    >>> normal('I am a normal text')
    >>> bold('I make text bold')
    >>> underline('I underline text')
```

To print logging text with color:

```python
    >>> import logging
    >>> from rgbpy import log_style
    
    >>> FORMATTER = '[+] [%(asctime)s] [%(levelname)s] %(message)s'
    >>> logging.basicConfig(format=FORMATTER)
    >>> LOGGER = logging.getLogger(__name__)
    >>> LOGGER.setLevel(logging.DEBUG)

    >>> log_style('I am info logger')
    >>> log_style('I am yellow logger', col='yellow')
    >>> log_style('I am error logger', log='error')
```

See more documentations <a href="https://rgbpy.readthedocs.io">here!</a>

## Useful links

-   Documentation: https://rgbpy.readthedocs.io
-   Repository: https://github.com/usmanmusa1920/rgbpy
-   PYPI Release: https://pypi.org/project/rgbpy

Pull requests are welcome
