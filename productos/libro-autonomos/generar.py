#!/usr/bin/env python3
"""Genera Libro-Autonomos.xlsx: libro de ingresos y gastos con resumen trimestral (estimación 303 y 130)."""
import sys
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.formatting.rule import FormulaRule
from openpyxl.chart import BarChart, Reference

N = 400  # filas de datos por hoja
AZUL, CLARO, GRIS, VERDE = "1F4E79", "DDEBF7", "F2F2F2", "E2EFDA"
H = Font(bold=True, color="FFFFFF"); B = Font(bold=True)
fillH = PatternFill("solid", fgColor=AZUL); fillIn = PatternFill("solid", fgColor="FFFFFF"); fillCalc = PatternFill("solid", fgColor=GRIS)
thin = Side(style="thin", color="BFBFBF"); box = Border(left=thin, right=thin, top=thin, bottom=thin)
EUR = '#,##0.00 "€";[Red]-#,##0.00 "€"'; PCT = '0%'; FECHA = 'DD/MM/YYYY'

def cab(ws, fila, cols, anchos):
    for i, (t, w) in enumerate(zip(cols, anchos), 1):
        c = ws.cell(fila, i, t); c.font = H; c.fill = fillH; c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True); c.border = box
        ws.column_dimensions[c.column_letter].width = w
    ws.row_dimensions[fila].height = 32

def titulo(ws, t, sub):
    ws["A1"] = t; ws["A1"].font = Font(bold=True, size=16, color=AZUL)
    ws["A2"] = sub; ws["A2"].font = Font(italic=True, color="595959")

wb = Workbook()
# ---------- Instrucciones ----------
ins = wb.active; ins.title = "Instrucciones"
ins.column_dimensions["A"].width = 110
lineas = [
 ("Libro de ingresos y gastos para autónomos", Font(bold=True, size=18, color=AZUL)),
 ("Registra tus facturas emitidas y tus gastos; la hoja calcula sola el IVA y el pago fraccionado de cada trimestre.", None),
 ("", None),
 ("CÓMO SE USA", B),
 ("1. En 'Ajustes' escribe el año, tu nombre y los porcentajes que más usas (IVA y retención).", None),
 ("2. En 'Ingresos' añade una fila por factura emitida: fecha, número, cliente, base imponible, % IVA y % retención.", None),
 ("3. En 'Gastos' añade una fila por factura recibida: fecha, proveedor, categoría, base, % IVA y si es deducible.", None),
 ("4. 'Trimestres' muestra la estimación de los modelos 303 (IVA) y 130 (pago fraccionado de IRPF) de T1 a T4.", None),
 ("5. 'Resumen' da el total del año y un gráfico de ingresos y gastos por mes.", None),
 ("Rellena solo las celdas blancas: las grises se calculan solas. Puedes dejar el % vacío para usar el de 'Ajustes'.", None),
 ("", None),
 ("CÓMO CALCULA", B),
 ("• 303: IVA repercutido de tus facturas − IVA soportado de los gastos marcados como deducibles. Si sale negativo, es a compensar.", None),
 ("• 130: 20 % del rendimiento neto acumulado del año (ingresos − gastos deducibles, sin IVA) − retenciones acumuladas que te han", None),
 ("   practicado − pagos fraccionados de los trimestres anteriores. Si sale negativo, el resultado es 0.", None),
 ("• Si al menos el 70 % de tus ingresos del año anterior llevaron retención, normalmente no tienes que presentar el 130.", None),
 ("", None),
 ("AVISO IMPORTANTE", B),
 ("Es una herramienta de control y estimación, no un programa oficial ni asesoramiento fiscal. No contempla casos especiales", None),
 ("(recargo de equivalencia, prorrata, régimen de módulos, operaciones intracomunitarias, gastos de difícil justificación, etc.).", None),
 ("Comprueba siempre las cifras en la sede electrónica de la Agencia Tributaria o con tu asesor antes de presentar nada.", None),
]
for i, (t, f) in enumerate(lineas, 1):
    c = ins.cell(i, 1, t); c.alignment = Alignment(wrap_text=True, vertical="top")
    if f: c.font = f

# ---------- Ajustes ----------
aj = wb.create_sheet("Ajustes"); titulo(aj, "Ajustes", "Cambia solo las celdas blancas.")
aj.column_dimensions["A"].width = 34; aj.column_dimensions["B"].width = 22
filas = [("Año", 2027, "0"), ("Nombre / actividad", "", "@"), ("% IVA habitual", 0.21, PCT), ("% retención IRPF habitual", 0.15, PCT), ("% pago fraccionado (modelo 130)", 0.20, PCT)]
for i, (k, v, fmt) in enumerate(filas, 4):
    aj.cell(i, 1, k).font = B
    c = aj.cell(i, 2, v); c.number_format = fmt; c.border = box; c.fill = fillIn
