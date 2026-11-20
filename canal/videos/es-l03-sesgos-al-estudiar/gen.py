# Guion del largo es-l03: 10 sesgos que te engañan al estudiar. Ejecuta: python3 gen.py
import json
F=[]
def b(t, pose="stand", face="neutral", props=(), big=None, head=None, bg=None, pant=None, x=0.32, say=None, hold=None, two=None, **kw):
    v={"chars":[{"x":x,"pose":pose,"face":face}]}
    if say: v["chars"][0]["say"]=say
    if hold: v["chars"][0]["hold"]=hold
    if kw.get("flip"): v["chars"][0]["flip"]=kw.pop("flip")
    if two: v["chars"].append(dict(id="b",flip=True,**two))
    pr=[]
    for i,p in enumerate(props):
        if isinstance(p,str): p={"k":p}
        p.setdefault("x",[0.66,0.78,0.56][i%3]); p.setdefault("y",[0.42,0.42,0.3][i%3]); p.setdefault("s",0.8); p.setdefault("d",0.15*i)
        pr.append(p)
    if pr and not kw.get("board"): v["props"]=pr  # con pizarra, nada delante del texto
    if big: v.update(big=big,bigx=kw.pop("bigx",0.66),bigy=kw.pop("bigy",0.32),bigs=kw.pop("bigs",130))
    if head: v["head"]=head; v["wipe"]=True
    if bg: v["bg"]=bg
    v["ground"]=kw.pop("ground",0.8 if not bg else 0.82)
    v.update(kw)
    f={"t":t,"v":v,"esc":"A"}
    if pant: f["pantalla"]=pant
    F.append(f)
BOARD=dict(x=0.84, flip=True)

# --- INTRO
b("Tu cerebro te engaña cada vez que estudias.", "shock","shock",[{"k":"brain","float":True}], big="!", bigc="#e8483f")
b("No es que seas vago. Es que viene de fábrica con fallos.", "shrug","smirk",[{"k":"cross"}])
b("Hoy vamos a ver diez sesgos cognitivos: atajos mentales que te hacen pensar mal sin darte cuenta.", "point","happy",[{"k":"brain"},{"k":"question","float":True}], pant="Hoy vamos a ver 10 sesgos cognitivos: atajos mentales que te hacen pensar mal sin darte cuenta.")
b("Cada uno con el experimento que lo destapó.", "read","focus",[{"k":"flask","anim":True}], bg="lab")
b("Y el número uno lo has hecho seguramente esta misma semana.", "pointup","smirk",[{"k":"calendar"}], big="#1", bigc="#f6c23e")
b("Empezamos.", "walk","happy",[], walk=0.05, pal=1)

# --- 10 DISPONIBILIDAD
b("Número diez: el sesgo de disponibilidad.", "stand","neutral",[{"k":"bulb","anim":True}], head="10. DISPONIBILIDAD")
b("Pregunta rápida: ¿qué hay más en inglés, palabras que empiezan por K, o palabras con la K en tercer lugar?", "think","focus",[{"k":"card"}], big="K", bigc="#3a7bd5")
b("En mil novecientos setenta y tres, Amos Tversky y Daniel Kahneman hicieron esa pregunta con varias letras.", "read","focus",["notes"], bg="lab", pant="En 1973, Amos Tversky y Daniel Kahneman hicieron esa pregunta con varias letras.")
b("Ciento cinco de ciento cincuenta y dos personas dijeron: empiezan por ella.", "point","happy",[{"k":"check"}], big="105 / 152", bigs=110, bg="lab", pant="105 de 152 personas dijeron: empiezan por ella.")
b("Pero en un texto normal hay más palabras con esas letras en tercera posición.", "shock","shock",[{"k":"cross"}], bg="lab")
b("Pasa porque es mucho más fácil acordarte de palabras por su primera letra.", "think","neutral",[{"k":"brain"}])
b("Y lo que recuerdas fácil, te parece más frecuente.", "shrug","smirk",[{"k":"arrowup"}])
b("Al estudiar: el tema que tienes más fresco te parece el que más cae en el examen. Mira los exámenes anteriores, no tu memoria.", "write","focus",["exam",{"k":"check"}])

