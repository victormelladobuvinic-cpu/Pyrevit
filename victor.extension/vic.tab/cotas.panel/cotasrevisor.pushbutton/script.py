# -*- coding: UTF-8 -*-
from pyrevit import revit, DB

doc = revit.doc
uidoc = revit.uidoc

# Buscar el elemento por su ID
dim_id = DB.ElementId(437838)
dim = doc.GetElement(dim_id)

if dim:
    print("Encontrada:", dim)
    print("Vista:", dim.OwnerViewId)
    # Seleccionarla en Revit para que la veamos
    uidoc.Selection.SetElementIds(
        DB.List[DB.ElementId]([dim_id])
    )
    uidoc.ShowElements(dim_id)
else:
    print("No existe")