aj["A10"] = "Categorías de gasto (puedes editarlas):"; aj["A10"].font = B
cats = ["Suministros", "Alquiler local", "Material de oficina", "Software y suscripciones", "Teléfono e internet", "Formación", "Gestoría y asesoría", "Seguros", "Cuota de autónomos", "Publicidad", "Transporte y viajes", "Equipos (amortización)", "Bancos y comisiones", "Otros"]
for i, c in enumerate(cats, 11):
    aj.cell(i, 1, c).border = box
from openpyxl.workbook.defined_name import DefinedName
wb.defined_names["Categorias"] = DefinedName("Categorias", attr_text="Ajustes!$A$11:$A$30")
wb.defined_names["IVAdef"] = DefinedName("IVAdef", attr_text="Ajustes!$B$6")
wb.defined_names["RETdef"] = DefinedName("RETdef", attr_text="Ajustes!$B$7")
wb.defined_names["PCT130"] = DefinedName("PCT130", attr_text="Ajustes!$B$8")
wb.defined_names["Anio"] = DefinedName("Anio", attr_text="Ajustes!$B$4")

# ---------- Ingresos ----------
ing = wb.create_sheet("Ingresos"); titulo(ing, "Ingresos (facturas emitidas)", "Una fila por factura. Columnas grises: automáticas.")
cols = ["Fecha", "Nº factura", "Cliente", "NIF cliente", "Base imponible", "% IVA", "Cuota IVA", "% retención", "Retención", "Total a cobrar", "Cobrada (Sí/No)", "Trim."]
cab(ing, 4, cols, [12, 12, 28, 13, 15, 8, 13, 11, 13, 15, 10, 7])
R0 = 5
for r in range(R0, R0 + N):
    f = lambda col: f"{col}{r}"
    ing[f("G")] = f'=IF(E{r}="","",ROUND(E{r}*IF(F{r}="",IVAdef,F{r}),2))'
    ing[f("I")] = f'=IF(E{r}="","",ROUND(E{r}*IF(H{r}="",RETdef,H{r}),2))'
    ing[f("J")] = f'=IF(E{r}="","",E{r}+G{r}-I{r})'
    ing[f("L")] = f'=IF(OR(A{r}="",E{r}=""),"",IF(YEAR(A{r})<>Anio,"Otro año",ROUNDUP(MONTH(A{r})/3,0)))'
    for col, fmt in zip("ABCDEFGHIJKL", [FECHA, "@", "@", "@", EUR, PCT, EUR, PCT, EUR, EUR, "@", "0"]):
        c = ing[f(col)]; c.number_format = fmt; c.border = box
        if col in "GIJL": c.fill = fillCalc
ing.freeze_panes = "A5"
# ---------- Gastos ----------
gas = wb.create_sheet("Gastos"); titulo(gas, "Gastos (facturas recibidas)", "Marca 'No' en Deducible si el gasto no está afecto a tu actividad.")
cols = ["Fecha", "Proveedor", "Concepto", "Categoría", "Base imponible", "% IVA", "Cuota IVA", "Deducible (Sí/No)", "Total pagado", "Trim."]
cab(gas, 4, cols, [12, 24, 30, 24, 15, 8, 13, 12, 15, 7])
for r in range(R0, R0 + N):
    gas[f"G{r}"] = f'=IF(E{r}="","",ROUND(E{r}*IF(F{r}="",IVAdef,F{r}),2))'
    gas[f"I{r}"] = f'=IF(E{r}="","",E{r}+G{r})'
    gas[f"J{r}"] = f'=IF(OR(A{r}="",E{r}=""),"",IF(YEAR(A{r})<>Anio,"Otro año",ROUNDUP(MONTH(A{r})/3,0)))'
    for col, fmt in zip("ABCDEFGHIJ", [FECHA, "@", "@", "@", EUR, PCT, EUR, "@", EUR, "0"]):
        c = gas[f"{col}{r}"]; c.number_format = fmt; c.border = box
        if col in "GIJ": c.fill = fillCalc
