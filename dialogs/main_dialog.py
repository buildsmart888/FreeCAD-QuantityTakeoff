# -*- coding: utf-8 -*-
"""
QuantityTakeoffMainDialog - Main BOQ Dialog for construction quantity takeoff
"""

try:
    from PySide2 import QtWidgets, QtCore, QtGui
    from PySide2.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QHeaderView, QMessageBox, QFileDialog, QLabel
    from PySide2.QtCore import Qt, QTimer, Signal
    from PySide2.QtGui import QFont
except ImportError:
    try:
        from PyQt5 import QtWidgets, QtCore, QtGui
        from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QHeaderView, QMessageBox, QFileDialog, QLabel
        from PyQt5.QtCore import Qt, QTimer, pyqtSignal as Signal
        from PyQt5.QtGui import QFont
    except ImportError as e:
        print(f"Error importing Qt modules: {e}")
        QtWidgets = None

import FreeCAD
import FreeCADGui
import csv
import os
import sys

# Add the module path to sys.path for absolute imports
module_path = os.path.dirname(os.path.dirname(__file__))
if module_path not in sys.path:
    sys.path.insert(0, module_path)

from utils.calculations import QTOCalculator

class QuantityTakeoffMainDialog(QMainWindow):
    """
    Main dialog for BOQ (Bill of Quantities) management
    """
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.calculator = QTOCalculator()
        self.setupUI()
        self.setupTable()
        self.load_objects_from_document()
        
    def setupUI(self):
        """Setup the user interface"""
        self.setWindowTitle("Quantity Takeoff - BOQ Management")
        self.setGeometry(100, 100, 1400, 600)
        
        # Central widget
        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        layout = QVBoxLayout(central_widget)
        
        # Title
        title = QLabel("Quantity Takeoff - Bill of Quantities")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Arial", 16, QFont.Bold))
        layout.addWidget(title)
        
        # Button layout
        button_layout = QHBoxLayout()
        
        self.refresh_btn = QPushButton("Refresh")
        self.refresh_btn.clicked.connect(self.refresh_data)
        button_layout.addWidget(self.refresh_btn)
        
        self.calculate_btn = QPushButton("Calculate")
        self.calculate_btn.clicked.connect(self.calculate_totals)
        button_layout.addWidget(self.calculate_btn)
        
        self.show_object_info_btn = QPushButton("แสดงข้อมูลชิ้นงาน")
        self.show_object_info_btn.clicked.connect(self.show_object_info_dialog)
        button_layout.addWidget(self.show_object_info_btn)
        
        self.export_btn = QPushButton("Export")
        self.export_btn.clicked.connect(self.export_to_csv)
        button_layout.addWidget(self.export_btn)
        
        button_layout.addStretch()
        layout.addLayout(button_layout)
        
        # Table
        self.table = QTableWidget()
        layout.addWidget(self.table)
        
        # Grand total layout
        total_layout = QHBoxLayout()
        total_layout.addStretch()
        
        self.grand_total_label = QLabel("Grand Total: 0.00")
        self.grand_total_label.setFont(QFont("Arial", 12, QFont.Bold))
        total_layout.addWidget(self.grand_total_label)
        
        layout.addLayout(total_layout)
        
    def setupTable(self):
        """Setup the main BOQ table"""
        # BOQ columns for construction
        self.columns = [
            "Object Name", "Object Type", "Material", "Length (m)", "Width (m)", 
            "Height (m)", "Volume (m³)", "Area (m²)", "Quantity", "Unit Weight (kg)",
            "Material/unit", "Labor/unit", "Material Total", "Labor Total", "Total"
        ]
        
        self.table.setColumnCount(len(self.columns))
        self.table.setHorizontalHeaderLabels(self.columns)
        
        # Set column widths
        header = self.table.horizontalHeader()
        for i in range(len(self.columns)):
            if i < 3:  # Name, Type, Material
                header.setSectionResizeMode(i, QHeaderView.ResizeToContents)
            else:
                header.setSectionResizeMode(i, QHeaderView.Interactive)
                self.table.setColumnWidth(i, 100)
        
        # Enable editing for price columns only
        self.table.setEditTriggers(QtWidgets.QAbstractItemView.DoubleClicked)
        self.table.itemChanged.connect(self.on_item_changed)
        
    def load_objects_from_document(self):
        """Load objects from current FreeCAD document"""
        if not FreeCAD.ActiveDocument:
            return
            
        objects = FreeCAD.ActiveDocument.Objects
        self.table.setRowCount(len(objects))
        
        for row, obj in enumerate(objects):
            props = self.calculator.get_object_properties(obj)
            
            # Fill non-editable columns
            for col, (key, value) in enumerate(props.items()):
                if col < 10:  # First 10 columns are from object properties
                    item = QTableWidgetItem(str(value))
                    if col < 10:  # Make first 10 columns read-only
                        item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                    self.table.setItem(row, col, item)
            
            # Add editable price columns
            for col in range(10, 15):
                item = QTableWidgetItem("0")
                if col in [10, 11]:  # Material/unit and Labor/unit are editable
                    item.setFlags(item.flags() | Qt.ItemIsEditable)
                else:  # Total columns are calculated
                    item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                self.table.setItem(row, col, item)
        
        self.calculate_totals()
        
    def on_item_changed(self, item):
        """Handle item changes in table"""
        row = item.row()
        col = item.column()
        
        # Only process changes to editable columns (Material/unit, Labor/unit)
        if col in [10, 11]:
            self.calculate_row_totals(row)
            self.update_grand_total()
    
    def calculate_row_totals(self, row):
        """Calculate totals for a specific row"""
        try:
            # Block signals temporarily to prevent infinite loops
            self.table.blockSignals(True)
            
            # Get values
            quantity_item = self.table.item(row, 8)  # Quantity column
            material_unit_item = self.table.item(row, 10)  # Material/unit
            labor_unit_item = self.table.item(row, 11)  # Labor/unit
            
            if not all([quantity_item, material_unit_item, labor_unit_item]):
                return
                
            quantity = float(quantity_item.text() or 0)
            material_unit = float(material_unit_item.text() or 0)
            labor_unit = float(labor_unit_item.text() or 0)
            
            # Calculate totals
            material_total = self.calculator.calculate_material_total(quantity, material_unit)
            labor_total = self.calculator.calculate_labor_total(quantity, labor_unit)
            row_total = self.calculator.calculate_row_total(material_total, labor_total)
            
            # Update total columns
            self.table.setItem(row, 12, QTableWidgetItem(f"{material_total:.2f}"))
            self.table.setItem(row, 13, QTableWidgetItem(f"{labor_total:.2f}"))
            self.table.setItem(row, 14, QTableWidgetItem(f"{row_total:.2f}"))
            
            # Make total columns read-only
            for col in [12, 13, 14]:
                item = self.table.item(row, col)
                if item:
                    item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                    
        except (ValueError, TypeError) as e:
            FreeCAD.Console.PrintError(f"Error calculating row totals: {e}\n")
        finally:
            # Re-enable signals
            self.table.blockSignals(False)
    
    def calculate_totals(self):
        """Calculate all row totals"""
        for row in range(self.table.rowCount()):
            self.calculate_row_totals(row)
        self.update_grand_total()
    
    def update_grand_total(self):
        """Update the grand total display"""
        try:
            total = 0.0
            for row in range(self.table.rowCount()):
                total_item = self.table.item(row, 14)  # Total column
                if total_item:
                    total += float(total_item.text() or 0)
            
            self.grand_total_label.setText(f"Grand Total: {total:,.2f}")
            
        except (ValueError, TypeError) as e:
            FreeCAD.Console.PrintError(f"Error updating grand total: {e}\n")
    
    def refresh_data(self):
        """Refresh data from FreeCAD document"""
        self.load_objects_from_document()
        FreeCAD.Console.PrintMessage("Data refreshed\n")
    
    def show_object_info_dialog(self):
        """Show detailed object information dialog"""
        try:
            # Import with absolute path
            import sys
            import os
            module_path = os.path.dirname(os.path.dirname(__file__))
            if module_path not in sys.path:
                sys.path.insert(0, module_path)
            
            from dialogs.object_info_dialog import ObjectInfoDialog
            
            # Get current document objects
            if not FreeCAD.ActiveDocument:
                QMessageBox.warning(self, "Warning", "No active document found!")
                return
                
            objects = FreeCAD.ActiveDocument.Objects
            if not objects:
                QMessageBox.information(self, "Information", "No objects found in document!")
                return
            
            # Show object info dialog
            dialog = ObjectInfoDialog(objects, self)
            dialog.exec_()
            
        except Exception as e:
            FreeCAD.Console.PrintError(f"Error showing object info dialog: {e}\n")
            QMessageBox.critical(self, "Error", f"Error showing object info dialog: {e}")
    
    def export_to_csv(self):
        """Export table data to CSV file"""
        try:
            filename, _ = QFileDialog.getSaveFileName(
                self, "Export to CSV", "", "CSV Files (*.csv)")
            
            if filename:
                with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                    writer = csv.writer(csvfile)
                    
                    # Write headers
                    writer.writerow(self.columns)
                    
                    # Write data
                    for row in range(self.table.rowCount()):
                        row_data = []
                        for col in range(self.table.columnCount()):
                            item = self.table.item(row, col)
                            row_data.append(item.text() if item else "")
                        writer.writerow(row_data)
                
                QMessageBox.information(self, "Success", f"Data exported to {filename}")
                FreeCAD.Console.PrintMessage(f"Data exported to {filename}\n")
                
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error exporting data: {e}")
            FreeCAD.Console.PrintError(f"Error exporting data: {e}\n")

# Global dialog instance
_main_dialog = None

def show_main_dialog():
    """Show the main BOQ dialog"""
    global _main_dialog
    
    try:
        if _main_dialog is None:
            _main_dialog = QuantityTakeoffMainDialog()
        
        _main_dialog.show()
        _main_dialog.raise_()
        _main_dialog.activateWindow()
        
    except Exception as e:
        FreeCAD.Console.PrintError(f"Error showing main dialog: {e}\n")
        
def add_selected_objects(objects):
    """Add selected objects to the main dialog table"""
    global _main_dialog
    
    if _main_dialog:
        _main_dialog.refresh_data()
    else:
        FreeCAD.Console.PrintMessage("Please open the main dialog first\n")
