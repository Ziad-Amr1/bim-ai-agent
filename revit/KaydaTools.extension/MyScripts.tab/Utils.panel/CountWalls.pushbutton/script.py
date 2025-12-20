from Autodesk.Revit.DB import FilteredElementCollector, Wall
from pyrevit import revit, DB

doc = revit.doc

walls = FilteredElementCollector(doc).OfClass(Wall).ToElements()

print("Number of walls:", len(walls))