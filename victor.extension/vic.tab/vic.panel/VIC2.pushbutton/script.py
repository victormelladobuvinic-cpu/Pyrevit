# -*- coding: UTF-8 -*-
from pyrevit import revit, forms
from Autodesk.Revit.DB import FilteredElementCollector, Wall

doc   = revit.doc
uidoc = revit.uidoc

# FilteredElementCollector recibe el documento
# .OfClass(Wall) le dice "solo quiero muros"
# .ToElements() ejecuta la búsqueda y devuelve una lista

muros = FilteredElementCollector(doc)\
        .OfClass(Wall)\
        .ToElements()

# Ahora "muros" es una lista de objetos Wall
# Cada objeto tiene propiedades: Id, Name, etc.

resultado = "Muros encontrados: {}\n\n".format(len(muros))

for muro in muros[:5]:   # solo los primeros 5 para no saturar
    resultado += "- ID: {}  |  Tipo: {}\n".format(
        muro.Id,
        muro.Name
    )

forms.alert(resultado, title="FilteredElementCollector")