# --- 9 COSTE HUNDIDO
b("Número nueve: el coste hundido.", "stand","neutral",[{"k":"ticket"}], head="9. COSTE HUNDIDO")
b("En mil novecientos ochenta y cinco, Hal Arkes y Catherine Blumer plantearon esto a sus estudiantes.", "read","focus",["notes"], bg="lab", pant="En 1985, Hal Arkes y Catherine Blumer plantearon esto a sus estudiantes.")
b("Has comprado un viaje para esquiar por cien dólares.", "cheer","happy",[{"k":"ticket","x":0.66}], big="100 $", bigs=110, bigc="#f6c23e", pant="Has comprado un viaje para esquiar por 100 dólares.")
b("Luego compras otro por cincuenta, que te apetece mucho más. Y descubres que los dos son el mismo fin de semana.", "facepalm","sad",[{"k":"ticket","x":0.62,"anim":"b"},{"k":"calendar","x":0.8}], pant="Luego compras otro por 50, que te apetece mucho más. Y descubres que los dos son el mismo fin de semana.")
b("Solo puedes ir a uno. ¿Cuál eliges?", "think","focus",[{"k":"question","float":True}])
b("El cincuenta y cuatro por ciento eligió el de cien. El que menos le apetecía.", "shock","shock",[{"k":"ticket"}], big="54 %", bigc="#e8483f", pant="El 54 % eligió el de 100. El que menos le apetecía.")
b("Los cien dólares ya estaban gastados fueras a donde fueras. Pero dolía tirarlos.", "sad","sad",[{"k":"cross"}], pant="Los 100 dólares ya estaban gastados fueras a donde fueras. Pero dolía tirarlos.")
b("Al estudiar: llevas dos horas con un método que no funciona, y sigues porque ya has invertido dos horas.", "sitsad","dead",[{"k":"clock"}], bg="library")
b("Las horas perdidas no vuelven. Cambia de método.", "point","focus",[{"k":"arrowup"}])

# --- 8 ENCUADRE
b("Número ocho: el efecto encuadre.", "stand","neutral",[{"k":"card"}], head="8. ENCUADRE")
b("En mil novecientos ochenta y uno, Tversky y Kahneman plantearon una epidemia imaginaria que amenaza a seiscientas personas.", "read","focus",[{"k":"flask","anim":True}], bg="lab", pant="En 1981, Tversky y Kahneman plantearon una epidemia imaginaria que amenaza a 600 personas.")
b("A un grupo le dijeron: con el plan A, se salvan doscientas personas seguro.", "point","happy",[{"k":"check"}], big="200 SALVADAS", bigs=90, bigc="#3fb06b", pant="A un grupo le dijeron: con el plan A, se salvan 200 personas seguro.")
b("El setenta y dos por ciento eligió ese plan.", "cheer","happy",[], big="72 %", bigc="#3fb06b", pant="El 72 % eligió ese plan.")
b("A otro grupo le dijeron lo mismo al revés: con el plan C, mueren cuatrocientas personas seguro.", "point","sad",[{"k":"cross"}], big="400 MUEREN", bigs=90, bigc="#e8483f", pant="A otro grupo le dijeron lo mismo al revés: con el plan C, mueren 400 personas seguro.")
b("Solo lo eligió el veintidós por ciento.", "shock","shock",[], big="22 %", bigc="#e8483f", pant="Solo lo eligió el 22 %.")
b("Mismo resultado, distintas palabras. Y la decisión cambia por completo.", "shrug","smirk",[{"k":"scale","anim":"left"}])
b("Al estudiar: no es lo mismo pensar me quedan tres temas, que solo llevo dos de cinco. Elige el marco que te empuja a seguir.", "write","happy",["notes"], pant="Al estudiar: no es lo mismo pensar «me quedan 3 temas» que «solo llevo 2 de 5». Elige el marco que te empuja a seguir.")

