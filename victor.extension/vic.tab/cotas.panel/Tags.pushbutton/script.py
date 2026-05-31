from pyrevit import revit
from pyrevit import DB
from pyrevit import forms

doc = revit.doc
view = doc.ActiveView

walls = (
    DB.FilteredElementCollector(doc, view.Id)
    .OfClass(DB.Wall)
    .WhereElementIsNotElementType()
    .ToElements()
)

ventanas =  (
    DB.FilteredElementCollector(doc, view.Id)
    .OfClass(DB.Window)
    .WhereElementIsNotElementType()
    .ToElements()
)

t = DB.Transaction(doc, "Auto Tag")

t.Start()

for ventana in ventanas:

    curve = ventana.Location.Curve

    midpoint = curve.Evaluate(
        0.5,
        True
    )

    reference = DB.Reference(ventana)

    DB.IndependentTag.Create(
        doc,
        view.Id,
        reference,
        False,
        DB.TagMode.TM_ADDBY_CATEGORY,
        DB.TagOrientation.Horizontal,
        midpoint,
        DB.XYZ(50, 0, 0)
    )

t.Commit()


forms.alert("Etiquetas creadas")
forms.alert("se etiquetaron {} ventanas".format(len(ventanas)))
