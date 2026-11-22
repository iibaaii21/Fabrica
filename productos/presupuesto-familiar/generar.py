#!/usr/bin/env python3
"""Genera Presupuesto-Familiar.xlsx: presupuesto mensual de casa (ingresos, gastos por categoría, 50/30/20 y metas de ahorro).
Uso: python3 generar.py SALIDA.xlsx [--prueba]   (--prueba rellena datos de ejemplo para verificar)"""
import sys, datetime as dt
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.formatting.rule import FormulaRule, CellIsRule, DataBarRule
from openpyxl.chart import BarChart, Reference

OUT = sys.argv[1]; PRUEBA = '--prueba' in sys.argv
NCAT, NM, NMETA = 40, 1500, 8          # categorías, filas de movimientos, metas
VERDE, GRIS = "2E5E4E", "F2F2F2"
H = Font(bold=True, color="FFFFFF"); B = Font(bold=True)
fillH = PatternFill("solid", fgColor=VERDE); fillCalc = PatternFill("solid", fgColor=GRIS)
thin = Side(style="thin", color="BFBFBF"); box = Border(left=thin, right=thin, top=thin, bottom=thin)
EUR = '#,##0.00 "€";[Red]-#,##0.00 "€"'; PCT = '0.0%'; FECHA = 'DD/MM/YYYY'
MESES = ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"]
TIPOS = ["Ingreso", "Necesidad", "Deseo", "Ahorro"]
CATS = [("Nómina", "Ingreso", 1800), ("Paga extra", "Ingreso", 0), ("Otros ingresos", "Ingreso", 0),
        ("Vivienda (alquiler o hipoteca)", "Necesidad", 650), ("Luz y gas", "Necesidad", 70), ("Agua", "Necesidad", 20),
        ("Internet y móvil", "Necesidad", 45), ("Supermercado", "Necesidad", 280), ("Transporte", "Necesidad", 60),
        ("Seguros", "Necesidad", 30), ("Salud y farmacia", "Necesidad", 20), ("Educación", "Necesidad", 0),
        ("Deudas y préstamos", "Necesidad", 0),
        ("Restaurantes y bares", "Deseo", 80), ("Ocio y salidas", "Deseo", 60), ("Ropa", "Deseo", 40),
        ("Suscripciones", "Deseo", 25), ("Viajes", "Deseo", 50), ("Regalos", "Deseo", 20), ("Otros gastos", "Deseo", 30),
        ("Fondo de emergencia", "Ahorro", 150), ("Ahorro para metas", "Ahorro", 100), ("Inversión", "Ahorro", 0)]
C0 = 8; CL = C0 + NCAT - 1          # filas de categorías en Ajustes
CAT = f"Ajustes!$A${C0}:$A${CL}"; TIP = f"Ajustes!$B${C0}:$B${CL}"; PRE = f"Ajustes!$C${C0}:$C${CL}"
M0 = 5; ML = M0 + NM - 1
MC = f"Movimientos!$C${M0}:$C${ML}"; MI = f"Movimientos!$D${M0}:$D${ML}"; MM = f"Movimientos!$F${M0}:$F${ML}"; MT = f"Movimientos!$G${M0}:$G${ML}"


def cab(ws, fila, cols, anchos):
    for i, (t, w) in enumerate(zip(cols, anchos), 1):
        c = ws.cell(fila, i, t); c.font = H; c.fill = fillH; c.border = box
        c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        ws.column_dimensions[c.column_letter].width = w
    ws.row_dimensions[fila].height = 34


def titulo(ws, t, sub):
    ws["A1"] = t; ws["A1"].font = Font(bold=True, size=16, color=VERDE)
    ws["A2"] = sub; ws["A2"].font = Font(italic=True, color="595959")


def calc(c, fmt=None, bold=False):
    c.fill = fillCalc; c.border = box
    if fmt: c.number_format = fmt
    if bold: c.font = B
    return c


