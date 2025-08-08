import os
import sys
import types

# Stub the FreeCAD module used by calculations
sys.modules.setdefault('FreeCAD', types.SimpleNamespace(Console=types.SimpleNamespace(PrintError=lambda msg: None)))

# Ensure the repository root is on sys.path
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from utils.calculations import QTOCalculator


def test_calculate_material_total():
    assert QTOCalculator.calculate_material_total(10, 5) == 50
    assert QTOCalculator.calculate_material_total('a', 5) == 0.0


def test_calculate_labor_total():
    assert QTOCalculator.calculate_labor_total(8, 12) == 96
    assert QTOCalculator.calculate_labor_total('x', 10) == 0.0


def test_calculate_row_total():
    assert QTOCalculator.calculate_row_total(50, 25) == 75
    assert QTOCalculator.calculate_row_total('invalid', 25) == 0.0


def test_format_currency():
    assert QTOCalculator.format_currency(1234.5) == '1,234.50'
    assert QTOCalculator.format_currency('abc') == '0.00'


def test_format_quantity():
    assert QTOCalculator.format_quantity(12.34) == '12'
    assert QTOCalculator.format_quantity('abc') == '0'


def test_format_dimension():
    assert QTOCalculator.format_dimension(123.456) == '123.46'
    assert QTOCalculator.format_dimension('abc') == '0.00'
