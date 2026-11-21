# Guion del largo es-l05: cómo preparar un examen en 7 días. Ejecuta: python3 gen.py
import json
F=[]
def b(t, pose="stand", face="neutral", props=(), big=None, head=None, bg=None, pant=None, x=0.32, tono=None, two=None, hold=None, **kw):
    v={"chars":[{"x":x,"pose":pose,"face":face}]}
    if hold: v["chars"][0]["hold"]=hold
    if kw.get("flip"): v["chars"][0]["flip"]=kw.pop("flip")
    if two: v["chars"].append(dict(id="b",flip=True,**two))
    pr=[]
    for i,p in enumerate(props):
        if isinstance(p,str): p={"k":p}
        p.setdefault("x",[0.66,0.8,0.56][i%3]); p.setdefault("y",[0.42,0.42,0.3][i%3]); p.setdefault("s",0.8); p.setdefault("d",0.15*i)
        pr.append(p)
    if pr and not kw.get("board"): v["props"]=pr
    if big: v.update(big=big,bigx=kw.pop("bigx",0.66),bigy=kw.pop("bigy",0.3),bigs=kw.pop("bigs",130))
    if head: v["head"]=head; v["wipe"]=True
    if bg: v["bg"]=bg
    v["ground"]=kw.pop("ground",0.8 if not bg else 0.82)
    v.update(kw)
    f={"t":t,"v":v,"esc":"A"}
    if pant: f["pantalla"]=pant
    if tono: f["tono"]=tono
    F.append(f)
BOARD=dict(x=0.84, flip=True)

# --- INTRO
b("Tienes un examen en siete días y no has empezado.", "shock","shock",[{"k":"calendar"},{"k":"alarm","anim":True}], big="7 DÍAS", bigc="#e8483f", tono="gancho, directo, un poco dramático", pant="Tienes un examen en 7 días y no has empezado.")
b("Tranquilo. Siete días dan para mucho, si los usas bien.", "shrug","smirk",[{"k":"check"}], tono="calma, de colega", pant="Tranquilo. 7 días dan para mucho, si los usas bien.")
b("En este vídeo tienes el plan exacto, día por día. Qué hacer, cuánto tiempo, y con qué aplicaciones gratis.", "point","happy",[{"k":"notes"},{"k":"phone"}])
b("Y al final, los cuatro errores que hacen que estudies mucho y apruebes poco.", "pointup","smirk",[{"k":"cross"}], pant="Y al final, los 4 errores que hacen que estudies mucho y apruebes poco.")
b("Coge papel. Empezamos.", "walk","happy",[{"k":"pencil"}], walk=0.05, pal=1)

# --- LAS DOS REGLAS
b("Antes del plan, dos reglas. Todo lo demás sale de aquí.", "stand","focus",[{"k":"book"}], head="LAS 2 REGLAS", tono="explicativo")
b("Regla uno: ponte a prueba en vez de releer.", "pointup","focus",["exam",{"k":"check"}], big="1", bigs=110)
b("En dos mil seis, en la Universidad de Washington en San Luis, unos estudiantes leyeron un texto.", "read","focus",["notes"], bg="lab", pant="En 2006, en la Universidad de Washington en San Luis, unos estudiantes leyeron un texto.")
b("Unos lo releyeron varias veces. Otros lo leyeron una vez y luego intentaron recordarlo, sin mirar, tres veces.", "write","focus",[{"k":"book"},{"k":"pencil"}], bg="lab")
b("Una semana después, los que se pusieron a prueba recordaban el sesenta y uno por ciento. Los que releyeron, el cuarenta.", "cheer","happy",[{"k":"graph"}], big="61 % vs 40 %", bigs=100, bigc="#3fb06b", pant="Una semana después, los que se pusieron a prueba recordaban el 61 %. Los que releyeron, el 40 %.")
b("Lo curioso: cinco minutos después de estudiar, ganaban los que releían. Por eso releer engaña: parece que funciona.", "think","smirk",[{"k":"clock"}], pant="Lo curioso: 5 minutos después de estudiar, ganaban los que releían. Por eso releer engaña: parece que funciona.", tono="como quien cuenta un secreto")
b("Regla dos: repasa con días de por medio.", "pointup","focus",[{"k":"calendar"}], big="2", bigs=110)
b("En dos mil ocho, un estudio con más de mil trescientas personas buscó el mejor momento para repasar.", "read","focus",[{"k":"graph"}], bg="lab", pant="En 2008, un estudio con más de 1.300 personas buscó el mejor momento para repasar.")
b("La conclusión: cuanto más lejos está el examen, más espacio debes dejar entre repasos.", "point","happy",[{"k":"calendar"},{"k":"arrowup"}], bg="lab")
b("Para un examen a una semana, eso es repasar cada uno o dos días. No todo el último día.", "write","focus",[{"k":"calendar"},{"k":"check"}], pant="Para un examen a una semana, eso es repasar cada 1 o 2 días. No todo el último día.")
b("Con estas dos reglas, vamos al plan.", "walk","happy",[], walk=0.05)

