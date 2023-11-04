"""
Helper class for easy console output

"""
from __future__ import annotations

USE_COLORS = False
"""Set default for class"""
ANSI_START = '\033['
"""Console ansi start value for special characters"""
ANSI_END = 'm'
"""Console ansi end value for special characters"""

COLOR_MAPPING: dict[str, int] = { 
    'black': 0,
    'red': 1,
    'green': 2,
    'yellow': 3,
    'blue': 4,
    'magenta': 5,
    'cyan': 6,
    'white': 7
} 
"""Dictionary of console color names to number."""

class color_numbers:
    """List of constants for color values"""
    RESET = 0
    BOLD = 1
    UNDERLINE = 4
    BLACK = 30
    RED = 31
    GREEN = 32
    YELLOW = 33
    BLUE = 34
    MAGENTA = 35 
    CYAN = 36
    WHITE = 37
    BGBLACK = 40
    BGRED = 41
    BGGREEN = 42
    BGYELLOW = 43
    BGBLUE = 44
    BGMAGENTA = 45 
    BGCYAN = 46
    BGWHITE = 47

class Console:
    """
    Singleton Class for handling console output.
    """
    _instance = None
    def __new__(cls, use_colors:bool=USE_COLORS):
        """
        Parameters
        ----------
        *use_colors* : str, optional
            Wether or not to use colors when printing to console

        """
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        cls._instance.set_colors(use_colors)
        return cls._instance

    #Dynamically tur on/off console colors
    def set_colors(self, use_colors:bool=False) -> None:
        """set to turn on or off console colors"""
        self.use_colors: bool = use_colors

    def is_colors(self) -> bool:
        """Return True if color output is set. Else return False."""
        return self.use_colors
    
    def bgcolor(self, color:str='black') -> int:
        """Get background color value from string"""
        return COLOR_MAPPING.get(color.lower(), 0) + 40
    
    def fgcolor(self, color:str='white') -> int:
        """Get forground color value from string"""
        return COLOR_MAPPING.get(color.lower(), 7) + 30

    def print(self, message:str, fgcolor:str=None, bgcolor:str=None, bold:bool=False, underline:bool=False) -> None:
        """
        Print message to console

        Parameters
        ----------
        *message* : str
            The message to print

        *fgcolor* : str, optional
            Forground color to use

        *bgcolor* : str, optional
            Background color to use

        *bold* : bool, optional
            Print message bold

        *underline* : bool
            Print message underlined
        """

        start_string: str = ""
        end_string: str = ""
        if self.is_colors():
            if bold:
                start_string += (";" if len(start_string) > 0 else "") + str(color_numbers.BOLD)
            if underline:
                start_string += (";" if len(start_string) > 0 else "") + str(color_numbers.UNDERLINE)
            if fgcolor is not None:
                start_string += (";" if len(start_string) > 0 else "") + str(self.fgcolor(fgcolor))
            if bgcolor is not None:
                start_string += (";" if len(start_string) > 0 else "") + str(self.bgcolor(bgcolor))
            start_string = f"{ANSI_START}{start_string}{ANSI_END}" if len(start_string) > 0 else ""
            end_string = f"{ANSI_START}{color_numbers.RESET}{ANSI_END}"
        print(f"{start_string}{message}{end_string}")

    def red(self, message, bold=False, underline=False) -> None:
        self.print(message=message, fgcolor='red', bold=bold, underline=underline)
    def black_on_red(self, message, bold=False, underline=False) -> None:
        self.print(message=message, fgcolor='black', bgcolor='red', bold=bold, underline=underline)
    def yellow(self, message, bold=False, underline=False) -> None:
        self.print(message=message, fgcolor='yellow', bold=bold, underline=underline)
    def green(self, message, bold=False, underline=False) -> None:
        self.print(message=message, fgcolor='green', bold=bold, underline=underline)
    def blue(self, message, bold=False, underline=False) -> None:
        self.print(message=message, fgcolor='blue', bold=bold, underline=underline)

    def critical(self, message) -> None:
        self.print(message=message, fgcolor='white', bgcolor='red', bold=True, underline=False)
    def error(self, message) -> None:
        self.print(message=message, fgcolor='red', bold=True, underline=False)
    def warning(self, message) -> None:
        self.print(message=message, fgcolor='yellow', bold=True, underline=False)
    def debug(self, message) -> None:
        self.print(message=message, fgcolor='cyan', bold=False, underline=False)
    def info(self, message) -> None:
        self.print(message=message, fgcolor='blue', bold=False, underline=False)
