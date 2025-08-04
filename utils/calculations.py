# -*- coding: utf-8 -*-
"""
QTOCalculator - Calculation utilities for Quantity Takeoff
"""

import FreeCAD

class QTOCalculator:
    """
    Calculator class for Quantity Takeoff operations
    """
    
    @staticmethod
    def get_object_properties(obj):
        """Extract properties from FreeCAD object"""
        try:
            properties = {
                'Name': obj.Name,
                'Label': obj.Label,
                'Type': obj.TypeId,
                'Material': getattr(obj, 'Material', 'Unknown'),
                'Length': 0.0,
                'Width': 0.0,
                'Height': 0.0,
                'Volume': 0.0,
                'Area': 0.0,
                'Quantity': 1,
                'Unit_Weight': 0.0
            }
            
            # Get dimensions based on object type
            if hasattr(obj, 'Shape') and obj.Shape:
                bbox = obj.Shape.BoundBox
                # Convert from mm to m
                properties['Length'] = round(bbox.XLength / 1000, 2)
                properties['Width'] = round(bbox.YLength / 1000, 2) 
                properties['Height'] = round(bbox.ZLength / 1000, 2)
                properties['Volume'] = round(obj.Shape.Volume / 1000000000, 6)  # mm³ to m³
                
                # Calculate area (using bounding box approximation)
                if properties['Height'] > 0:
                    properties['Area'] = round((properties['Length'] * properties['Width']), 2)
            
            # Try to get specific properties for different object types
            if hasattr(obj, 'Length'):
                properties['Length'] = round(obj.Length.Value / 1000, 2)
            if hasattr(obj, 'Width'):
                properties['Width'] = round(obj.Width.Value / 1000, 2)
            if hasattr(obj, 'Height'):
                properties['Height'] = round(obj.Height.Value / 1000, 2)
                
            return properties
            
        except Exception as e:
            FreeCAD.Console.PrintError(f"Error extracting object properties: {e}\n")
            return {
                'Name': getattr(obj, 'Name', 'Unknown'),
                'Label': getattr(obj, 'Label', 'Unknown'),
                'Type': getattr(obj, 'TypeId', 'Unknown'),
                'Material': 'Unknown',
                'Length': 0.0,
                'Width': 0.0,
                'Height': 0.0,
                'Volume': 0.0,
                'Area': 0.0,
                'Quantity': 1,
                'Unit_Weight': 0.0
            }
    
    @staticmethod
    def calculate_material_total(quantity, material_per_unit):
        """Calculate material total cost"""
        try:
            return float(quantity) * float(material_per_unit)
        except (ValueError, TypeError):
            return 0.0
    
    @staticmethod
    def calculate_labor_total(quantity, labor_per_unit):
        """Calculate labor total cost"""
        try:
            return float(quantity) * float(labor_per_unit)
        except (ValueError, TypeError):
            return 0.0
    
    @staticmethod
    def calculate_row_total(material_total, labor_total):
        """Calculate total for a row"""
        try:
            return float(material_total) + float(labor_total)
        except (ValueError, TypeError):
            return 0.0
    
    @staticmethod
    def format_currency(value):
        """Format number as currency"""
        try:
            return f"{float(value):,.2f}"
        except (ValueError, TypeError):
            return "0.00"
    
    @staticmethod
    def format_quantity(value):
        """Format quantity value"""
        try:
            return f"{float(value):,.0f}"
        except (ValueError, TypeError):
            return "0"
    
    @staticmethod
    def format_dimension(value):
        """Format dimension value (meters)"""
        try:
            return f"{float(value):,.2f}"
        except (ValueError, TypeError):
            return "0.00"