# --- DÍA 0
b("Hoy. Día cero. Media hora para organizarte.", "stand","focus",[{"k":"clock"}], head="HOY: DÍA 0", pal=2, tono="enérgico, empieza el plan", pant="Hoy. Día 0. Media hora para organizarte.")
b("Primero: reúne todo lo que entra. Temas, apuntes, ejercicios y, sobre todo, exámenes de otros años.", "read","focus",["notes",{"k":"book"}])
b("Y ponte un objetivo realista: qué nota quieres y cuántas horas al día puedes estudiar de verdad. Si son tres, son tres.", "think","focus",[{"k":"clock"},{"k":"trophy"}])
b("Los exámenes antiguos te dicen qué preguntan y cómo. Son el mapa del tesoro.", "point","happy",["exam",{"k":"trophy"}])
b("Segundo: divide el temario en bloques pequeños, de una o dos horas cada uno.", "write","focus",[{"k":"notes"},{"k":"pencil"}], pant="Segundo: divide el temario en bloques pequeños, de 1 o 2 horas cada uno.")
b("Tercero: mételos en el calendario. Yo uso Google Calendar, que es gratis: un evento por bloque, con hora de inicio y de fin.", "point","happy",[{"k":"calendar"},{"k":"phone"}])
b("Si no está en el calendario, no existe. Estudiar cuando me apetezca no funciona.", "shrug","smirk",[{"k":"cross"}])
b("Y deja huecos libres. Algo saldrá mal, y es mejor que tengas sitio para recuperarlo.", "think","neutral",[{"k":"calendar"}])

# --- DÍAS 1 y 2
b("Días uno y dos: primera vuelta al temario. Pero activa.", "stand","focus",[{"k":"book"}], head="DÍAS 1 Y 2", pal=3, pant="Días 1 y 2: primera vuelta al temario. Pero activa.")
b("Para cada bloque: lee una sección con calma, hasta entenderla.", "read","focus",[{"k":"book"}], bg="library")
b("Luego cierra el libro y escribe todo lo que recuerdes en una hoja en blanco. Sin mirar.", "write","focus",[{"k":"notes"},{"k":"pencil"}], bg="library", tono="insistiendo en «sin mirar»")
b("Cuando no puedas más, abre el libro y compara. Lo que se te olvidó, en rojo.", "think","focus",[{"k":"check"},{"k":"cross"}], bg="library")
b("Ese hueco en rojo es justo lo que tienes que estudiar. Lo demás ya lo sabes.", "point","happy",[{"k":"arrowup"}])
b("Y mientras, haz tarjetas de pregunta y respuesta. Una idea por tarjeta.", "write","happy",[{"k":"card"}])
b("¿De qué? De lo que tienes que saber de memoria: definiciones, fechas, fórmulas, vocabulario. Lo que se entiende, se practica con ejercicios.", "think","focus",[{"k":"card"},{"k":"pencil"}])
b("Para eso, Anki. Te enseña cada tarjeta justo antes de que la olvides.", "point","happy",[{"k":"card"},{"k":"brain"}])
b("Cada día te dice cuántas tarjetas tocan. Hazlas todas, aunque sean pocas. La constancia es lo que funciona.", "read","happy",[{"k":"card"},{"k":"check"}])
b("Es gratis en el ordenador, en Android y en la web. En iPhone la aplicación es de pago, un solo pago, unos veinticinco dólares en Estados Unidos. Pero puedes usar la web gratis.", "think","neutral",[{"k":"phone"},{"k":"check"}], pant="Es gratis en el ordenador, en Android y en la web. En iPhone la aplicación es de pago, un solo pago, unos 25 dólares en EE. UU. Pero puedes usar la web gratis.", tono="informativo, honesto")
b("Si prefieres algo más sencillo, Quizlet. La versión gratis vale para hacer y repasar tarjetas. Algunos modos, como el de aprendizaje sin límites, son de pago.", "point","neutral",[{"k":"card"},{"k":"phone"}])
b("Nadie nos paga por nombrarlas. Son las que funcionan.", "shrug","smirk",[{"k":"heart"}])

