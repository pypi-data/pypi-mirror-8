#!/usr/bin/env python

import sys
import os
import os.path
sys.path.insert(0, os.path.normpath(os.getcwd()))

from cppman import Formatter

Formatter.func_test()
