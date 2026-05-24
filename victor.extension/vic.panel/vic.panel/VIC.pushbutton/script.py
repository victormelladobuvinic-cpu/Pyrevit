# -*- coding: UTF-8 -*-
# Importaciones obligatorias en todo script de PyRevit
from Autoesl.Revit.DB import Transaction
from pyrevit import forms

# pyrevit te da acceso fácil al documento activo
from pyrevit import revit, DB

# Acceso al modelo y la UI
doc    = revit.doc       # El documento de Revit abierto
uidoc  = revit.uidoc     # La interfaz de usuario

# --- Tu lógica va aquí ---
nombre_modelo = doc.Title

# Mostrar resultado en un cuadro de diálogo nativo de Revit
forms.alert (
    "Modelo abierto: {}".format(nombre_modelo),
    title="Información del Modelo"
)