# --- POMODORO / FOCO
b("¿Y cómo aguantas horas estudiando? No las aguantas. Haces bloques.", "think","focus",[{"k":"clock"}], head="CÓMO CONCENTRARTE", pal=4)
b("La técnica Pomodoro: veinticinco minutos de estudio, cinco de descanso. Cada cuatro, un descanso largo.", "point","happy",[{"k":"clock"},{"k":"coffee"}], big="25 + 5", bigs=110, pant="La técnica Pomodoro: 25 minutos de estudio, 5 de descanso. Cada 4, un descanso largo.")
b("Vale cualquier temporizador. El del móvil, o uno de cocina.", "shrug","smirk",[{"k":"alarm"}])
b("En los descansos, levántate, bebe agua y estira. Nada de redes: te comen el descanso y la cabeza.", "cheer","happy",[{"k":"water"},{"k":"cross"}])
b("Y el móvil, en otra habitación. Boca abajo en la mesa no basta: sigue llamándote.", "point","focus",[{"k":"phone"},{"k":"cross"}])
b("Si lo necesitas cerca, Forest: plantas un árbol virtual que se muere si sales de la aplicación.", "cheer","happy",[{"k":"phone"},{"k":"check"}])
b("En iPhone cuesta unos cuatro dólares, un solo pago. En Android hay versión gratis. Y colaboran con una organización que planta árboles de verdad.", "point","happy",[{"k":"heart"}], pant="En iPhone cuesta unos 4 dólares, un solo pago. En Android hay versión gratis. Y colaboran con una organización que planta árboles de verdad.")

# --- DÍA 3
b("Día tres: repaso y ejercicios.", "stand","focus",[{"k":"pencil"}], head="DÍA 3", pal=5, pant="Día 3: repaso y ejercicios.")
b("Empieza con las tarjetas de Anki que te toquen hoy. Diez o quince minutos.", "read","focus",[{"k":"card"},{"k":"phone"}], pant="Empieza con las tarjetas de Anki que te toquen hoy. 10 o 15 minutos.")
b("Y luego, ejercicios del tipo que cae en el examen. Si es de problemas, problemas. Si es de desarrollar, escribe respuestas de verdad.", "write","focus",["exam",{"k":"pencil"}])
b("Mezcla ejercicios de temas distintos. Así aprendes a reconocer qué te están pidiendo, como en el examen real.", "think","focus",[{"k":"card"},{"k":"question"}])
b("Y si uno te sale mal, no mires la solución enseguida. Inténtalo cinco minutos más. Ese esfuerzo es lo que te lo deja grabado.", "think","focus",[{"k":"clock"},{"k":"brain"}], pant="Y si uno te sale mal, no mires la solución enseguida. Inténtalo 5 minutos más. Ese esfuerzo es lo que te lo deja grabado.")
b("Y sigue con la primera vuelta a los bloques que te queden.", "read","neutral",[{"k":"book"}])