# --- 7 ANCLAJE
b("Número siete: el anclaje.", "stand","neutral",[{"k":"wheel","anim":True}], head="7. ANCLAJE")
b("En mil novecientos setenta y cuatro, Tversky y Kahneman giraban delante de la gente una ruleta trucada.", "point","smirk",[{"k":"wheel","anim":True,"s":1.1}], bg="lab", pant="En 1974, Tversky y Kahneman giraban delante de la gente una ruleta trucada.")
b("Solo podía caer en diez o en sesenta y cinco.", "think","focus",[], big="10 o 65", bigs=120, pant="Solo podía caer en 10 o en 65.")
b("Después preguntaban: ¿qué porcentaje de países de la ONU son africanos?", "think","neutral",[{"k":"question","float":True}])
b("Los que habían visto el diez respondieron un veinticinco por ciento.", "point","neutral",[], big="25 %", bigc="#3a7bd5", pant="Los que habían visto el 10 respondieron un 25 %.")
b("Los que habían visto el sesenta y cinco, un cuarenta y cinco.", "shock","shock",[], big="45 %", bigc="#e8483f", pant="Los que habían visto el 65, un 45 %.")
b("Un número al azar de una ruleta cambió su respuesta casi el doble.", "facepalm","dead",[{"k":"wheel","anim":True}])
b("Al estudiar: si la primera nota que oyes es un cinco, te parece que un seis es un notición. Ponte tu propio objetivo antes de mirar nada.", "pointup","focus",["exam"], pant="Al estudiar: si la primera nota que oyes es un 5, te parece que un 6 es un notición. Ponte tu propio objetivo antes de mirar nada.")

# --- 6 CONFORMIDAD
b("Número seis: la conformidad.", "stand","neutral",[], head="6. CONFORMIDAD", two=dict(x=0.62,pose="stand",face="neutral"))
b("En los años cincuenta, Solomon Asch enseñaba tres líneas y preguntaba cuál medía lo mismo que otra. Era facilísimo.", "point","happy",[{"k":"graph"}], bg="classroom", board="A   B   C", boards=110, **BOARD, pant="En los años 50, Solomon Asch enseñaba tres líneas y preguntaba cuál medía lo mismo que otra. Era facilísimo.")
b("Solos, casi nadie fallaba: menos del uno por ciento de errores.", "cheer","happy",[{"k":"check"}], big="<1 %", pant="Solos, casi nadie fallaba: menos del 1 % de errores.")
b("Pero Asch metía al participante en un grupo de actores que decían en voz alta la respuesta equivocada.", "think","shock",[], bg="stage", spot=0.3, two=dict(x=0.62,pose="pointup",face="smirk"))
b("Resultado: unas tres de cada cuatro personas se dejaron llevar al menos una vez.", "shock","shock",[], big="3 de 4", bigc="#e8483f", pant="Resultado: unas 3 de cada 4 personas se dejaron llevar al menos una vez.")
b("Y en total, siguieron al grupo en más o menos un tercio de las preguntas.", "sad","sad",[{"k":"arrowdown"}])
b("Al estudiar: si en el grupo de clase todos dicen que ese tema no entra, no lo des por hecho. Pregunta a quien pone el examen.", "point","focus",[{"k":"phone"},{"k":"cross"}])

# --- 5 CONFIRMACION
b("Número cinco: el sesgo de confirmación.", "stand","neutral",[{"k":"check"}], head="5. CONFIRMACIÓN")
b("En mil novecientos sesenta, Peter Wason daba tres números: dos, cuatro, seis. Y decía: siguen una regla, adivínala.", "point","happy",[], bg="classroom", board="2 · 4 · 6", boards=130, **BOARD, pant="En 1960, Peter Wason daba tres números: 2, 4, 6. Y decía: siguen una regla, adivínala.")
b("Podías probar otros tríos y él te decía si cumplían la regla o no.", "think","focus",[{"k":"check"},{"k":"cross"}])
b("Casi todos pensaban: pares de dos en dos. Y probaban ocho, diez, doce. Sí. Veinte, veintidós, veinticuatro. Sí.", "write","happy",[], bg="classroom", board="8 · 10 · 12 ✓", boards=110, **BOARD, pant="Casi todos pensaban: pares de 2 en 2. Y probaban 8, 10, 12. Sí. 20, 22, 24. Sí.")
b("La regla real era: cualquier número mayor que el anterior.", "shock","shock",[], bg="classroom", board="1 · 2 · 3 ✓", boards=110, **BOARD)
b("Solo seis de veintinueve acertaron a la primera.", "facepalm","dead",[], big="6 / 29", bigc="#e8483f", pant="Solo 6 de 29 acertaron a la primera.")
b("Porque solo probaban ejemplos que confirmaban su idea. Nunca uno que pudiera tumbarla.", "shrug","smirk",[{"k":"cross"}])
b("Al estudiar: cuando te haces un test, no elijas solo las preguntas que sabes. Busca las que te pillan.", "write","focus",["exam",{"k":"question"}])

