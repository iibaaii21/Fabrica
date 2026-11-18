#!/usr/bin/env python3
"""Genera Control-Alquileres.xlsx: control de pisos de alquiler (cobros, gastos, morosidad y rentabilidad).
Uso: python3 generar.py SALIDA.xlsx [--prueba]   (--prueba rellena datos de ejemplo para verificar)"""
import sys
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.formatting.rule import FormulaRule, CellIsRule
from openpyxl.chart import BarChart, Reference

OUT = sys.argv[1]; PRUEBA = '--prueba' in sys.argv
NI, NC, NG = 10, 600, 600          # inmuebles, filas de cobros, filas de gastos
AZUL, GRIS = "1F3A5F", "F2F2F2"
H = Font(bold=True, color="FFFFFF"); B = Font(bold=True)
fillH = PatternFill("solid", fgColor=AZUL); fillCalc = PatternFill("solid", fgColor=GRIS)
thin = Side(style="thin", color="BFBFBF"); box = Border(left=thin, right=thin, top=thin, bottom=thin)
EUR = '#,##0.00 "€";[Red]-#,##0.00 "€"'; PCT = '0.00%'; FECHA = 'DD/MM/YYYY'
MESES = ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"]
CATS = ["IBI", "Comunidad", "Seguro", "Reparaciones", "Mantenimiento", "Suministros", "Intereses hipoteca",
        "Gestoría", "Agencia / publicidad", "Tasa de basuras", "Mobiliario", "Seguro de impago", "Otros"]


def cab(ws, fila, cols, anchos):
    for i, (t, w) in enumerate(zip(cols, anchos), 1):
        c = ws.cell(fila, i, t); c.font = H; c.fill = fillH; c.border = box
        c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        ws.column_dimensions[c.column_letter].width = w
    ws.row_dimensions[fila].height = 34


def titulo(ws, t, sub):
    ws["A1"] = t; ws["A1"].font = Font(bold=True, size=16, color=AZUL)
    ws["A2"] = sub; ws["A2"].font = Font(italic=True, color="595959")


wb = Workbook()
# ---------------------------------------------------------------- Instrucciones
ins = wb.active; ins.title = "Instrucciones"; ins.column_dimensions["A"].width = 112
L = [
 ("Control de alquileres para propietarios", Font(bold=True, size=18, color=AZUL)),
 ("Hasta 10 viviendas o locales: cobros mes a mes, inquilinos que deben dinero, gastos y rentabilidad real.", None),
 ("", None), ("CÓMO SE USA", B),
 ("1. En 'Ajustes' escribe el año. Usa un archivo por año (Archivo > Guardar como, y vacía Cobros y Gastos).", None),
 ("2. En 'Inmuebles' da de alta cada vivienda: nombre corto, inquilino, renta mensual, fianza, precio de compra y fechas de contrato.", None),
 ("3. En 'Cobros' apunta cada pago: fecha, inmueble, mes al que corresponde, lo que tocaba cobrar y lo que has cobrado.", None),
 ("   Si un inquilino paga tarde o a medias, la fila se marca en naranja o rojo y aparece en 'Resumen' como pendiente.", None),
 ("4. En 'Gastos' apunta cada gasto con su inmueble y categoría (IBI, comunidad, seguro, reparaciones...).", None),
 ("5. 'Resumen' da por inmueble lo cobrado, lo pendiente, los gastos, el beneficio y la rentabilidad bruta y neta.", None),
 ("6. 'Mes a mes' muestra lo cobrado de cada inmueble en cada mes y un gráfico de ingresos y gastos.", None),
 ("Rellena solo las celdas blancas: las grises se calculan solas. El nombre del inmueble se elige de una lista.", None),
 ("", None), ("CÓMO CALCULA", B),
 ("• Pendiente = importe que tocaba cobrar − importe cobrado (por fila y sumado por inmueble).", None),
 ("• Beneficio neto = cobrado − gastos del año.", None),
 ("• Rentabilidad bruta = renta mensual × 12 / precio de compra.  Rentabilidad neta = beneficio neto / precio de compra.", None),
 ("• El aviso de contrato se pone en naranja cuando faltan 90 días o menos para el fin del contrato, y en rojo si ya ha vencido.", None),
 ("", None), ("AVISO", B),
 ("Es una herramienta de organización. No calcula impuestos (amortización, reducciones por alquiler de vivienda, etc.):", None),
 ("para tu declaración de la renta usa el programa de la Agencia Tributaria o consulta a un asesor.", None),
]
for i, (t, f) in enumerate(L, 1):
    c = ins.cell(i, 1, t); c.alignment = Alignment(wrap_text=True, vertical="top")
    if f: c.font = f

