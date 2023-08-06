# -*- coding: utf-8 -*-
"""
@name:          new_program.py
@vers:          0.1.0
@author:        dthor
@created:       Tue Dec 02 10:04:25 2014
@descr:         A new file

Usage:
    new_program.py

Options:
    -h --help           # Show this screen.
    --version           # Show version.
"""

from __future__ import print_function, division, absolute_import
#from __future__ import unicode_literals

__author__ = "Douglas Thor"
__version__ = "v0.1.0"


class WaferInfo(object):
    """
    Contains the wafer info:
    Die Size
    Center XY
    Wafer Diameter
    Edge Exclusion
    Flat Exclusion
    """
    def __init__(self, die_size, center_xy, dia=150, edge_excl=5, flat_excl=5):
        self.die_size = die_size
        self.center_xy = center_xy
        self.dia = dia
        self.edge_excl = edge_excl
        self.flat_excl = flat_excl

    def __str__(self):
        string = """{}mm wafer with {}mm edge exclusion and \
{}mm flat exclusion. Die Size = {}"""
        return string.format(self.dia,
                             self.edge_excl,
                             self.flat_excl,
                             self.die_size)


def main():
    """ Main Code """
    raise RuntimeError("This module is not meant to be run by itself.")


if __name__ == "__main__":
    main()