wb = Workbook()
# ---------------------------------------------------------------- Instrucciones
ins = wb.active; ins.title = "Instrucciones"; ins.column_dimensions["A"].width = 112
L = [
 ("Presupuesto familiar y personal", Font(bold=True, size=18, color=VERDE)),
 ("Sabe cada mes cuánto entra, en qué se va y cuánto ahorras, por categorías y con metas de ahorro.", None),
 ("", None), ("CÓMO SE USA", B),
 ("1. En 'Ajustes' escribe el año y el mes que quieres analizar.", None),
 ("2. En 'Ajustes', revisa las categorías: cada una tiene un tipo (Ingreso, Necesidad, Deseo o Ahorro) y un presupuesto mensual.", None),
 ("   Cambia, borra o añade las que quieras (hay sitio para 40). Pon 0 si no quieres presupuesto para una categoría.", None),
 ("3. En 'Movimientos' apunta cada ingreso o gasto: fecha, concepto, categoría (de la lista) e importe, siempre en positivo.", None),
 ("   Lo que apartas para ahorrar (por ejemplo, la transferencia a tu cuenta de ahorro) apúntalo con una categoría de tipo Ahorro.", None),
 ("4. 'Presupuesto' compara, para el mes elegido y para todo el año, lo presupuestado con lo real. En rojo, lo que se pasa.", None),
 ("5. 'Mes a mes' muestra cada categoría en cada mes, los totales y un gráfico de ingresos, gastos y ahorro.", None),
 ("6. 'Resumen' da la tasa de ahorro y el reparto entre necesidades, deseos y ahorro frente a la regla 50/30/20.", None),
 ("7. En 'Metas' apunta tus objetivos de ahorro: te dice el porcentaje conseguido y cuánto apartar al mes para llegar a tiempo.", None),
 ("Rellena solo las celdas blancas: las grises se calculan solas. Usa un archivo por año.", None),
 ("", None), ("CÓMO CALCULA", B),
 ("• Gastos = categorías de tipo Necesidad + Deseo. Ahorro apartado = categorías de tipo Ahorro.", None),
 ("• Te queda = ingresos − gastos − ahorro apartado (dinero que sigue en la cuenta corriente).", None),
 ("• Tasa de ahorro = (ingresos − gastos) / ingresos: incluye lo apartado y lo que te queda sin gastar.", None),
 ("• Regla 50/30/20: una guía orientativa muy usada (50 % necesidades, 30 % deseos, 20 % ahorro). No es una norma: adáptala a tu caso.", None),
 ("• Cuota mensual de una meta = lo que falta / meses que quedan hasta la fecha objetivo.", None),
 ("", None), ("AVISO", B),
 ("Es una herramienta de organización personal. No es asesoramiento financiero ni fiscal.", None),
 ("Plantilla creada con ayuda de IA y revisada fórmula a fórmula.", Font(italic=True, color="595959")),
]
for i, (t, f) in enumerate(L, 1):
    c = ins.cell(i, 1, t)
    if f: c.font = f
# ---------------------------------------------------------------- Ajustes
aj = wb.create_sheet("Ajustes"); titulo(aj, "Ajustes y categorías", "Año, mes a analizar y categorías con su tipo y presupuesto mensual.")
aj["A4"] = "Año"; aj["A4"].font = B; aj["B4"] = 2027; aj["B4"].border = box
aj["A5"] = "Mes a analizar (1-12)"; aj["A5"].font = B; aj["B5"] = 1; aj["B5"].border = box
dvm = DataValidation(type="whole", operator="between", formula1="1", formula2="12", allow_blank=False); aj.add_data_validation(dvm); dvm.add("B5")
cab(aj, 7, ["Categoría", "Tipo", "Presupuesto mensual"], [34, 14, 20])
dvt = DataValidation(type="list", formula1='"' + ",".join(TIPOS) + '"', allow_blank=True); aj.add_data_validation(dvt); dvt.add(f"B{C0}:B{CL}")
for i in range(NCAT):
    r = C0 + i
    for col in (1, 2, 3): aj.cell(r, col).border = box
    aj.cell(r, 3).number_format = EUR
    if i < len(CATS):
        aj.cell(r, 1, CATS[i][0]); aj.cell(r, 2, CATS[i][1]); aj.cell(r, 3, CATS[i][2])