# ---------------------------------------------------------------- Ajustes
aj = wb.create_sheet("Ajustes"); titulo(aj, "Ajustes", "Cambia solo las celdas blancas.")
aj.column_dimensions["A"].width = 30; aj.column_dimensions["B"].width = 26
aj["A4"] = "Año del archivo"; aj["B4"] = 2027
aj["A5"] = "Propietario (opcional)"; aj["B5"] = ""
aj["A6"] = "Hoy (se calcula solo)"; aj["B6"] = "=TODAY()"; aj["B6"].number_format = FECHA; aj["B6"].fill = fillCalc
for r in (4, 5, 6):
    aj.cell(r, 1).font = B; aj.cell(r, 2).border = box

# ---------------------------------------------------------------- Inmuebles
im = wb.create_sheet("Inmuebles"); titulo(im, "Inmuebles", "Una fila por vivienda o local. El nombre corto es el que eliges luego en Cobros y Gastos.")
cab(im, 4, ["Nombre corto", "Dirección", "Inquilino", "Teléfono / email", "Renta mensual", "Día de cobro", "Fianza",
            "Precio de compra", "Inicio contrato", "Fin contrato", "Renta anual", "Aviso de contrato"],
    [18, 30, 22, 22, 14, 10, 12, 16, 14, 14, 15, 22])
for r in range(5, 5 + NI):
    for col in range(1, 13):
        im.cell(r, col).border = box
    for col in (5, 7, 8, 11): im.cell(r, col).number_format = EUR
    for col in (9, 10): im.cell(r, col).number_format = FECHA
    im.cell(r, 11, f'=IF(E{r}="","",E{r}*12)').fill = fillCalc
    im.cell(r, 12, f'=IF(J{r}="","",IF(J{r}<Ajustes!$B$6,"Vencido",IF(J{r}-Ajustes!$B$6<=90,"Vence en "&(J{r}-Ajustes!$B$6)&" días","En vigor")))').fill = fillCalc
dvd = DataValidation(type="whole", operator="between", formula1="1", formula2="31", allow_blank=True); im.add_data_validation(dvd); dvd.add(f"F5:F{4 + NI}")
im.conditional_formatting.add(f"L5:L{4 + NI}", FormulaRule(formula=['LEFT(L5,6)="Vencid"'], fill=PatternFill("solid", fgColor="F8CBAD")))
im.conditional_formatting.add(f"L5:L{4 + NI}", FormulaRule(formula=['LEFT(L5,5)="Vence"'], fill=PatternFill("solid", fgColor="FFE699")))
im.freeze_panes = "B5"
LISTA = f"Inmuebles!$A$5:$A${4 + NI}"

# ---------------------------------------------------------------- Cobros
co = wb.create_sheet("Cobros"); titulo(co, "Cobros", "Una fila por mes y inmueble. Si aún no ha pagado, deja «Cobrado» vacío: contará como pendiente.")
cab(co, 4, ["Fecha", "Inmueble", "Mes", "Concepto", "Tocaba cobrar", "Cobrado", "Pendiente", "Estado", "Notas"],
    [13, 18, 9, 16, 15, 15, 15, 13, 30])
