# -*- coding: utf-8 -*-
"""
ObjectInfoDialog - Dialog for displaying detailed object information
"""

try:
    from PySide2 import QtWidgets, QtCore, QtGui
    from PySide2.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QHeaderView, QMessageBox, QLabel, QLineEdit, QComboBox
    from PySide2.QtCore import Qt
    from PySide2.QtGui import QFont
except ImportError:
    try:
        from PyQt5 import QtWidgets, QtCore, QtGui
        from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QHeaderView, QMessageBox, QLabel, QLineEdit, QComboBox
        from PyQt5.QtCore import Qt
        from PyQt5.QtGui import QFont
    except ImportError as e:
        print(f"Error importing Qt modules: {e}")
        QtWidgets = None

import FreeCAD
import sys
import os

# Add the module path to sys.path for absolute imports
module_path = os.path.dirname(os.path.dirname(__file__))
if module_path not in sys.path:
    sys.path.insert(0, module_path)

from utils.calculations import QTOCalculator

class ObjectInfoDialog(QDialog):
    """
    Dialog for displaying detailed object information with filtering capabilities
    """
    
    def __init__(self, objects, parent=None):
        super().__init__(parent)
        self.objects = objects
        self.calculator = QTOCalculator()
        self.setupUI()
        self.setupTable()
        self.load_object_data()
        
    def setupUI(self):
        """Setup the user interface"""
        self.setWindowTitle("ข้อมูลชิ้นงานทั้งหมด - Object Information")
        self.setGeometry(150, 150, 1200, 700)
        
        # Main layout
        layout = QVBoxLayout(self)
        
        # Title
        title = QLabel("ข้อมูลชิ้นงานทั้งหมด - Detailed Object Information")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Arial", 14, QFont.Bold))
        layout.addWidget(title)
        
        # Filter section
        filter_layout = QHBoxLayout()
        
        filter_layout.addWidget(QLabel("กรองตาม Object Type:"))
        self.type_filter = QComboBox()
        self.type_filter.addItem("All Types")
        self.type_filter.currentTextChanged.connect(self.apply_filter)
        filter_layout.addWidget(self.type_filter)
        
        filter_layout.addWidget(QLabel("ค้นหาชื่อ:"))
        self.name_filter = QLineEdit()
        self.name_filter.setPlaceholderText("ใส่ชื่อชิ้นงานที่ต้องการค้นหา...")
        self.name_filter.textChanged.connect(self.apply_filter)
        filter_layout.addWidget(self.name_filter)
        
        clear_filter_btn = QPushButton("Clear Filter")
        clear_filter_btn.clicked.connect(self.clear_filters)
        filter_layout.addWidget(clear_filter_btn)
        
        filter_layout.addStretch()
        layout.addLayout(filter_layout)
        
        # Table
        self.table = QTableWidget()
        layout.addWidget(self.table)
        
        # Summary section
        summary_layout = QHBoxLayout()
        self.summary_label = QLabel("Total Objects: 0")
        self.summary_label.setFont(QFont("Arial", 10, QFont.Bold))
        summary_layout.addWidget(self.summary_label)
        summary_layout.addStretch()
        
        # Buttons
        button_layout = QHBoxLayout()
        
        refresh_btn = QPushButton("Refresh")
        refresh_btn.clicked.connect(self.refresh_data)
        button_layout.addWidget(refresh_btn)
        
        export_btn = QPushButton("Export Info")
        export_btn.clicked.connect(self.export_info)
        button_layout.addWidget(export_btn)
        
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.close)
        button_layout.addWidget(close_btn)
        
        button_layout.addStretch()
        summary_layout.addLayout(button_layout)
        layout.addLayout(summary_layout)
        
    def setupTable(self):
        """Setup the object information table"""
        # Extended columns for detailed object information
        self.columns = [
            "Object Name", "Label", "Object Type", "Material", 
            "Length (m)", "Width (m)", "Height (m)", "Volume (m³)", 
            "Area (m²)", "Quantity", "Unit Weight (kg)", "Status"
        ]
        
        self.table.setColumnCount(len(self.columns))
        self.table.setHorizontalHeaderLabels(self.columns)
        
        # Set column widths
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Interactive)
        
        # Set specific widths
        column_widths = [120, 120, 150, 100, 80, 80, 80, 100, 100, 80, 100, 80]
        for i, width in enumerate(column_widths):
            self.table.setColumnWidth(i, width)
        
        # Make table read-only
        self.table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        
        # Enable sorting
        self.table.setSortingEnabled(True)
        
        # Enable row selection
        self.table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        
    def load_object_data(self):
        """Load object data into the table"""
        self.all_data = []  # Store all data for filtering
        
        for obj in self.objects:
            props = self.calculator.get_object_properties(obj)
            
            # Add status information
            status = "Active"
            if hasattr(obj, 'Visibility') and not obj.Visibility:
                status = "Hidden"
            
            row_data = [
                props['Name'],
                props.get('Label', props['Name']),
                props['Type'],
                props['Material'],
                f"{props['Length']:.2f}",
                f"{props['Width']:.2f}",
                f"{props['Height']:.2f}",
                f"{props['Volume']:.6f}",
                f"{props['Area']:.2f}",
                str(props['Quantity']),
                f"{props['Unit_Weight']:.2f}",
                status
            ]
            
            self.all_data.append(row_data)
        
        # Populate type filter
        self.populate_type_filter()
        
        # Display all data initially
        self.display_data(self.all_data)
        
    def populate_type_filter(self):
        """Populate the type filter combobox"""
        types = set()
        for row_data in self.all_data:
            types.add(row_data[2])  # Object Type column
        
        self.type_filter.clear()
        self.type_filter.addItem("All Types")
        for obj_type in sorted(types):
            self.type_filter.addItem(obj_type)
    
    def display_data(self, data):
        """Display data in the table"""
        self.table.setRowCount(len(data))
        
        for row, row_data in enumerate(data):
            for col, value in enumerate(row_data):
                item = QTableWidgetItem(str(value))
                
                # Color coding based on object type
                if col == 2:  # Object Type column
                    if "Part::Feature" in value:
                        item.setBackground(QtGui.QColor(230, 255, 230))  # Light green
                    elif "Beam" in value:
                        item.setBackground(QtGui.QColor(255, 240, 230))  # Light orange
                    elif "Column" in value:
                        item.setBackground(QtGui.QColor(230, 240, 255))  # Light blue
                
                # Status color coding
                if col == 11:  # Status column
                    if value == "Hidden":
                        item.setBackground(QtGui.QColor(255, 230, 230))  # Light red
                
                self.table.setItem(row, col, item)
        
        # Update summary
        self.summary_label.setText(f"Total Objects: {len(data)}")
    
    def apply_filter(self):
        """Apply filters to the data"""
        filtered_data = []
        
        type_filter = self.type_filter.currentText()
        name_filter = self.name_filter.text().lower()
        
        for row_data in self.all_data:
            # Type filter
            if type_filter != "All Types" and type_filter not in row_data[2]:
                continue
            
            # Name filter
            if name_filter and name_filter not in row_data[0].lower() and name_filter not in row_data[1].lower():
                continue
            
            filtered_data.append(row_data)
        
        self.display_data(filtered_data)
    
    def clear_filters(self):
        """Clear all filters"""
        self.type_filter.setCurrentText("All Types")
        self.name_filter.clear()
        self.display_data(self.all_data)
    
    def refresh_data(self):
        """Refresh object data"""
        if FreeCAD.ActiveDocument:
            self.objects = FreeCAD.ActiveDocument.Objects
            self.load_object_data()
            FreeCAD.Console.PrintMessage("Object information refreshed\n")
    
    def export_info(self):
        """Export object information to CSV"""
        try:
            from PySide2.QtWidgets import QFileDialog
        except ImportError:
            from PyQt5.QtWidgets import QFileDialog
        
        filename, _ = QFileDialog.getSaveFileName(
            self, "Export Object Info", "", "CSV Files (*.csv)")
        
        if filename:
            import csv
            
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                
                # Write headers
                writer.writerow(self.columns)
                
                # Write current displayed data
                for row in range(self.table.rowCount()):
                    row_data = []
                    for col in range(self.table.columnCount()):
                        item = self.table.item(row, col)
                        row_data.append(item.text() if item else "")
                    writer.writerow(row_data)
            
            QMessageBox.information(self, "Success", f"Object information exported to {filename}")
            FreeCAD.Console.PrintMessage(f"Object information exported to {filename}\n")
