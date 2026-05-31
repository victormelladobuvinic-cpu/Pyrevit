# -*- coding: utf-8 -*-
import json
from pyrevit import revit
from pyrevit import DB
from pyrevit import forms

doc = revit.doc
view = doc.ActiveView

# Obtener puertas de la vista actual
puertas = (
    DB.FilteredElementCollector(doc, view.Id)
    .OfCategory(DB.BuiltInCategory.OST_Doors)
    .WhereElementIsNotElementType()
    .ToElements()
)

diccionario_conteo = {}

for puerta in puertas:
    # 1. Obtener Familia y Tipo de forma segura
    nombre_familia = puerta.Symbol.Family.Name
    nombre_tipo = puerta.Symbol.get_Parameter(DB.BuiltInParameter.SYMBOL_NAME_PARAM).AsString()
    
    # 2. Construir la clave

    clave = (nombre_familia, nombre_tipo)

    if clave not in diccionario_conteo:
        diccionario_conteo[clave] = 0
    diccionario_conteo[clave] += 1

    
# Crear lista par UI

lista_ui = []

for clave, cantidad in diccionario_conteo.items():

    familia = clave[0]
    tipo = clave[1]

    texto "{}: {} [{}]".format( familia, tipo, cantidad)

lista_ui.append(texto)

# Mostrar resultados en UI

seleccion = forms.SelectFromList.show(
    lista_ui,
    title="seleciona puertas",
    multiselect=True
)

forms.alert(str(seleccion))


