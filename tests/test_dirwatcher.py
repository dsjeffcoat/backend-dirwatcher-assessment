#!/usr/bin/env python

import unittest
import argparse
import os
import logging
import signal


__author__ = 'madarp'


class TestDirwatcher(unittest.TestCase):
    """Main test fixture for Dirwatcher module"""

    def test_prog(self):
        """Test to see if the program is fully
        functional"""
        pass

    def test_parser(self):
        """Test to see if check_parser() returns
        a parser object"""
        pass

    def test_dir(self):
        """Test to see if program has a command
        line argument that watches for a specific
        directory"""
        pass

    def test_ext(self):
        """Tests to see if program filters file
        extensions"""
        pass

    def test_int(self):
        """Tests for a polling interval provided
        in the program"""
        pass

    def test_magic(self):
        """Test to see if command line argument
        searches for magic text"""
        pass

    def test_magic_detect(self):
        """Test to see if magic text is detected
        within files"""
        pass

    def test_os_signal(self):
        """Test if program responds to SIGINT and
        SIGTERM signals from the OS"""
        pass

    def test_exceptions(self):
        """Test for at least one exception handler
        in program. Program must stay running even
        if files/directories are deleted. Must also
        log appropriate event messages in either
        case"""
        pass

    def test_logging(self):
        """Tests for logger in program. All log
        messages should contain timestamps"""
        pass


if __name__ == '__main__':
    unittest.main()
