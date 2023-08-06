#!/usr/bin/env python3

__author__ = 'Frazer McLean <frazer@frazermclean.co.uk>'
__version__ = '0.1.7'
__license__ = 'MIT'


def test():
    """Run tests from tests directory."""
    import os.path
    import pytest
    pytest.main(os.path.dirname(os.path.abspath(__file__)))