# --- 4 DUNNING KRUGER
b("Número cuatro: el efecto Dunning Kruger.", "stand","smirk",[{"k":"trophy"}], head="4. DUNNING-KRUGER")
b("En mil novecientos noventa y nueve, Justin Kruger y David Dunning pusieron pruebas de lógica, gramática y humor.", "read","focus",["exam"], bg="lab", pant="En 1999, Justin Kruger y David Dunning pusieron pruebas de lógica, gramática y humor.")
b("Y luego preguntaban a cada uno qué tal creía que lo había hecho comparado con los demás.", "think","neutral",[{"k":"graph"}], bg="lab")
b("Los que peor lo hicieron estaban, de media, en el percentil doce.", "sad","dead",[], big="12", bigc="#e8483f", pant="Los que peor lo hicieron estaban, de media, en el percentil 12.")
b("Ellos creían estar en el sesenta y dos. Por encima de la media.", "cheer","happy",[{"k":"trophy"}], big="62", bigc="#3fb06b", pant="Ellos creían estar en el 62. Por encima de la media.")
b("Para darte cuenta de que algo lo haces mal, necesitas justo lo que te falta: saber hacerlo bien.", "pointup","focus",[{"k":"brain"}])
b("Hay investigadores que discuten cuánto de esto es real y cuánto es estadística. Pero el consejo vale igual.", "shrug","neutral",[{"k":"scale"}])
b("Al estudiar: corrige tus ejercicios con la solución delante, no con tu sensación.", "write","focus",[{"k":"pencil"},{"k":"check"}])

# --- 3 PLANIFICACION
b("Número tres: la falacia de la planificación.", "stand","neutral",[{"k":"calendar"}], head="3. PLANIFICACIÓN")
b("En mil novecientos noventa y cuatro, Roger Buehler preguntó a estudiantes cuánto tardarían en acabar su trabajo de fin de carrera.", "read","focus",["notes"], bg="library", pant="En 1994, Roger Buehler preguntó a estudiantes cuánto tardarían en acabar su trabajo de fin de carrera.")
b("La media de lo que dijeron: treinta y cuatro días.", "point","happy",[{"k":"calendar"}], big="34 días", bigs=110, bigc="#3fb06b", pant="La media de lo que dijeron: 34 días.")
b("La media de lo que tardaron de verdad: cincuenta y cinco.", "shock","shock",[{"k":"alarm","anim":True}], big="55 días", bigs=110, bigc="#e8483f", pant="La media de lo que tardaron de verdad: 55.")
b("Y solo tres de cada diez lo acabaron en el plazo que ellos mismos se habían puesto.", "sad","sad",[{"k":"cross"}], pant="Y solo 3 de cada 10 lo acabaron en el plazo que ellos mismos se habían puesto.")
b("Al planear, imaginas el caso ideal. Sin gripes, sin bloqueos, sin cumpleaños.", "think","smirk",[{"k":"heart"}])
b("Al estudiar: mira cuánto tardaste en el último tema y usa eso. No lo que te gustaría tardar.", "write","focus",[{"k":"clock"},{"k":"notes"}], bg="bedroom", ground=0.7)