gas.freeze_panes = "A5"
last = R0 + N - 1
# validaciones
dvSN = DataValidation(type="list", formula1='"Sí,No"', allow_blank=True)
dvCat = DataValidation(type="list", formula1="=Categorias", allow_blank=True)
dvF = DataValidation(type="date", operator="between", formula1="DATE(2000,1,1)", formula2="DATE(2100,12,31)", allow_blank=True, error="Escribe una fecha válida (dd/mm/aaaa).", showErrorMessage=True)
dvP = DataValidation(type="decimal", operator="between", formula1="0", formula2="1", allow_blank=True, error="Escribe un porcentaje entre 0 % y 100 %.", showErrorMessage=True)
dvF2 = DataValidation(type="date", operator="between", formula1="DATE(2000,1,1)", formula2="DATE(2100,12,31)", allow_blank=True, error="Escribe una fecha válida (dd/mm/aaaa).", showErrorMessage=True)
dvP2 = DataValidation(type="decimal", operator="between", formula1="0", formula2="1", allow_blank=True, error="Escribe un porcentaje entre 0 % y 100 %.", showErrorMessage=True)
dvSN2 = DataValidation(type="list", formula1='"Sí,No"', allow_blank=True)
for ws, dvs in ((ing, (dvSN, dvF, dvP)), (gas, (dvCat, dvF2, dvP2, dvSN2))):
    for d in dvs: ws.add_data_validation(d)
dvSN.add(f"K{R0}:K{last}"); dvF.add(f"A{R0}:A{last}"); dvP.add(f"F{R0}:F{last}"); dvP.add(f"H{R0}:H{last}")
dvCat.add(f"D{R0}:D{last}"); dvF2.add(f"A{R0}:A{last}"); dvP2.add(f"F{R0}:F{last}"); dvSN2.add(f"H{R0}:H{last}")
rojo = PatternFill("solid", fgColor="F8CBAD")
ing.conditional_formatting.add(f"K{R0}:K{last}", FormulaRule(formula=[f'AND($E{R0}<>"",$K{R0}="No")'], fill=rojo))
for ws, col in ((ing, "L"), (gas, "J")):
    ws.conditional_formatting.add(f"{col}{R0}:{col}{last}", FormulaRule(formula=[f'${col}{R0}="Otro año"'], fill=rojo))

# ---------- Trimestres ----------
tr = wb.create_sheet("Trimestres"); titulo(tr, "Resumen trimestral (estimación)", "Modelos 303 y 130. Compruébalo siempre antes de presentar.")
tr.column_dimensions["A"].width = 48
for i, t in enumerate(["T1 (ene-mar)", "T2 (abr-jun)", "T3 (jul-sep)", "T4 (oct-dic)"]):
    c = tr.cell(4, 2 + i, t); c.font = H; c.fill = fillH; c.alignment = Alignment(horizontal="center"); tr.column_dimensions[c.column_letter].width = 16
tr.cell(4, 1, "Concepto").font = H; tr.cell(4, 1).fill = fillH
IL, GL = f"Ingresos!$L${R0}:$L${last}", f"Gastos!$J${R0}:$J${last}"
rng = lambda h, c: f"{h}!${c}${R0}:${c}${last}"
filas = [
 ("IVA (modelo 303)", None),
 ("Base imponible facturada", lambda q, C: f'=SUMIFS({rng("Ingresos","E")},{IL},{q})'),
 ("IVA repercutido", lambda q, C: f'=SUMIFS({rng("Ingresos","G")},{IL},{q})'),
 ("IVA soportado deducible", lambda q, C: f'=SUMIFS({rng("Gastos","G")},{GL},{q},{rng("Gastos","H")},"<>No")'),
 ("Resultado 303 (positivo = a ingresar)", lambda q, C: f"={C}7-{C}8"),
 ("IRPF (modelo 130)", None),
 ("Ingresos del trimestre (sin IVA)", lambda q, C: f"={C}6"),
 ("Gastos deducibles del trimestre (sin IVA)", lambda q, C: f'=SUMIFS({rng("Gastos","E")},{GL},{q},{rng("Gastos","H")},"<>No")'),
 ("Rendimiento neto acumulado del año", lambda q, C: f"=SUM($B11:{C}11)-SUM($B12:{C}12)"),
 ("20 % del rendimiento acumulado", lambda q, C: f"=MAX(0,{C}13*PCT130)"),
 ("Retenciones acumuladas", lambda q, C: f'=SUMIFS({rng("Ingresos","I")},{IL},"<="&{q})'),
 ("Pagos fraccionados de trimestres anteriores", lambda q, C: "=0" if C == "B" else f"=SUM($B17:{chr(ord(C)-1)}17)"),
 ("Resultado 130 a ingresar", lambda q, C: f"=MAX(0,{C}14-{C}15-{C}16)"),
]
orden = list(range(5, 18))
for (t, fn), r in zip(filas, orden):
    a = tr.cell(r, 1, t)
    if fn is None:
        a.font = Font(bold=True, color=AZUL); continue
    a.border = box
    for i, C in enumerate("BCDE"):
        c = tr[f"{C}{r}"]; c.value = fn(i + 1, C); c.number_format = EUR; c.border = box; c.fill = fillCalc
