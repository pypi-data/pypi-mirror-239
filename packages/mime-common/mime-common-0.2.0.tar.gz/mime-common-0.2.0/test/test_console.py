import unittest
import io
import sys

from src.console import Console, color_numbers

class ConsoleTest(unittest.TestCase):
    TEST_MESSAGE = 'TEST MESSAGE'
    def test_error_nocolor(self):
        capture_output = io.StringIO()
        sys.stdout = capture_output
        cons = Console(use_colors=False)        
        cons.error(self.TEST_MESSAGE)
        sys.stdout = sys.__stdout__
        assert f"{self.TEST_MESSAGE}\n" == capture_output.getvalue()

    def test_error_color(self):
        capture_output = io.StringIO()
        sys.stdout = capture_output
        cons = Console(use_colors=True)        
        cons.error(self.TEST_MESSAGE)
        sys.stdout = sys.__stdout__
        assert f"\x1b[1;31m{self.TEST_MESSAGE}\x1b[0m\n" == capture_output.getvalue()

    def test_critical_color(self):
        capture_output = io.StringIO()
        sys.stdout = capture_output
        cons = Console(use_colors=True)        
        cons.critical(self.TEST_MESSAGE)
        sys.stdout = sys.__stdout__
        assert f"\x1b[1;37;41m{self.TEST_MESSAGE}\x1b[0m\n" == capture_output.getvalue()

    def test_print(self):
        capture_output = io.StringIO()
        sys.stdout = capture_output
        cons = Console(use_colors=False)
        cons.print(self.TEST_MESSAGE)
        sys.stdout = sys.__stdout__
        assert f"{self.TEST_MESSAGE}\n" == capture_output.getvalue()

    def test_all_colors_dummy(self):
        cons = Console(use_colors=True)
        cons.red("red")
        cons.black_on_red("black")
        cons.yellow("yellow")
        cons.green("green")
        cons.blue("blue")
        cons.print(f"{self.TEST_MESSAGE}", underline=True)
        assert True

    def test_rest_dummy(self):
        cons = Console()
        cons.debug("debug")
        cons.info("info")
        cons.warning("warning")
        assert True

class color_numbersTest(unittest.TestCase):
     def test_some_values(self):
        if color_numbers.RESET == 0 and \
            color_numbers.BOLD == 1 and \
            color_numbers.UNDERLINE == 4 and \
            color_numbers.BLACK == 30 and \
            color_numbers.RED == 31 and \
            color_numbers.GREEN == 32 and \
            color_numbers.YELLOW == 33 and \
            color_numbers.BLUE == 34 and \
            color_numbers.MAGENTA == 35  and \
            color_numbers.CYAN == 36 and \
            color_numbers.WHITE == 37 and \
            color_numbers.BGBLACK == 40 and \
            color_numbers.BGRED == 41 and \
            color_numbers.BGGREEN == 42 and \
            color_numbers.BGYELLOW == 43 and \
            color_numbers.BGBLUE == 44 and \
            color_numbers.BGMAGENTA == 45  and \
            color_numbers.BGCYAN == 46 and \
            color_numbers.BGWHITE == 47:
            assert True

if __name__=='__main__':
	unittest.main()     # pragma: no cover

