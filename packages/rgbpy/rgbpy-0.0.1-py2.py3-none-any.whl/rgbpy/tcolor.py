# -*- coding: utf-8 -*-
"""
The `tcolor.py` is mainly for print (equivalent)
"""

class Tcolor:
    """
    Text-Color

    It print colored text to the terminal

    Usage:
        You can print normal text by:
            >>> from rgbpy.tcolor import Tcolor
            >>> print(Tcolor('Default text color'))

        The above one is equivalent of the below:
            >>> from rgbpy import normal
            >>> normal('I am in normal color')

        More examples:
            >>> from rgbpy import *

            >>> purple('I am purple in color')
            >>> blue('I am blue in color')
            >>> cyan('I am cyan in color')
            >>> green('I am green in color')
            >>> yellow('I am yellow in color')
            >>> red('I am red in color')
            >>> normal('I am a normal text')
            >>> bold('I make text bold')
            >>> underline('I underline text')
    """

    OKPURPLE = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    OKYELLOW = '\033[93m'
    OKRED = '\033[91m'
    ENDC = '\033[0m' # normal text
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

    # The `ENDC` is a normal text, that is why we include at the end of the print, to make sure color of previous, won't be for the next unless been choosen.

    def __init__(self, msg: bool = False):
        self.msg = msg

    def okpurple(self, msg):
        """Header, it print text in purple"""
        print(f'{self.OKPURPLE}{msg}{self.ENDC}')

    def okblue(self, msg):
        """Okblue, it print text in blue"""
        print(f'{self.OKBLUE}{msg}{self.ENDC}')

    def okcyan(self, msg):
        """Okcyan, it print text in cyan"""
        print(f'{self.OKCYAN}{msg}{self.ENDC}')

    def okgreen(self, msg):
        """Okgreen, it print text in green"""
        print(f'{self.OKGREEN}{msg}{self.ENDC}')

    def okyellow(self, msg):
        """Okyellow, it print text in yellow"""
        print(f'{self.OKYELLOW}{msg}{self.ENDC}')

    def okred(self, msg):
        """Okred, it print text in red"""
        print(f'{self.OKRED}{msg}{self.ENDC}')

    def okendc(self, msg):
        """Okendc, it print text in normal condition"""
        print(f'{self.ENDC}{msg}{self.ENDC}')

    def okbold(self, msg):
        """Okbold, it make text to be bold"""
        print(f'{self.BOLD}{msg}{self.ENDC}')

    def okunderline(self, msg):
        """Okunderline, it underline text"""
        print(f'{self.UNDERLINE}{msg}{self.ENDC}')

    def __str__(self):
        """__str__, it print text in normal condition"""
        return f'{self.ENDC}{self.msg}{self.ENDC}'
    

# APIs
def purple(msg):
    """
    Usage:
        >>> from rgbpy import purple
        >>> purple('I am in purple color')
    """
    a = Tcolor()
    a.okpurple(msg)


def blue(msg):
    """
    Usage:
        >>> from rgbpy import blue
        >>> blue('I am in blue color')
    """
    a = Tcolor()
    a.okblue(msg)


def cyan(msg):
    """
    Usage:
        >>> from rgbpy import cyan
        >>> cyan('I am in cyan color')
    """
    a = Tcolor()
    a.okcyan(msg)


def green(msg):
    """
    Usage:
        >>> from rgbpy import green
        >>> green('I am in green color')
    """
    a = Tcolor()
    a.okgreen(msg)


def yellow(msg):
    """
    Usage:
        >>> from rgbpy import yellow
        >>> yellow('I am in yellow color')
    """
    a = Tcolor()
    a.okyellow(msg)


def red(msg):
    """
    Usage:
        >>> from rgbpy import red
        >>> red('I am in red color')
    """
    a = Tcolor()
    a.okred(msg)


def normal(msg):
    """
    Usage:
        >>> from rgbpy import normal
        >>> normal('I am in normal color')
    """
    a = Tcolor()
    a.okendc(msg)


def bold(msg):
    """
    Usage:
        >>> from rgbpy import bold
        >>> bold('I am in bold color')
    """
    a = Tcolor()
    a.okbold(msg)


def underline(msg):
    """
    Usage:
        >>> from rgbpy import underline
        >>> underline('I am in underline color')
    """
    a = Tcolor()
    a.okunderline(msg)