# --- 2 PROFUNDIDAD EXPLICATIVA
b("Número dos: la ilusión de profundidad explicativa.", "stand","neutral",[{"k":"question","float":True}], head="2. PROFUNDIDAD")
b("En dos mil dos, Leonid Rozenblit y Frank Keil preguntaron: ¿cuánto entiendes cómo funciona una cremallera, o una cisterna?", "think","happy",[{"k":"water"}], bg="lab", pant="En 2002, Leonid Rozenblit y Frank Keil preguntaron: ¿cuánto entiendes cómo funciona una cremallera, o una cisterna?")
b("La gente se puntuaba alto. Claro que lo entiendo.", "cheer","happy",[{"k":"check"}])
b("Luego les pedían explicarlo paso a paso.", "write","focus",["notes"])
b("Y al volver a puntuarse, la nota bajaba. Al intentar explicarlo, descubrían el agujero.", "facepalm","dead",[{"k":"arrowdown"}])
b("Al estudiar: entender una explicación no es saber explicarla. Cierra el libro y cuéntalo en voz alta, como si dieras la clase.", "point","focus",[{"k":"book"},{"k":"cross"}], bg="classroom", board="EXPLÍCALO TÚ", boards=90, **BOARD)

# --- 1 FLUIDEZ / RELEER
b("Y número uno: la ilusión de fluidez.", "stand","smirk",[{"k":"book"}], head="1. FLUIDEZ", big="#1", bigc="#f6c23e")
b("La que seguramente has tenido esta semana.", "pointup","smirk",[{"k":"calendar"}])
b("En dos mil nueve, Jeffrey Karpicke y su equipo preguntaron a ciento setenta y siete universitarios cómo estudiaban.", "read","focus",["notes"], bg="library", pant="En 2009, Jeffrey Karpicke y su equipo preguntaron a 177 universitarios cómo estudiaban.")
b("El ochenta y cuatro por ciento dijo: releer. Y para más de la mitad era su método principal.", "read","happy",[{"k":"book"}], big="84 %", bigc="#3a7bd5", bg="library", pant="El 84 % dijo: releer. Y para más de la mitad era su método principal.")
b("Ponerse a prueba a uno mismo lo mencionó solo el once por ciento.", "sad","sad",["exam"], big="11 %", bigc="#e8483f", pant="Ponerse a prueba a uno mismo lo mencionó solo el 11 %.")
b("Y es justo al revés de lo que funciona.", "facepalm","dead",[{"k":"cross"}])
b("Cuando relees, todo te suena. Y tu cerebro confunde me suena con me lo sé.", "think","smirk",[{"k":"brain","float":True}])
b("Hasta que llega el examen, la hoja está en blanco, y descubres que solo te sonaba.", "shock","shock",["exam"], bg="classroom", board="EXAMEN", boards=110, **BOARD)
b("Lo que sí funciona: cerrar los apuntes e intentar recordar. Cuesta más, por eso funciona.", "write","focus",[{"k":"pencil"},{"k":"check"}])

# --- EXTRA RETROSPECTIVO
b("Un extra antes de terminar: el sesgo retrospectivo. El famoso ya lo sabía yo.", "pointup","smirk",[{"k":"exclaim"}], head="EXTRA: YA LO SABÍA")
b("En mil novecientos setenta y dos, antes de un viaje del presidente Nixon a China y a la Unión Soviética, Baruch Fischhoff y Ruth Beyth pidieron a estudiantes que apostaran qué iba a pasar.", "read","focus",["notes"], bg="lab", pant="En 1972, antes de un viaje del presidente Nixon a China y a la Unión Soviética, Baruch Fischhoff y Ruth Beyth pidieron a estudiantes que apostaran qué iba a pasar.")
b("Después del viaje, les pidieron recordar lo que habían dicho.", "think","neutral",[{"k":"calendar"}], bg="lab")
b("Y recordaban haber dado más probabilidad a lo que sí había pasado. Su memoria se había corregido sola.", "shock","shock",[{"k":"brain","float":True}], bg="lab")
b("Al estudiar: al corregir un examen piensas, si esto me lo sabía. Antes de ver la solución, apunta qué ibas a responder. Así ves lo que de verdad sabías.", "write","focus",["exam",{"k":"pencil"}])

