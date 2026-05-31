# -*- coding: UTF-8 -*-

from pyrevit import revit, DB
#importaciones basicas
doc = revit.doc
view = revit.active_view

# incluyenfdo las referencias de los elementos seleccionados

opt = DB.Options()
opt.ComputeReferences = True
opt.View = view


#Todos los muros

muros = DB.FilteredElementCollector(doc, view.Id)\
    .OfCategory(DB.BuiltInCategory.OST_Walls)\
    .WhereElementIsNotElementType().ToElements()


# lista de lineas de referencia ( ReferenceArray)

ref_array = DB.ReferenceArray()

for muro in muros:
    geom = muro.get_Geometry(opt)
    for obj in geom:
        if obj.GetType().Name == 'Solid':
            for cara in obj.Faces:
                normal = cara.FaceNormal

                if abs(normal.Z) < 0.01:
                    ref_array.Append(cara.Reference)
                    break

# BoundingBox de todos los muros para saber dónde estan
bb = view.get_BoundingBox(None)
min_pt = bb.Min
max_pt = bb.Max

# La linea va de lado a lado de la vista, un poco mas arriba del modelo
pt1 = DB.XYZ(min_pt.X - 5, max_pt.Y + 3, 0)
pt2 = DB.XYZ(max_pt.X + 5, max_pt.Y + 3, 0)
linea = DB.Line.CreateBound(pt1, pt2)


# Diagnostico
print("Muros encontrados:", len(list(muros)))
print("Referencias encontradas:", ref_array.Size)

#creacion de cota
with revit.Transaction('Crear cota'):
    doc.Create.NewDimension(view, linea, ref_array)