for r in range(5, 5 + NC):
    for col in range(1, 10): co.cell(r, col).border = box
    co.cell(r, 1).number_format = FECHA
    for col in (5, 6, 7): co.cell(r, col).number_format = EUR
    co.cell(r, 7, f'=IF(E{r}="","",E{r}-N(F{r}))').fill = fillCalc
    co.cell(r, 8, f'=IF(E{r}="","",IF(N(F{r})>=E{r},"Cobrado",IF(N(F{r})>0,"Parcial","Pendiente")))').fill = fillCalc
dvi = DataValidation(type="list", formula1=LISTA, allow_blank=True); co.add_data_validation(dvi); dvi.add(f"B5:B{4 + NC}")
dvm = DataValidation(type="whole", operator="between", formula1="1", formula2="12", allow_blank=True,
                     error="Escribe el número del mes (1 a 12)", showErrorMessage=True); co.add_data_validation(dvm); dvm.add(f"C5:C{4 + NC}")
dvc = DataValidation(type="list", formula1='"Renta,Suministros,Fianza,Otros"', allow_blank=True); co.add_data_validation(dvc); dvc.add(f"D5:D{4 + NC}")
co.conditional_formatting.add(f"A5:I{4 + NC}", FormulaRule(formula=['$H5="Pendiente"'], fill=PatternFill("solid", fgColor="F8CBAD")))
co.conditional_formatting.add(f"A5:I{4 + NC}", FormulaRule(formula=['$H5="Parcial"'], fill=PatternFill("solid", fgColor="FFE699")))
co.conditional_formatting.add(f"A5:A{4 + NC}", FormulaRule(formula=['AND(A5<>"",YEAR(A5)<>Ajustes!$B$4)'], font=Font(color="C00000", bold=True)))
co.freeze_panes = "A5"

# ---------------------------------------------------------------- Gastos
ga = wb.create_sheet("Gastos"); titulo(ga, "Gastos", "Una fila por gasto o factura. Elige el inmueble y la categoría de la lista.")
cab(ga, 4, ["Fecha", "Inmueble", "Categoría", "Descripción / proveedor", "Importe", "Mes"], [13, 18, 20, 34, 15, 8])
for r in range(5, 5 + NG):
    for col in range(1, 7): ga.cell(r, col).border = box
    ga.cell(r, 1).number_format = FECHA; ga.cell(r, 5).number_format = EUR
    ga.cell(r, 6, f'=IF(A{r}="","",MONTH(A{r}))').fill = fillCalc
dvi2 = DataValidation(type="list", formula1=LISTA, allow_blank=True); ga.add_data_validation(dvi2); dvi2.add(f"B5:B{4 + NG}")
cats = wb.create_sheet("Listas"); cats["A1"] = "Categorías de gasto (puedes cambiarlas)"; cats["A1"].font = B; cats.column_dimensions["A"].width = 36
for i, c in enumerate(CATS, 2): cats.cell(i, 1, c)
dvg = DataValidation(type="list", formula1=f"Listas!$A$2:$A$30", allow_blank=True); ga.add_data_validation(dvg); dvg.add(f"C5:C{4 + NG}")
ga.conditional_formatting.add(f"A5:A{4 + NG}", FormulaRule(formula=['AND(A5<>"",YEAR(A5)<>Ajustes!$B$4)'], font=Font(color="C00000", bold=True)))
ga.freeze_panes = "A5"

# ---------------------------------------------------------------- Resumen
rs = wb.create_sheet("Resumen", 1); titulo(rs, "Resumen del año", "Todo se calcula solo a partir de Inmuebles, Cobros y Gastos.")
cab(rs, 4, ["Inmueble", "Inquilino", "Renta anual prevista", "Cobrado", "Pendiente de cobro", "Gastos", "Beneficio neto",
            "Rentabilidad bruta", "Rentabilidad neta", "Contrato"], [18, 22, 16, 15, 15, 15, 15, 13, 13, 22])