aj.freeze_panes = "A8"
# ---------------------------------------------------------------- Movimientos
mv = wb.create_sheet("Movimientos"); titulo(mv, "Movimientos", "Un ingreso o gasto por fila. Importe siempre en positivo.")
cab(mv, 4, ["Fecha", "Concepto", "Categoría", "Importe", "Quién (opcional)", "Mes", "Tipo"], [13, 34, 30, 14, 16, 8, 12])
dvc = DataValidation(type="list", formula1=CAT, allow_blank=True); mv.add_data_validation(dvc); dvc.add(f"C{M0}:C{ML}")
dvi = DataValidation(type="decimal", operator="greaterThanOrEqual", formula1="0", allow_blank=True); mv.add_data_validation(dvi); dvi.add(f"D{M0}:D{ML}")
for r in range(M0, ML + 1):
    for col in range(1, 6): mv.cell(r, col).border = box
    mv.cell(r, 1).number_format = FECHA; mv.cell(r, 4).number_format = EUR
    calc(mv.cell(r, 6, f'=IF(A{r}="","",MONTH(A{r}))'))
    calc(mv.cell(r, 7, f'=IF(C{r}="","",IFERROR(INDEX({TIP},MATCH(C{r},{CAT},0)),"¿Categoría?"))'))
mv.conditional_formatting.add(f"A{M0}:A{ML}", FormulaRule(formula=[f'AND(A{M0}<>"",YEAR(A{M0})<>Ajustes!$B$4)'], font=Font(color="C00000", bold=True)))
mv.conditional_formatting.add(f"G{M0}:G{ML}", FormulaRule(formula=[f'G{M0}="¿Categoría?"'], fill=PatternFill("solid", fgColor="F8CBAD")))
mv.conditional_formatting.add(f"A{M0}:G{ML}", FormulaRule(formula=[f'$G{M0}="Ingreso"'], font=Font(color="2E7D4F")))
mv.freeze_panes = "A5"
# ---------------------------------------------------------------- Presupuesto
ps = wb.create_sheet("Presupuesto"); titulo(ps, "Presupuesto frente a real", "Mes elegido en Ajustes y acumulado del año.")
ps["A3"] = '="Mes analizado: "&INDEX({"Enero","Febrero","Marzo","Abril","Mayo","Junio","Julio","Agosto","Septiembre","Octubre","Noviembre","Diciembre"},Ajustes!$B$5)&" de "&Ajustes!$B$4'
ps["A3"].font = Font(bold=True, color=VERDE)
cab(ps, 5, ["Categoría", "Tipo", "Presupuesto mes", "Real mes", "Diferencia mes", "% usado mes", "Presupuesto año", "Real año", "Diferencia año"], [32, 12, 15, 14, 15, 12, 16, 14, 15])
P0 = 6
for i in range(NCAT):
    r = P0 + i; a = C0 + i
    calc(ps.cell(r, 1, f'=IF(Ajustes!A{a}="","",Ajustes!A{a})'))
    calc(ps.cell(r, 2, f'=IF(A{r}="","",Ajustes!B{a})'))
    calc(ps.cell(r, 3, f'=IF(A{r}="","",N(Ajustes!C{a}))'), EUR)
    calc(ps.cell(r, 4, f'=IF(A{r}="","",SUMIFS({MI},{MC},A{r},{MM},Ajustes!$B$5))'), EUR)
    calc(ps.cell(r, 5, f'=IF(A{r}="","",C{r}-D{r})'), EUR)
    calc(ps.cell(r, 6, f'=IF(OR(A{r}="",N(C{r})=0),"",D{r}/C{r})'), PCT)
    calc(ps.cell(r, 7, f'=IF(A{r}="","",C{r}*12)'), EUR)
    calc(ps.cell(r, 8, f'=IF(A{r}="","",SUMIFS({MI},{MC},A{r}))'), EUR)
    calc(ps.cell(r, 9, f'=IF(A{r}="","",G{r}-H{r})'), EUR)