# --- CIERRE
b("Resumen rápido para que tu cerebro no te la juegue:", "stand","happy",[{"k":"notes"}], head="RESUMEN", pal=3)
b("Uno: ponte a prueba en vez de releer.", "write","focus",["exam",{"k":"check"}], big="1", bigs=110)
b("Dos: explícalo en voz alta sin mirar.", "point","happy",[{"k":"book"}], big="2", bigs=110)
b("Tres: planifica con lo que tardaste de verdad.", "write","focus",[{"k":"clock"}], big="3", bigs=110)
b("Cuatro: busca las preguntas que te pillan, no las que sabes.", "think","focus",[{"k":"question"}], big="4", bigs=110)
b("Y cinco: si un método no funciona, suéltalo aunque le hayas dedicado horas.", "shrug","smirk",[{"k":"ticket"}], big="5", bigs=110)
b("Si te ha servido, aquí tienes todos los tipos de memoria explicados.", "point","happy",[{"k":"brain"}])
b("Y suscríbete. Que el sesgo de confirmación por lo menos te confirme algo bueno.", "cheer","happy",[{"k":"gradeA"}], confetti=True)

g={"titulo":"10 sesgos cognitivos que te engañan al estudiar","lang":"es","cfg":0.0,"expresividad":0.5,"frases":F,"fuentes":[
"Tversky, A. y Kahneman, D. (1973). Availability: A heuristic for judging frequency and probability. Cognitive Psychology, 5(2), 207-232. (105 de 152 participantes juzgaron más probable la primera posición para la mayoría de las letras K, L, N, R, V, más frecuentes en tercera posición.)",
"Arkes, H. R. y Blumer, C. (1985). The psychology of sunk cost. Organizational Behavior and Human Decision Processes, 35, 124-140. (Viaje a Míchigan de 100 $ frente a Wisconsin de 50 $: 33 de 61, el 54 %, eligió Míchigan.)",
"Tversky, A. y Kahneman, D. (1981). The framing of decisions and the psychology of choice. Science, 211, 453-458. (Plan A: 72 %; plan C: 22 %.)",
"Tversky, A. y Kahneman, D. (1974). Judgment under uncertainty: Heuristics and biases. Science, 185, 1124-1131. (Ruleta 10 o 65; medianas 25 % y 45 %.)",
"Asch, S. E. (1951, 1956). Experimentos de conformidad: errores <1 % en el control; ~75 % se conformó al menos una vez; ~37 % de conformidad en los ensayos críticos.",
"Wason, P. C. (1960). On the failure to eliminate hypotheses in a conceptual task. Quarterly Journal of Experimental Psychology, 12, 129-140. (6 de 29 anunciaron la regla correcta al primer intento.)",
"Kruger, J. y Dunning, D. (1999). Unskilled and unaware of it. Journal of Personality and Social Psychology, 77(6), 1121-1134. (Cuartil inferior: percentil 12 real, 62 estimado.) El efecto se debate en la literatura posterior.",
"Buehler, R., Griffin, D. y Ross, M. (1994). Exploring the planning fallacy. Journal of Personality and Social Psychology, 67, 366-381. (Estimación media 33,9 días; real 55,5; ~30 % a tiempo.)",
"Rozenblit, L. y Keil, F. (2002). The misunderstood limits of folk science: an illusion of explanatory depth. Cognitive Science, 26, 521-562.",
"Fischhoff, B. y Beyth, R. (1975). «I knew it would happen»: Remembered probabilities of once-future things. Organizational Behavior and Human Performance, 13, 1-16. (Viaje de Nixon a China y la URSS en 1972.)",
"Karpicke, J. D., Butler, A. C. y Roediger, H. L. (2009). Metacognitive strategies in student learning: Do students practise retrieval when they study on their own? Memory, 17(4), 471-479. (177 estudiantes: 84 % relectura, 55 % como estrategia principal; 11 % autoevaluación.)"]}
json.dump(g,open("guion.json","w"),ensure_ascii=False,indent=1)
w=sum(len(f["t"].split()) for f in F); c=sum(len(f["t"]) for f in F)
print(len(F),"frases",w,"palabras",round(c/13),"s aprox")
