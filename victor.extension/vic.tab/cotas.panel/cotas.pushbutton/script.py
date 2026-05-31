# codigo UTF-8

from pyrevit import revit, DB
#importaciones basicas
doc = revit.doc
view = revit.active_view

# incluyenfdo las referencias de los elementos seleccionados

opt = DB.Options()
opt.ComputeReferences = True
opt.view = view


#Todos los muros

muros = DB.FilteredElemntCollector(doc, view.Id)\
        .OfCategory(DB.BuiltInCategory.OST_Walls)\
        .WhereElementIsNotElementType().ToElements()


# lista de lineas de referencia ( ReferenceArray)

ref_array = DB.ReferenceArray()

for muri in muros:
    geom = muro.get_Geometry(opt)
    for obj in geom:
        if obj.GetType().Name == 'Solid':
            for cara in obj.Faces:
                normal = cara.FaceNormal

                if abs(normal.Z) < 0.01:
                    ref_array.Append(cara.Reference)
                    break

# definicion de linea de cota

pt1 = DB.XYZ(-10, 20, 0)
pt2 = DB.XYZ(50, 20, 0)
linea = DB.Line.CreateBound(pt1, pt2)

#creacion de cota

with revit.Transaction('Crear cota'):
    doc.Create.NewDimension(view, linea, ref_array)

