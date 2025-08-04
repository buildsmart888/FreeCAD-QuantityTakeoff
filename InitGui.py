# -*- coding: utf-8 -*-
"""
InitGui.py - Initialization file for QuantityTakeoff GUI
This file is executed when FreeCAD starts and loads the GUI elements
"""

import FreeCADGui

# Import the workbench
from QTOWorkbench import QTOWorkbench

# Register the workbench
FreeCADGui.addWorkbench(QTOWorkbench())
