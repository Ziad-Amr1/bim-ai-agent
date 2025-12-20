from Autodesk.Revit.DB import FilteredElementCollector, View

def rename_views(old_prefix, new_prefix):
    doc = revit.doc
    views = FilteredElementCollector(doc).OfClass(View).ToElements()

    renamed = 0
    t = DB.Transaction(doc, "Rename Views")
    t.Start()

    for v in views:
        if not v.IsTemplate and v.Name.startswith(old_prefix):
            v.Name = v.Name.replace(old_prefix, new_prefix, 1)
            renamed += 1

    t.Commit()
    return renamed
