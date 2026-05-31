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

if not walls:
    forms.alert("No se encontraron muros")
    raise Exception()

wall = walls[0]

curve = wall.Location.Curve

start_point = curve.GetEndPoint(0)
end_point = curve.GetEndPoint(1)

offset = DB.XYZ(0, 5, 0)

dim_line = DB.Line.CreateBound(
    start_point + offset,
    end_point + offset
)

options = DB.Options()
options.ComputeReferences = True

geometry = wall.get_Geometry(options)

references = []

for geo in geometry:

    if not isinstance(geo, DB.Solid):
        continue

    for face in geo.Faces:

        if face.Reference:
            references.append(face.Reference)

if len(references) < 2:
    forms.alert(
        "No se encontraron referencias suficientes"
    )
    raise Exception()

ref_array = DB.ReferenceArray()

ref_array.Append(references[0])
ref_array.Append(references[1])

t = DB.Transaction(
    doc,
    "Dimension Wall"
)

t.Start()

doc.Create.NewDimension(
    view,
    dim_line,
    ref_array
)

t.Commit()