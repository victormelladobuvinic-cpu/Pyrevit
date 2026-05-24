# -*- coding: UTF-8 -*-
# Importaciones obligatorias en todo script de PyRevit
import clr
clr.AddReference('RevitAPI')
clr.AddReference('RevitAPIUI')

from Autodesk.Revit.DB import *
from Autodesk.Revit.UI import TaskDialog

# pyrevit te da acceso fácil al documento activo
from pyrevit import revit, DB

# Acceso al modelo y la UI
doc    = revit.doc       # El documento de Revit abierto
uidoc  = revit.uidoc     # La interfaz de usuario

# --- Tu lógica va aquí ---
nombre_modelo = doc.Title

# Mostrar resultado en un cuadro de diálogo nativo de Revit
TaskDialog.Show(
    "Mi primer script",
    "Modelo activo: {}".format(nombre_modelo)
)