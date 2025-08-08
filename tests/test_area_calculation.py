import unittest
import types
import sys

try:
    import FreeCAD, Part  # type: ignore
    HAS_FREECAD = True
except Exception:  # ModuleNotFoundError or others
    HAS_FREECAD = False
    FreeCAD = types.SimpleNamespace(  # type: ignore
        Console=types.SimpleNamespace(PrintError=lambda msg: None)
    )
    sys.modules.setdefault("FreeCAD", FreeCAD)  # type: ignore
    Part = None  # type: ignore

from utils.calculations import QTOCalculator


class TestAreaCalculation(unittest.TestCase):
    @unittest.skipUnless(HAS_FREECAD, "FreeCAD not available")
    def test_shape_area_preferred(self):
        box = Part.makeBox(2000, 1000, 1000)  # dimensions in mm
        obj = type("Obj", (), {})()
        obj.Name = "Box"
        obj.Label = "Box"
        obj.TypeId = "Part::Box"
        obj.Shape = box
        properties = QTOCalculator.get_object_properties(obj)
        self.assertAlmostEqual(properties["Area"], round(box.Area / 1_000_000, 2))

    def test_bounding_box_fallback(self):
        class DummyBoundBox:
            XLength = 2000
            YLength = 1000
            ZLength = 1000

        class DummyShape:
            BoundBox = DummyBoundBox()
            Area = 0
            Volume = 2000 * 1000 * 1000

        obj = type("Obj", (), {})()
        obj.Name = "Dummy"
        obj.Label = "Dummy"
        obj.TypeId = "DummyType"
        obj.Shape = DummyShape()
        properties = QTOCalculator.get_object_properties(obj)
        expected_area = round(properties["Length"] * properties["Width"], 2)
        self.assertEqual(properties["Area"], expected_area)


if __name__ == "__main__":
    unittest.main()
