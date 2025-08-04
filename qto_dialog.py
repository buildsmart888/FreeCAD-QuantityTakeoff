# -*- coding: utf-8 -*-
"""
qto_dialog.py - Compatibility layer for old imports
This file maintains backward compatibility while redirecting to new modular structure
"""

import sys
import os

# Add the module path to sys.path for absolute imports
module_path = os.path.dirname(__file__)
if module_path not in sys.path:
    sys.path.insert(0, module_path)

try:
    # Import from new modular structure
    from dialogs.main_dialog import show_main_dialog as show_dialog, add_selected_objects
except ImportError as e:
    print(f"Error importing from new structure: {e}")
    # Fallback functions
    def show_dialog():
        print("Dialog import failed")
    
    def add_selected_objects(objects):
        print(f"Add objects import failed: {len(objects) if objects else 0}")

# Legacy function names for backward compatibility
def show_quantity_takeoff_dialog():
    """Legacy function name - redirects to new show_main_dialog"""
    return show_dialog()

# Make sure the old API still works
__all__ = ['show_dialog', 'add_selected_objects', 'show_quantity_takeoff_dialog']
