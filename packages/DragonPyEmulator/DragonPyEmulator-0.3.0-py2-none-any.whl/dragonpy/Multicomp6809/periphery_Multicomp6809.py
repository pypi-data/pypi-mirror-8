#!/usr/bin/env python
# encoding:utf8

"""
    DragonPy - Dragon 32 emulator in Python
    =======================================


    http://searle.hostei.com/grant/Multicomp/


    :created: 2014 by Jens Diemer - www.jensdiemer.de
    :copyleft: 2014 by the DragonPy team, see AUTHORS for more details.
    :license: GNU GPL v3 or above, see LICENSE for more details.
"""

from __future__ import absolute_import, division, print_function


import sys
import os
import logging

log = logging.getLogger(__name__)

try:
    # Python 3
    import queue
    import tkinter
except ImportError:
    # Python 2
    import Queue as queue
    import Tkinter as tkinter


class Multicomp6809Periphery(object):
    def __init__(self, cfg, cpu, memory, display_callback, user_input_queue):
        self.cfg = cfg
        self.cpu = cpu
        self.memory = memory
        self.display_callback = display_callback
        self.user_input_queue = user_input_queue

#     BUS_ADDR_AREAS = (
#         (0xFFD8, 0xFFDF, "SD Card"),
#         (0xFFD2, 0xFFD3, "Interface 2"),
#         (0xFFD0, 0xFFD1, "Interface 1 (serial interface or TV/Keyboard)"),
#         (0xBFF0, 0xBFFF, "Interrupt vectors"),
#     )
        self.memory.add_read_byte_callback(self.read_acia_status, 0xffd0) #  Control/status port of ACIA
        self.memory.add_read_byte_callback(self.read_acia_data, 0xffd1) #  Data port of ACIA

        self.memory.add_write_byte_callback(self.write_acia_status, 0xffd0) #  Control/status port of ACIA
        self.memory.add_write_byte_callback(self.write_acia_data, 0xffd1) #  Data port of ACIA

    def write_acia_status(self, cpu_cycles, op_address, address, value):
        return 0xff
    def read_acia_status(self, cpu_cycles, op_address, address):
        return 0x03

    def read_acia_data(self, cpu_cycles, op_address, address):
        try:
            char = self.user_input_queue.get(block=False)
        except queue.Empty:
            return 0x0

        if isinstance(char, int):
            log.critical("Ignore %s from user_input_queue", repr(char))
            return 0x0

        value = ord(char)
        log.error("%04x| (%i) read from ACIA-data, send back %r $%x",
            op_address, cpu_cycles, char, value
        )
        return value

    def write_acia_data(self, cpu_cycles, op_address, address, value):
        char = chr(value)
        log.debug("Write to screen: %s ($%x)" , repr(char), value)

#         if value >= 0x90: # FIXME: Why?
#             value -= 0x60
#             char = chr(value)
# #            log.error("convert value -= 0x30 to %s ($%x)" , repr(char), value)
#
#         if value <= 9: # FIXME: Why?
#             value += 0x41
#             char = chr(value)
# #            log.error("convert value += 0x41 to %s ($%x)" , repr(char), value)

        self.display_callback(char)


"""
    KEYCODE_MAP = {
        127: 0x03, # Break Key
    }
"""


#------------------------------------------------------------------------------


def test_run():
    import os
    import sys
    import subprocess
    cmd_args = [
        sys.executable,
        os.path.join("..", "DragonPy_CLI.py"),
#         "-h"
#         "--log_list",
        "--log", "dragonpy.Multicomp6809,10", # "dragonpy.Dragon32.MC6821_PIA,10",

#          "--verbosity", "10", # DEBUG
#         "--verbosity", "20", # INFO
#         "--verbosity", "30", # WARNING
#         "--verbosity", "40", # ERROR
#         "--verbosity", "50", # CRITICAL/FATAL
        "--verbosity", "99", # nearly all off
#         "--machine", "Dragon32", "run",
        "--machine", "Multicomp6809", "run",
#        "--max_ops", "1",
#        "--trace",
    ]
    print("Startup CLI with: %s" % " ".join(cmd_args[1:]))
    subprocess.Popen(cmd_args, cwd="..").wait()


if __name__ == "__main__":
    test_run()