# --- DÍA 4
b("Día cuatro: el simulacro.", "stand","shock",[{"k":"exam"}], head="DÍA 4: SIMULACRO", pal=0, tono="serio, este día importa", pant="Día 4: el simulacro.")
b("Coge un examen de otro año y hazlo entero, con el tiempo real, sin apuntes y sin móvil.", "write","focus",["exam",{"k":"clock"}], bg="classroom", board="SIMULACRO", boards=90, x=0.8, flip=True)
b("Da miedo. Por eso funciona: te dice dónde estás de verdad, no dónde crees que estás.", "shock","shock",[{"k":"eye"}])
b("Corrígelo con la solución delante. Y apunta cada fallo en una lista: la lista de errores.", "write","focus",[{"k":"notes"},{"k":"cross"}])
b("Esa lista vale más que todos tus apuntes juntos.", "point","happy",[{"k":"trophy"}])
b("Y no te agobies con la nota. Es un diagnóstico, no una sentencia.", "shrug","smirk",[{"k":"heart"}], tono="tranquilizador")

# --- DÍA 5
b("Día cinco: a por tus puntos débiles.", "stand","focus",[{"k":"arrowup"}], head="DÍA 5", pal=1, pant="Día 5: a por tus puntos débiles.")
b("Coge la lista de errores y ataca primero lo que más falla. No lo que más te gusta.", "point","focus",[{"k":"notes"},{"k":"cross"}])
b("Para cada error, vuelve a la teoría, entiende por qué fallaste y haz dos o tres ejercicios parecidos.", "write","focus",[{"k":"book"},{"k":"pencil"}], pant="Para cada error, vuelve a la teoría, entiende por qué fallaste y haz 2 o 3 ejercicios parecidos.")
b("Un truco: explícalo en voz alta como si dieras la clase. Si te atascas, ahí hay un hueco.", "point","happy",[{"k":"bulb","anim":True}], bg="classroom", board="EXPLÍCALO", boards=80, **BOARD)
b("Y por supuesto, tus tarjetas del día.", "read","happy",[{"k":"card"}])

# --- DÍA 6
b("Día seis: segundo simulacro.", "stand","focus",[{"k":"exam"}], head="DÍA 6", pal=2, pant="Día 6: segundo simulacro.")
b("Otro examen distinto, en las mismas condiciones. Y compara la nota con la del día cuatro.", "write","focus",["exam",{"k":"graph"}], pant="Otro examen distinto, en las mismas condiciones. Y compara la nota con la del día 4.")
b("Si has subido, el plan funciona. Si algo sigue fallando, ya sabes qué repasar mañana por la mañana.", "cheer","happy",[{"k":"arrowup"},{"k":"check"}])
b("Y antes de cenar, repasa la lista de errores. Los que ya no fallas, táchalos. Ver cómo se acorta da mucha moral.", "write","happy",[{"k":"notes"},{"k":"check"}])

# --- DÍA 7
b("Día siete: la víspera.", "stand","neutral",[{"k":"moon"}], head="DÍA 7: LA VÍSPERA", bg="bedroom", tono="más tranquilo", pant="Día 7: la víspera.")
b("Hoy no se aprende nada nuevo. Se repasa.", "point","focus",[{"k":"cross"},{"k":"book"}], bg="bedroom")
b("Por la mañana: tarjetas, la lista de errores y un resumen de una página por tema, hecho por ti y de memoria.", "write","focus",[{"k":"notes"},{"k":"card"}])
b("Por la tarde: prepara lo que necesitas. Bolígrafos, calculadora, documento de identidad, y cómo vas a llegar.", "read","happy",[{"k":"pencil"},{"k":"check"}])
b("Y por la noche, a dormir a tu hora.", "stand","happy",[{"k":"bed"},{"k":"zzz","float":True}], bg="bedroom")
b("Dormir no es tiempo perdido: mientras duermes, el cerebro afianza lo que estudiaste.", "point","happy",[{"k":"brain"},{"k":"moon"}], bg="bedroom")
b("Hay estudios que muestran que después de una noche sin dormir, se aprende hasta un cuarenta por ciento peor al día siguiente.", "shock","shock",[{"k":"battery"}], big="−40 %", bigs=110, bigc="#e8483f", bg="bedroom", pant="Hay estudios que muestran que después de una noche sin dormir, se aprende hasta un 40 % peor al día siguiente.")

