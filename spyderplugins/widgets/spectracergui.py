# -*- coding: utf-8 -*-
#
# Copyright © 2009-2010 Pierre Raybaut
# Licensed under the terms of the MIT License
# (see spyderlib/__init__.py for details)

"""Pylint widget"""

# pylint: disable=C0103
# pylint: disable=R0903
# pylint: disable=R0911
# pylint: disable=R0201

from __future__ import with_statement, print_function

from spyderlib.qt.QtGui import (QHBoxLayout, QWidget, QTreeWidgetItem,
                                QMessageBox, QVBoxLayout, QLabel)
from spyderlib.qt.QtCore import Signal, QProcess, QByteArray, QTextCodec
locale_codec = QTextCodec.codecForLocale()
from spyderlib.qt.compat import getopenfilename

import sys
import os
import os.path as osp
import time
import re
import subprocess

from pyqtgraph import GraphicsLayoutWidget

# Local imports
from spyderlib import dependencies
from spyderlib.utils import programs
from spyderlib.utils.encoding import to_unicode_from_fs
from spyderlib.utils.qthelpers import get_icon, create_toolbutton
from spyderlib.baseconfig import get_conf_path, get_translation
from spyderlib.widgets.onecolumntree import OneColumnTree
from spyderlib.widgets.texteditor import TextEditor
from spyderlib.widgets.comboboxes import (PythonModulesComboBox,
                                          is_module_or_package)
from spyderlib.py3compat import PY3, to_text_string, getcwd, pickle
_ = get_translation("spectracer", dirname="spyderplugins")

class SpectracerWidget(QWidget):
    """
    Spectracer widget
    """
    VERSION = '1.1.0'
    redirect_stdio = Signal(bool)
    
    def __init__(self, parent):
        QWidget.__init__(self, parent)
        self.setWindowTitle("Spectracer")
        
        self.output = None
        self.error_output = None

        self.chart = GraphicsLayoutWidget()
        layout = QVBoxLayout()
        layout.addWidget(self.chart)
        self.setLayout(layout)