C, G = f"Cobros!$B$5:$B${4 + NC}", f"Gastos!$B$5:$B${4 + NG}"
for i in range(NI):
    r = 5 + i; s = 5 + i
    f = {
        1: f'=IF(Inmuebles!A{s}="","",Inmuebles!A{s})',
        2: f'=IF(Inmuebles!A{s}="","",Inmuebles!C{s})',
        3: f'=IF(A{r}="","",N(Inmuebles!K{s}))',
        4: f'=IF(A{r}="","",SUMIFS(Cobros!$F$5:$F${4 + NC},{C},A{r}))',
        5: f'=IF(A{r}="","",SUMIFS(Cobros!$G$5:$G${4 + NC},{C},A{r}))',
        6: f'=IF(A{r}="","",SUMIFS(Gastos!$E$5:$E${4 + NG},{G},A{r}))',
        7: f'=IF(A{r}="","",D{r}-F{r})',
        8: f'=IF(OR(A{r}="",N(Inmuebles!H{s})=0),"",C{r}/Inmuebles!H{s})',
        9: f'=IF(OR(A{r}="",N(Inmuebles!H{s})=0),"",G{r}/Inmuebles!H{s})',
        10: f'=IF(A{r}="","",Inmuebles!L{s})',
    }
    for col, fx in f.items():
        c = rs.cell(r, col, fx); c.fill = fillCalc; c.border = box
        c.number_format = EUR if col in (3, 4, 5, 6, 7) else (PCT if col in (8, 9) else "General")
T = 5 + NI
rs.cell(T, 1, "TOTAL").font = B
for col, L_ in ((3, "C"), (4, "D"), (5, "E"), (6, "F"), (7, "G")):
    c = rs.cell(T, col, f"=SUM({L_}5:{L_}{T - 1})"); c.font = B; c.number_format = EUR; c.border = box
c = rs.cell(T, 8, f'=IF(SUM(Inmuebles!H5:H{4 + NI})=0,"",SUMIFS(Inmuebles!K5:K{4 + NI},Inmuebles!H5:H{4 + NI},">0")/SUM(Inmuebles!H5:H{4 + NI}))')
c.number_format = PCT; c.font = B
c = rs.cell(T, 9, f'=IF(SUM(Inmuebles!H5:H{4 + NI})=0,"",SUMIFS(G5:G{T - 1},Inmuebles!H5:H{4 + NI},">0")/SUM(Inmuebles!H5:H{4 + NI}))')
c.number_format = PCT; c.font = B
rs.cell(T + 2, 1, "Recibos pendientes o parciales:").font = B
rs.cell(T + 2, 3, f'=COUNTIF(Cobros!$H$5:$H${4 + NC},"Pendiente")+COUNTIF(Cobros!$H$5:$H${4 + NC},"Parcial")')
rs.cell(T + 3, 1, "Tasa de cobro del año:").font = B
c = rs.cell(T + 3, 3, f'=IF(SUM(Cobros!$E$5:$E${4 + NC})=0,"",SUM(Cobros!$F$5:$F${4 + NC})/SUM(Cobros!$E$5:$E${4 + NC}))'); c.number_format = PCT
rs.cell(T + 4, 1, "Gasto por categoría:").font = B
for i, cat in enumerate(CATS):
    rs.cell(T + 5 + i, 1, f"=Listas!A{i + 2}")
    c = rs.cell(T + 5 + i, 3, f'=IF(A{T + 5 + i}="","",SUMIFS(Gastos!$E$5:$E${4 + NG},Gastos!$C$5:$C${4 + NG},A{T + 5 + i}))'); c.number_format = EUR
rs.conditional_formatting.add(f"E5:E{T - 1}", CellIsRule(operator="greaterThan", formula=["0"], fill=PatternFill("solid", fgColor="F8CBAD")))
rs.freeze_panes = "B5"