for r in (9, 17):
    tr.cell(r, 1).font = B
    for C in "BCDE": tr[f"{C}{r}"].font = B; tr[f"{C}{r}"].fill = PatternFill("solid", fgColor=VERDE)
tr["A19"] = "Facturas emitidas sin cobrar (importe pendiente):"; tr["A19"].font = B
tr["B19"] = f'=SUMIFS({rng("Ingresos","J")},{rng("Ingresos","K")},"No")'; tr["B19"].number_format = EUR
tr["A20"] = "Filas con fecha de otro año (revisa):"; tr["A20"].font = B
tr["B20"] = f'=COUNTIF({IL},"Otro año")+COUNTIF({GL},"Otro año")'

# ---------- Resumen ----------
rs = wb.create_sheet("Resumen"); titulo(rs, "Resumen del año", "Ingresos y gastos por mes (sin IVA).")
for i, (t, w) in enumerate([("Mes", 14), ("Ingresos", 16), ("Gastos deducibles", 18), ("Rendimiento", 16)], 1):
    c = rs.cell(4, i, t); c.font = H; c.fill = fillH; rs.column_dimensions[c.column_letter].width = w
meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
for m, nom in enumerate(meses, 1):
    r = 4 + m; rs.cell(r, 1, nom).border = box
    ini, fin = f"DATE(Anio,{m},1)", f"EOMONTH(DATE(Anio,{m},1),0)"
    rs[f"B{r}"] = f'=SUMIFS({rng("Ingresos","E")},{rng("Ingresos","A")},">="&{ini},{rng("Ingresos","A")},"<="&{fin})'
    rs[f"C{r}"] = f'=SUMIFS({rng("Gastos","E")},{rng("Gastos","A")},">="&{ini},{rng("Gastos","A")},"<="&{fin},{rng("Gastos","H")},"<>No")'
    rs[f"D{r}"] = f"=B{r}-C{r}"
    for C in "BCD": rs[f"{C}{r}"].number_format = EUR; rs[f"{C}{r}"].border = box; rs[f"{C}{r}"].fill = fillCalc
rs["A17"] = "TOTAL"; rs["A17"].font = B
for C in "BCD":
    rs[f"{C}17"] = f"=SUM({C}5:{C}16)"; rs[f"{C}17"].number_format = EUR; rs[f"{C}17"].font = B
ch = BarChart(); ch.title = "Ingresos y gastos por mes"; ch.y_axis.title = "€"; ch.height = 8; ch.width = 18
ch.add_data(Reference(rs, min_col=2, max_col=3, min_row=4, max_row=16), titles_from_data=True)
ch.set_categories(Reference(rs, min_col=1, min_row=5, max_row=16)); rs.add_chart(ch, "F4")

for ws in wb.worksheets: ws.sheet_view.showGridLines = ws.title not in ("Instrucciones",)
wb.active = 0
out = sys.argv[1] if len(sys.argv) > 1 else "Libro-Autonomos.xlsx"
if len(sys.argv) > 2:  # datos de prueba
    import datetime as d
    I = [(d.date(2027,1,15),1000,None,None),(d.date(2027,2,10),500,0.21,0),(d.date(2027,5,3),2000,None,0.07),(d.date(2027,11,30),800,0.10,None),(d.date(2026,12,30),999,None,None)]
    for i,(f,b,iv,rt) in enumerate(I):
        r=R0+i; ing[f"A{r}"]=f; ing[f"E{r}"]=b; ing[f"F{r}"]=iv; ing[f"H{r}"]=rt; ing[f"K{r}"]="No" if i==1 else "Sí"
    G = [(d.date(2027,1,20),200,None,"Sí"),(d.date(2027,3,5),100,0.21,"No"),(d.date(2027,4,1),300,0.10,None),(d.date(2027,12,1),50,0,"Sí")]
    for i,(f,b,iv,de) in enumerate(G):
        r=R0+i; gas[f"A{r}"]=f; gas[f"E{r}"]=b; gas[f"F{r}"]=iv; gas[f"H{r}"]=de
wb.save(out); print("guardado", out)