PL = P0 + NCAT - 1
rojo = PatternFill("solid", fgColor="F8CBAD"); verde = PatternFill("solid", fgColor="C6E0B4")
for col in ("E", "I"):  # diferencia negativa = te pasas (gastos) / ingresos por debajo
    ps.conditional_formatting.add(f"{col}{P0}:{col}{PL}", FormulaRule(formula=[f'AND($B{P0}<>"Ingreso",$B{P0}<>"",{col}{P0}<0)'], fill=rojo))
    ps.conditional_formatting.add(f"{col}{P0}:{col}{PL}", FormulaRule(formula=[f'AND($B{P0}="Ingreso",{col}{P0}<0)'], fill=PatternFill("solid", fgColor="FFE699")))
ps.conditional_formatting.add(f"F{P0}:F{PL}", DataBarRule(start_type="num", start_value=0, end_type="num", end_value=1, color="5B9B7E"))
T = PL + 2
for j, (lab, tipos) in enumerate([("Ingresos", ["Ingreso"]), ("Gastos (necesidades + deseos)", ["Necesidad", "Deseo"]), ("Ahorro apartado", ["Ahorro"])]):
    r = T + j; ps.cell(r, 1, lab).font = B
    for col, src in ((3, "C"), (4, "D"), (7, "G"), (8, "H")):
        f = "+".join(f'SUMIFS({src}{P0}:{src}{PL},B{P0}:B{PL},"{t}")' for t in tipos)
        calc(ps.cell(r, col, "=" + f), EUR, True)
r = T + 3; ps.cell(r, 1, "Te queda (ingresos − gastos − ahorro)").font = B
for col in ("C", "D", "G", "H"):
    calc(ps[f"{col}{r}"], EUR, True); ps[f"{col}{r}"] = f"={col}{T}-{col}{T + 1}-{col}{T + 2}"
ps.freeze_panes = "B6"
# ---------------------------------------------------------------- Mes a mes
mm = wb.create_sheet("Mes a mes"); titulo(mm, "Mes a mes", "Real de cada categoría en cada mes del año.")
cab(mm, 4, ["Categoría", "Tipo"] + MESES + ["Total"], [32, 12] + [11] * 12 + [13])
for i in range(NCAT):
    r = 5 + i; a = C0 + i
    calc(mm.cell(r, 1, f'=IF(Ajustes!A{a}="","",Ajustes!A{a})')); calc(mm.cell(r, 2, f'=IF(A{r}="","",Ajustes!B{a})'))
    for m in range(1, 13):
        calc(mm.cell(r, 2 + m, f'=IF($A{r}="","",SUMIFS({MI},{MC},$A{r},{MM},{m}))'), EUR)
    calc(mm.cell(r, 15, f'=IF(A{r}="","",SUM(C{r}:N{r}))'), EUR, True)
    hc = mm.cell(r, 17, f'=IF(AND(A{r}<>"",OR(B{r}="Necesidad",B{r}="Deseo"),N(O{r})>0),O{r}+ROW()/1000000,"")'); hc.font = Font(color="BFBFBF")
R1 = 5 + NCAT + 1; LBL = ["Ingresos", "Gastos", "Ahorro apartado", "Te queda", "Tasa de ahorro"]
for j, lab in enumerate(LBL):
    mm.cell(R1 + j, 1, lab).font = B
for m in range(1, 14):
    col = mm.cell(1, 2 + m).column_letter
    if m <= 12:
        mm[f"{col}{R1}"] = f'=SUMIFS({MI},{MM},{m},{MT},"Ingreso")'
        mm[f"{col}{R1 + 1}"] = f'=SUMIFS({MI},{MM},{m},{MT},"Necesidad")+SUMIFS({MI},{MM},{m},{MT},"Deseo")'
        mm[f"{col}{R1 + 2}"] = f'=SUMIFS({MI},{MM},{m},{MT},"Ahorro")'
    else:
        for k in range(3): mm[f"{col}{R1 + k}"] = f"=SUM(C{R1 + k}:N{R1 + k})"
    mm[f"{col}{R1 + 3}"] = f"={col}{R1}-{col}{R1 + 1}-{col}{R1 + 2}"
    mm[f"{col}{R1 + 4}"] = f'=IF({col}{R1}=0,"",({col}{R1}-{col}{R1 + 1})/{col}{R1})'
    for k in range(5): calc(mm[f"{col}{R1 + k}"], PCT if k == 4 else EUR, True)
