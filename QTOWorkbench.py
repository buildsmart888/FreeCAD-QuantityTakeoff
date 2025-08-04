# -*- coding: utf-8 -*-
"""
QTOWorkbench.py - Quantity Takeoff Workbench for FreeCAD
This file defines the workbench that will appear in FreeCAD's workbench selector
"""

import FreeCADGui
import FreeCAD
import os

class QTOWorkbench(FreeCADGui.Workbench):
    """
    Quantity Takeoff Workbench
    """
    
    def __init__(self):
        self.__class__.MenuText = "Quantity Takeoff"
        self.__class__.ToolTip = "Quantity Takeoff workbench for calculating material quantities"
        self.__class__.Icon = self._get_icon_path()
    
    def _get_icon_path(self):
        """Get the path to the workbench icon"""
        import os
        icon_path = os.path.join(os.path.dirname(__file__), "resources", "icons", "qto.svg")
        if os.path.exists(icon_path):
            return icon_path
        return ""
    
    def Initialize(self):
        """
        This function is executed when the workbench is first activated.
        It is executed only once in a FreeCAD session followed by the Activated function.
        """
        # Import using absolute path with try/except for error handling
        import sys
        import os
        
        # Add current module path to sys.path
        module_path = os.path.dirname(__file__)
        if module_path not in sys.path:
            sys.path.insert(0, module_path)
        
        try:
            from dialogs.main_dialog import show_main_dialog, add_selected_objects
        except ImportError as e:
            FreeCAD.Console.PrintError(f"Error importing main_dialog: {e}\n")
            # Fallback to old qto_dialog if available
            try:
                import qto_dialog
                show_main_dialog = qto_dialog.show_dialog
                add_selected_objects = qto_dialog.add_selected_objects
            except ImportError:
                FreeCAD.Console.PrintError("Could not import dialog modules\n")
                return
        
        # Create commands
        self.commands = ["QTO_OpenDialog", "QTO_ShowObjectInfo", "QTO_SelectObject"]
        
        # Create the main dialog command
        class QTOOpenDialogCommand:
            def GetResources(self):
                return {
                    'Pixmap': self._get_icon_path(),
                    'MenuText': 'เปิด BOQ Dialog',
                    'ToolTip': 'เปิด dialog หลักสำหรับ Bill of Quantities'
                }
            
            def Activated(self):
                """Called when the command is activated"""
                show_main_dialog()
            
            def IsActive(self):
                """Return True when the command should be active"""
                return True
            
            def _get_icon_path(self):
                """Get the path to the command icon"""
                icon_path = os.path.join(os.path.dirname(__file__), "resources", "icons", "qto.svg")
                if os.path.exists(icon_path):
                    return icon_path
                return ""
        
        # Create the object info dialog command
        class QTOShowObjectInfoCommand:
            def GetResources(self):
                return {
                    'Pixmap': self._get_icon_path(),
                    'MenuText': 'แสดงข้อมูลชิ้นงาน',
                    'ToolTip': 'แสดงหน้าต่างข้อมูลชิ้นงานทั้งหมดพร้อมระบบกรอง'
                }
            
            def Activated(self):
                """Called when the command is activated"""
                try:
                    # Import with absolute path
                    import sys
                    import os
                    module_path = os.path.dirname(__file__)
                    if module_path not in sys.path:
                        sys.path.insert(0, module_path)
                    
                    from dialogs.object_info_dialog import ObjectInfoDialog
                    
                    if not FreeCAD.ActiveDocument:
                        FreeCAD.Console.PrintMessage("กรุณาเปิด document ก่อน\\n")
                        return
                        
                    objects = FreeCAD.ActiveDocument.Objects
                    if not objects:
                        FreeCAD.Console.PrintMessage("ไม่มีชิ้นงานใน document\\n")
                        return
                    
                    dialog = ObjectInfoDialog(objects)
                    dialog.exec_()
                    
                except Exception as e:
                    FreeCAD.Console.PrintError(f"Error showing object info dialog: {e}\\n")
            
            def IsActive(self):
                """Return True when the command should be active"""
                return FreeCAD.ActiveDocument is not None
            
            def _get_icon_path(self):
                """Get the path to the command icon"""
                icon_path = os.path.join(os.path.dirname(__file__), "resources", "icons", "qto.svg")
                if os.path.exists(icon_path):
                    return icon_path
                return ""
        
        # Create the select object command
        class QTOSelectObjectCommand:
            def GetResources(self):
                return {
                    'Pixmap': self._get_icon_path(),
                    'MenuText': 'เลือกชิ้นงาน',
                    'ToolTip': 'เลือกชิ้นงานใน 3D view และเพิ่มเข้าตาราง'
                }
            
            def Activated(self):
                """Called when the command is activated"""
                # Get selected objects
                selection = FreeCADGui.Selection.getSelection()
                if selection:
                    add_selected_objects(selection)
                    FreeCAD.Console.PrintMessage(f"เพิ่ม {len(selection)} ชิ้นงานเข้าตาราง\\n")
                else:
                    FreeCAD.Console.PrintMessage("กรุณาเลือกชิ้นงานใน 3D view ก่อน\\n")
            
            def IsActive(self):
                """Return True when the command should be active"""
                return FreeCAD.ActiveDocument is not None
            
            def _get_icon_path(self):
                """Get the path to the command icon"""
                icon_path = os.path.join(os.path.dirname(__file__), "resources", "icons", "qto.svg")
                if os.path.exists(icon_path):
                    return icon_path
                return ""
        
        # Register the commands
        FreeCADGui.addCommand('QTO_OpenDialog', QTOOpenDialogCommand())
        FreeCADGui.addCommand('QTO_ShowObjectInfo', QTOShowObjectInfoCommand())
        FreeCADGui.addCommand('QTO_SelectObject', QTOSelectObjectCommand())
        
        # Add to toolbar and menu
        self.appendToolbar("Quantity Takeoff", self.commands)
        self.appendMenu("Quantity Takeoff", self.commands)
    
    def Activated(self):
        """
        This function is executed whenever the workbench is activated
        """
        FreeCAD.Console.PrintMessage("Quantity Takeoff workbench activated\\n")
    
    def Deactivated(self):
        """
        This function is executed whenever the workbench is deactivated
        """
        FreeCAD.Console.PrintMessage("Quantity Takeoff workbench deactivated\\n")
    
    def ContextMenu(self, recipient):
        """
        This function is executed whenever the user right-clicks on screen
        "recipient" will be either "view" for 3D view or "tree" for tree view
        """
        pass
    
    def GetClassName(self):
        """
        This function is mandatory if this is a full Python workbench
        """
        return "Gui::PythonWorkbench"