# ---------------------------------------------------------------- Mes a mes
mm = wb.create_sheet("Mes a mes", 2); titulo(mm, "Mes a mes", "Cobrado por inmueble y mes (según la columna «Mes» de Cobros) y gastos por mes.")
cab(mm, 4, ["Inmueble"] + MESES + ["Total"], [18] + [11] * 12 + [14])
for i in range(NI):
    r = 5 + i
    mm.cell(r, 1, f'=IF(Inmuebles!A{5 + i}="","",Inmuebles!A{5 + i})').fill = fillCalc
    for m in range(1, 13):
        c = mm.cell(r, 1 + m, f'=IF($A{r}="","",SUMIFS(Cobros!$F$5:$F${4 + NC},{C},$A{r},Cobros!$C$5:$C${4 + NC},{m}))')
        c.number_format = EUR; c.border = box
    c = mm.cell(r, 14, f'=IF($A{r}="","",SUM(B{r}:M{r}))'); c.number_format = EUR; c.font = B
R1, R2 = 5 + NI, 6 + NI
mm.cell(R1, 1, "Ingresos").font = B; mm.cell(R2, 1, "Gastos").font = B
for m in range(1, 13):
    L_ = mm.cell(1, 1 + m).column_letter
    c = mm.cell(R1, 1 + m, f"=SUM({L_}5:{L_}{4 + NI})"); c.number_format = EUR; c.font = B
    c = mm.cell(R2, 1 + m, f'=SUMIFS(Gastos!$E$5:$E${4 + NG},Gastos!$F$5:$F${4 + NG},{m})'); c.number_format = EUR; c.font = B
for rr in (R1, R2):
    c = mm.cell(rr, 14, f"=SUM(B{rr}:M{rr})"); c.number_format = EUR; c.font = B
ch = BarChart(); ch.type = "col"; ch.title = "Ingresos y gastos por mes"; ch.height = 8; ch.width = 24
ch.add_data(Reference(mm, min_col=1, max_col=13, min_row=R1, max_row=R2), from_rows=True, titles_from_data=True)
ch.set_categories(Reference(mm, min_col=2, max_col=13, min_row=4))
mm.add_chart(ch, f"A{R2 + 3}")

# ---------------------------------------------------------------- datos de prueba
if PRUEBA:
    import datetime as dt
    D = dt.date
    im["A5"], im["C5"], im["E5"], im["F5"], im["G5"], im["H5"], im["I5"], im["J5"] = "Piso Centro", "Laura M.", 750, 5, 750, 150000, D(2025, 9, 1), D(2030, 8, 31)
    im["A6"], im["C6"], im["E6"], im["F6"], im["G6"], im["H6"], im["I6"], im["J6"] = "Estudio Playa", "Jorge R.", 520, 1, 520, 98000, D(2026, 3, 1), D(2027, 2, 28)
    rows = []
    for m in range(1, 4):
        rows.append((D(2027, m, 5), "Piso Centro", m, "Renta", 750, 750))
        rows.append((D(2027, m, 2), "Estudio Playa", m, "Renta", 520, 520 if m < 3 else 260))
    rows.append((D(2027, 4, 5), "Piso Centro", 4, "Renta", 750, None))
    for i, row in enumerate(rows):
        for j, v in enumerate(row, 1):
            if v is not None: co.cell(5 + i, j, v)
    g = [(D(2027, 1, 20), "Piso Centro", "Comunidad", "Cuota T1", 180), (D(2027, 2, 10), "Piso Centro", "IBI", "Recibo IBI", 420),
         (D(2027, 3, 15), "Estudio Playa", "Reparaciones", "Fontanero", 95.5), (D(2027, 1, 30), "Estudio Playa", "Seguro", "Hogar", 160)]
    for i, row in enumerate(g):
        for j, v in enumerate(row, 1): ga.cell(5 + i, j, v)

wb.save(OUT); print("ok", OUT)
