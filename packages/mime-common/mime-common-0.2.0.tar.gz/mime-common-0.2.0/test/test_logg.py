from __future__ import annotations
import unittest
import os
import sys
import tempfile
import re

from logg import Logg

class LoggTest(unittest.TestCase):
    DEBUG_MESSAGE = 'DEBUG MESSAGE'
    INFO_MESSAGE = 'INFO MESSAGE'
    WARNING_MESSAGE = 'WARNING MESSAGE'
    ERROR_MESSAGE = 'ERROR MESSAGE'
    CRITICAL_MESSAGE = 'CRITICAL_MESSAGE'
    MESSAGE_PATTERN = r"(\d{4}-\d{2}-\d{2} \d{2}\:\d{2}\:\d{2}) (DEBUG|INFO|WARNING|ERROR|CRITICAL): (.*)"
    EXCEPTION_PATTERN = r".*'Exception'.* (INFO\ MESSAGE) .*"

    @classmethod
    def setUpClass(cls) -> None:
        super(LoggTest, cls).setUpClass()
        cls.tempdir: tempfile.TemporaryDirectory = tempfile.TemporaryDirectory()
  
    def setUp(self):
        return super().setUp()
    
    def tearDown(self):
        return super().tearDown()
    
    @classmethod
    def tearDownClass(self) -> None:
        pass

    def write_messages(self, logg : Logg) -> None:
        """Helper method to write one of each logglevel to file"""
        logg.debug(self.DEBUG_MESSAGE)
        logg.info(self.INFO_MESSAGE)
        logg.warning(self.WARNING_MESSAGE)
        logg.error(self.ERROR_MESSAGE)
        logg.critical(self.CRITICAL_MESSAGE)

    def match_message(self, line, message : str) -> bool:   # pragma: no cover
        found: re.Match[str] | None = re.match(self.MESSAGE_PATTERN, line)
        if found:
            if found.groups()[2] == message:
                return True
        return False        

    def match_exception(self, line, message : str) -> bool: # pragma: no cover
        found: re.Match[str] | None = re.match(self.EXCEPTION_PATTERN, line)
        if found:
            if found.groups()[0] == message:
                return True
        return False        

        
    def test_errorlevel_noconsole(self) -> None:
        loggfile: str = os.path.join(self.tempdir.name, f"{sys._getframe(  ).f_code.co_name}.log")
        logg = Logg(loggfile, Logg.ERROR, show_in_console=False)
        self.write_messages(logg)
        logg.clear(Logg)
        logg = None

        with open(loggfile, "r") as f:
            lines: str = f.read().splitlines()
            if len(lines) == 2:
                if self.match_message(lines[0], self.ERROR_MESSAGE) and \
                    self.match_message(lines[1], self.CRITICAL_MESSAGE):
                    assert True
                    return      # pragma: no cover
        assert False    # pragma: no cover

    def test_errorlevel_console(self):
        # TODO: Do console tests
        assert True

    def test_debuglevel_console(self):
        loggfile: str = os.path.join(self.tempdir.name, f"{sys._getframe(  ).f_code.co_name}.log")
        logg = Logg(loggfile, Logg.DEBUG, show_in_console=False)
        self.write_messages(logg)
        logg.clear(Logg)
        logg = None

        with open(loggfile, "r") as f:
            lines: str = f.read().splitlines()
            if len(lines) == 5:
                if self.match_message(lines[0], self.DEBUG_MESSAGE) and \
                    self.match_message(lines[1], self.INFO_MESSAGE) and \
                    self.match_message(lines[2], self.WARNING_MESSAGE) and \
                    self.match_message(lines[3], self.ERROR_MESSAGE) and \
                    self.match_message(lines[4], self.CRITICAL_MESSAGE):
                    assert True
                    return
        assert False    # pragma: no cover

    def test_exception_string(self) -> None:
        loggfile: str = os.path.join(self.tempdir.name, f"{sys._getframe(  ).f_code.co_name}.log")
        logg = Logg(loggfile, Logg.DEBUG, show_in_console=False)
        try:
            raise Exception(self.INFO_MESSAGE)
        except Exception as e:
            exception_string: str = logg.exception_string(e)
            if self.match_exception(exception_string, self.INFO_MESSAGE):
                logg.clear(Logg)
                logg = None
                assert True
                return
        logg.clear(Logg)    # pragma: no cover
        logg = None         # pragma: no cover
        assert False        # pragma: no cover
        
    def test_str2level(self) -> None:
        loggfile: str = os.path.join(self.tempdir.name, f"{sys._getframe(  ).f_code.co_name}.log")
        logg = Logg(loggfile, Logg.DEBUG, show_in_console=False)
        debug_id: int = logg.str2level('DEBUG')
        info_id: int = logg.str2level(None)
        warning_id: int = logg.str2level('warning')
        error_id: int = logg.str2level('ERroR')
        critical_id = logg.str2level('critical')

        if debug_id == 10 and \
            info_id == 20 and \
            warning_id == 30 and \
            error_id == 40 and \
            critical_id == 50:
            assert True
            logg.clear(Logg)
            logg = None
            return
        logg.clear(Logg)    # pragma: no cover
        logg = None         # pragma: no cover
        assert False        # pragma: no cover

if __name__=='__main__':
	unittest.main()     # pragma: no cover