mm.conditional_formatting.add(f"C{R1 + 3}:O{R1 + 3}", CellIsRule(operator="lessThan", formula=["0"], fill=rojo))
ch = BarChart(); ch.type = "col"; ch.title = "Ingresos, gastos y ahorro por mes"; ch.height = 8; ch.width = 26
data = Reference(mm, min_col=1, max_col=14, min_row=R1, max_row=R1 + 2)
ch.add_data(data, from_rows=True, titles_from_data=True)
ch.set_categories(Reference(mm, min_col=3, max_col=14, min_row=4)); mm.add_chart(ch, f"A{R1 + 7}")
mm.freeze_panes = "C5"
mm["Q4"] = "aux. ranking"; mm["Q4"].font = Font(italic=True, color="BFBFBF"); mm.column_dimensions["Q"].width = 12
# ---------------------------------------------------------------- Resumen
rs = wb.create_sheet("Resumen", 1); titulo(rs, "Resumen del año", "Cuánto entra, cuánto sale y cómo se reparte.")
rs.column_dimensions["A"].width = 38; rs.column_dimensions["B"].width = 18; rs.column_dimensions["C"].width = 18; rs.column_dimensions["D"].width = 22
tot = f"'Mes a mes'!O{R1}"
filas = [("Ingresos del año", f"='Mes a mes'!O{R1}", EUR), ("Gastos del año", f"='Mes a mes'!O{R1 + 1}", EUR),
         ("Ahorro apartado", f"='Mes a mes'!O{R1 + 2}", EUR), ("Te queda en la cuenta", f"='Mes a mes'!O{R1 + 3}", EUR),
         ("Tasa de ahorro", f"='Mes a mes'!O{R1 + 4}", PCT),
         ("Meses con movimientos", f'=SUMPRODUCT(--(COUNTIFS({MM},ROW($1:$12))>0))', "0"),
         ("Gasto medio al mes", '=IF(B9=0,"",B5/B9)', EUR)]
for j, (lab, f, fmt) in enumerate(filas):
    r = 4 + j; rs.cell(r, 1, lab).font = B; calc(rs.cell(r, 2, f), fmt, True)
rs["A13"] = "Reparto frente a la regla 50/30/20 (orientativa)"; rs["A13"].font = Font(bold=True, size=13, color=VERDE)
cab(rs, 14, ["Tipo", "Real", "% de ingresos", "Guía 50/30/20"], [38, 18, 18, 22])
for j, (t, g) in enumerate([("Necesidad", 0.5), ("Deseo", 0.3), ("Ahorro", 0.2)]):
    r = 15 + j; rs.cell(r, 1, t).border = box
    if t == "Ahorro":
        calc(rs.cell(r, 2, "=B4-B16-B15"), EUR)   # ahorro total = ingresos - necesidades - deseos
    else:
        calc(rs.cell(r, 2, f'=SUMIFS({MI},{MT},"{t}")'), EUR)
    calc(rs.cell(r, 3, f'=IF($B$4=0,"",B{r}/$B$4)'), PCT)
    c = rs.cell(r, 4, g); c.number_format = '0%'; c.border = box
rs["A18"] = "Ahorro = ingresos − necesidades − deseos (lo apartado más lo que te queda)."; rs["A18"].font = Font(italic=True, color="595959")
rs.conditional_formatting.add("C15:C16", FormulaRule(formula=['AND(C15<>"",C15>D15)'], fill=rojo))
rs.conditional_formatting.add("C17", FormulaRule(formula=['AND(C17<>"",C17>=D17)'], fill=verde))
rs["A20"] = "Las 5 categorías de gasto que más pesan"; rs["A20"].font = Font(bold=True, size=13, color=VERDE)
cab(rs, 21, ["Categoría", "Gastado en el año", "% de los gastos", ""], [38, 18, 18, 22])
GQ = f"'Mes a mes'!$Q$5:$Q${4 + NCAT}"; GA = f"'Mes a mes'!$A$5:$A${4 + NCAT}"; GO = f"'Mes a mes'!$O$5:$O${4 + NCAT}"
for k in range(5):
    r = 22 + k; pos = f'MATCH(LARGE({GQ},{k + 1}),{GQ},0)'
    calc(rs.cell(r, 1, f'=IFERROR(INDEX({GA},{pos}),"")'))
    calc(rs.cell(r, 2, f'=IFERROR(INDEX({GO},{pos}),"")'), EUR)
    calc(rs.cell(r, 3, f'=IF(OR(B{r}="",$B$5=0),"",B{r}/$B$5)'), PCT)
