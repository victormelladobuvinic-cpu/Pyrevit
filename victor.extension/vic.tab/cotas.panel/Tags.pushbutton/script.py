# -*- coding: utf-8 -*-

from pyrevit import revit, DB, forms


doc = revit.doc
view = doc.ActiveView


# ---------------------------------------------------
# OBTENER PUERTAS
# ---------------------------------------------------

puertas = (
    DB.FilteredElementCollector(doc, view.Id)
    .OfCategory(DB.BuiltInCategory.OST_Doors)
    .WhereElementIsNotElementType()
    .ToElements()
)


# ---------------------------------------------------
# CREAR CATALOGO
# clave -> lista de puertas
# ---------------------------------------------------

catalogo_puertas = {}

for puerta in puertas:

    familia = puerta.Symbol.Family.Name

    tipo = puerta.Symbol.get_Parameter(
        DB.BuiltInParameter.SYMBOL_NAME_PARAM
    ).AsString()

    clave = (
        familia,
        tipo
    )

    if clave not in catalogo_puertas:

        catalogo_puertas[clave] = []

    catalogo_puertas[clave].append(
        puerta
    )


# ---------------------------------------------------
# CREAR LISTA PARA UI
# ---------------------------------------------------

lista_ui = []
mapa_ui = {}

for clave, lista_puertas in catalogo_puertas.items():

    familia, tipo = clave

    cantidad = len(
        lista_puertas
    )

    texto = "{} | {} [{}]".format(
        familia,
        tipo,
        cantidad
    )

    lista_ui.append(
        texto
    )

    mapa_ui[texto] = clave


# ---------------------------------------------------
# MOSTRAR UI
# ---------------------------------------------------

seleccion = forms.SelectFromList.show(
    sorted(lista_ui),
    title="Seleccione puertas",
    multiselect=True
)

claves_seleccionadas = []
puertas_seleccionadas = []

for texto in seleccion:

    clave = mapa_ui[texto]

    claves_seleccionadas.append(
        clave
    )

for clave in claves_seleccionadas:

    puertas_seleccionadas.extend(
        catalogo_puertas[clave]
    )
# ---------------------------------------------------
# TRANSACCION
# ---------------------------------------------------

t = DB.Transaction(doc, "Taguear puertas")
t.Start()



for puerta in puertas_seleccionadas:

    point = puerta.Location.Point
    tag_point = point + DB.XYZ(0, 2, 0)

    DB.IndependentTag.Create(
        doc,
        view.Id,
        DB.Reference(puerta),
        True,
        DB.TagMode.TM_ADDBY_CATEGORY,
        DB.TagOrientation.Horizontal,
        tag_point
    )
t.Commit()
# ---------------------------------------------------
# RESULTADO
# ---------------------------------------------------

if puertas_seleccionadas:

    forms.alert(
        "Seleccionaste {} puertas".format(
            len(puertas_seleccionadas)
        )
    )

else:

    forms.alert(
        "No se seleccionó nada"
    )