# --- EL DÍA DEL EXAMEN
b("Y el día del examen, tres cosas.", "stand","happy",[{"k":"exam"}], head="EL DÍA D", pal=3, pant="Y el día del examen, 3 cosas.")
b("Una: desayuna algo y llega con tiempo. Correr te sube los nervios.", "walk","happy",[{"k":"coffee"}], walk=0.05)
b("Dos: lee todo el examen antes de empezar, y reparte el tiempo según lo que vale cada pregunta.", "read","focus",["exam",{"k":"clock"}])
b("Tres: empieza por lo que sabes. Coges confianza y aseguras puntos.", "write","happy",["exam",{"k":"check"}])
b("Y si te bloqueas en una pregunta, márcala y sigue. Vuelves al final con la cabeza más fría.", "point","focus",[{"k":"question"},{"k":"arrowup"}])

# --- ERRORES
b("Ahora, los cuatro errores que hacen que estudies mucho y apruebes poco.", "pointup","smirk",[{"k":"cross"}], head="4 ERRORES", pal=4, pant="Ahora, los 4 errores que hacen que estudies mucho y apruebes poco.")
b("Error uno: releer y subrayar. Es lo más cómodo y de lo que menos funciona. Una revisión de cientos de estudios lo puso de los últimos de la lista.", "facepalm","sad",[{"k":"book"},{"k":"cross"}], big="1", bigs=100, pant="Error 1: releer y subrayar. Es lo más cómodo y de lo que menos funciona. Una revisión de cientos de estudios lo puso de los últimos de la lista.")
b("Error dos: pasar horas haciendo apuntes bonitos. Si no te pones a prueba con ellos, son decoración.", "write","smirk",[{"k":"pencil"},{"k":"heart"}], big="2", bigs=100, pant="Error 2: pasar horas haciendo apuntes bonitos. Si no te pones a prueba con ellos, son decoración.")
b("Error tres: el atracón del último día. Lo que entra deprisa, sale deprisa.", "sitsad","dead",[{"k":"coffee"},{"k":"moon"}], big="3", bigs=100, pant="Error 3: el atracón del último día. Lo que entra deprisa, sale deprisa.")
b("Error cuatro: estudiar con el móvil al lado. Cada notificación te saca del tema, aunque no la mires.", "read","shock",[{"k":"phone","anim":True}], big="4", bigs=100, pant="Error 4: estudiar con el móvil al lado. Cada notificación te saca del tema, aunque no la mires.")

# --- 3 DÍAS
b("¿Y si solo tienes tres días? El mismo plan, comprimido.", "shock","shock",[{"k":"calendar"},{"k":"alarm","anim":True}], head="¿Y SI SOLO TENGO 3 DÍAS?", pal=0, pant="¿Y si solo tienes 3 días? El mismo plan, comprimido.")
b("Día uno: organízate, y primera vuelta activa a lo más importante. Lo que más cae en los exámenes antiguos.", "write","focus",["exam",{"k":"notes"}], big="1", bigs=100, pant="Día 1: organízate, y primera vuelta activa a lo más importante. Lo que más cae en los exámenes antiguos.")
b("Día dos: simulacro por la mañana y errores por la tarde.", "write","focus",["exam",{"k":"cross"}], big="2", bigs=100, pant="Día 2: simulacro por la mañana y errores por la tarde.")
b("Día tres: repaso de errores y tarjetas, y a dormir pronto. Sin trasnochar.", "stand","happy",[{"k":"moon"},{"k":"bed"}], big="3", bigs=100, pant="Día 3: repaso de errores y tarjetas, y a dormir pronto. Sin trasnochar.")
b("No llegarás a todo. Pero llegarás a lo que más puntos da.", "shrug","smirk",[{"k":"trophy"}])