# ---------------------------------------------------------------- Metas
mt = wb.create_sheet("Metas"); titulo(mt, "Metas de ahorro", "Objetivo, fecha y lo que llevas ahorrado para cada meta.")
cab(mt, 4, ["Meta", "Objetivo", "Fecha objetivo", "Ahorrado hasta hoy", "% conseguido", "Falta", "Meses que quedan", "Apartar al mes"], [28, 14, 15, 18, 14, 14, 14, 16])
mt["J4"] = "Fecha de hoy"; mt["J4"].font = B; mt["K4"] = "=TODAY()"; mt["K4"].number_format = FECHA; mt.column_dimensions["K"].width = 13
for i in range(NMETA):
    r = 5 + i
    for col in range(1, 5): mt.cell(r, col).border = box
    mt.cell(r, 2).number_format = EUR; mt.cell(r, 3).number_format = FECHA; mt.cell(r, 4).number_format = EUR
    calc(mt.cell(r, 5, f'=IF(OR(A{r}="",N(B{r})=0),"",MIN(1,N(D{r})/B{r}))'), PCT)
    calc(mt.cell(r, 6, f'=IF(A{r}="","",MAX(0,N(B{r})-N(D{r})))'), EUR)
    calc(mt.cell(r, 7, f'=IF(OR(A{r}="",C{r}=""),"",MAX(0,(YEAR(C{r})-YEAR($K$4))*12+MONTH(C{r})-MONTH($K$4)))'), "0")
    calc(mt.cell(r, 8, f'=IF(OR(A{r}="",G{r}=""),"",IF(F{r}=0,0,IF(G{r}=0,F{r},F{r}/G{r})))'), EUR)
mt.conditional_formatting.add(f"E5:E{4 + NMETA}", DataBarRule(start_type="num", start_value=0, end_type="num", end_value=1, color="5B9B7E"))
mt["A15"] = "Si la fecha ya ha llegado o es este mes, «Apartar al mes» muestra todo lo que falta."; mt["A15"].font = Font(italic=True, color="595959")
# ---------------------------------------------------------------- datos de prueba
if PRUEBA:
    aj["B4"] = 2027; aj["B5"] = 2
    D = [("2027-01-01", "Nómina enero", "Nómina", 1800), ("2027-01-02", "Alquiler", "Vivienda (alquiler o hipoteca)", 650),
         ("2027-01-05", "Mercadona", "Supermercado", 120.50), ("2027-01-12", "Cena", "Restaurantes y bares", 45),
         ("2027-01-15", "A cuenta de ahorro", "Fondo de emergencia", 150), ("2027-01-20", "Luz", "Luz y gas", 64.30),
         ("2027-02-01", "Nómina febrero", "Nómina", 1800), ("2027-02-02", "Alquiler", "Vivienda (alquiler o hipoteca)", 650),
         ("2027-02-06", "Supermercado", "Supermercado", 310), ("2027-02-10", "Concierto", "Ocio y salidas", 95),
         ("2027-02-14", "Regalo", "Regalos", 40), ("2027-02-20", "Bizum ahorro viaje", "Ahorro para metas", 100),
         ("2027-02-25", "Abono transporte", "Transporte", 20)]
    for k, (f, c, cat, imp) in enumerate(D):
        r = M0 + k; mv.cell(r, 1, dt.date.fromisoformat(f)); mv.cell(r, 2, c); mv.cell(r, 3, cat); mv.cell(r, 4, imp)
    mt["A5"] = "Viaje a Lisboa"; mt["B5"] = 600; mt["C5"] = dt.date(2027, 8, 1); mt["D5"] = 100
    mt["A6"] = "Fondo de emergencia"; mt["B6"] = 3000; mt["D6"] = 150
wb.save(OUT); print("ok", OUT)