# --- RESUMEN
b("Resumen del plan:", "stand","happy",[{"k":"notes"}], head="RESUMEN", pal=5)
b("Hoy, organiza y mételo en el calendario.", "write","focus",[{"k":"calendar","x":0.84,"y":0.5}], big="0", bigs=110)
b("Días uno y dos, primera vuelta activa y tarjetas.", "read","focus",[{"k":"card","x":0.84,"y":0.5}], big="1-2", bigs=110, pant="Días 1 y 2, primera vuelta activa y tarjetas.")
b("Día tres, ejercicios mezclados.", "write","focus",[{"k":"pencil","x":0.84,"y":0.5}], big="3", bigs=110, pant="Día 3, ejercicios mezclados.")
b("Día cuatro, simulacro y lista de errores.", "write","focus",[{"k":"exam","x":0.84,"y":0.5}], big="4", bigs=110, pant="Día 4, simulacro y lista de errores.")
b("Día cinco, puntos débiles. Día seis, segundo simulacro.", "point","happy",[{"k":"arrowup","x":0.84,"y":0.5}], big="5-6", bigs=110, pant="Día 5, puntos débiles. Día 6, segundo simulacro.")
b("Y día siete, repaso ligero y a dormir.", "stand","happy",[{"k":"moon","x":0.84,"y":0.5}], big="7", bigs=110, pant="Y día 7, repaso ligero y a dormir.")
b("Si te sirve, guarda el vídeo para la próxima vez. Y cuéntame en los comentarios para qué examen lo vas a usar.", "point","happy",[{"k":"heart"}], tono="cercano")
b("Suerte. Aunque con este plan, la vas a necesitar menos.", "cheer","happy",[{"k":"trophy"}], confetti=True, tono="remate con sonrisa")

g={"titulo":"Cómo preparar un examen en 7 días (plan día por día)","lang":"es","frases":F,"fuentes":[
"Roediger, H. L. y Karpicke, J. D. (2006). Test-enhanced learning: Taking memory tests improves long-term retention. Psychological Science, 17(3), 249-255. (Nota de prensa de la Universidad de Washington en San Luis: a la semana, 61 % frente a 40 %; a los 5 minutos, releer 81 % frente a 75 %.)",
"Cepeda, N. J., Vul, E., Rohrer, D., Wixted, J. T. y Pashler, H. (2008). Spacing effects in learning: A temporal ridgeline of optimal retention. Psychological Science, 19(11), 1095-1102. (Más de 1.350 personas; el hueco óptimo entre repasos crece con la distancia al examen: en torno al 20-40 % para un examen a una semana.)",
"Dunlosky, J., Rawson, K. A., Marsh, E. J., Nathan, M. J. y Willingham, D. T. (2013). Improving students' learning with effective learning techniques. Psychological Science in the Public Interest, 14(1), 4-58. (Autoevaluación y práctica espaciada: utilidad alta; subrayar y releer: utilidad baja.)",
"Yoo, S.-S., Hu, P. T., Gujar, N., Jolesz, F. A. y Walker, M. P. (2007). A deficit in the ability to form new human memories without sleep. Nature Neuroscience, 10, 385-392. (Hasta un 40 % peor tras una noche sin dormir.)",
"Anki: escritorio, AnkiDroid y AnkiWeb gratis; AnkiMobile (iPhone) de pago único, 24,99 $ en EE. UU. (apps.ankiweb.net y docs.ankiweb.net, consultado el 21/11/2026).",
"Quizlet: plan gratis con tarjetas y repaso; Learn y Test limitados; Quizlet Plus de pago (quizlet.com, consultado el 21/11/2026).",
"Forest: 3,99 $ pago único en iOS; versión gratis en Android; colaboración con Trees for the Future (forestapp.cc y App Store, consultado el 21/11/2026).",
"Técnica Pomodoro: Francesco Cirillo (bloques de 25 minutos y pausas de 5)."]}
json.dump(g,open("guion.json","w"),ensure_ascii=False,indent=1)
w=sum(len(f["t"].split()) for f in F)
print(len(F),"frases",w,"palabras ≈",round(w/2.5/60,1),"min a 2,5 palabras/s")
