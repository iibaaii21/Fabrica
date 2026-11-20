# Generador del guion de es-l02 (texto + visuales). Ejecuta: python3 gen.py
import json
F=[]
def b(t, pose="stand", face="neutral", props=(), big=None, head=None, bg=None, pant=None, x=0.32, say=None, hold=None, two=None, **kw):
    v={"chars":[{"x":x,"pose":pose,"face":face}]}
    if say: v["chars"][0]["say"]=say
    if hold: v["chars"][0]["hold"]=hold
    if two: v["chars"].append(dict(id="b",flip=True,**two))
    pr=[]
    for i,p in enumerate(props):
        if isinstance(p,str): p={"k":p}
        p.setdefault("x",[0.7,0.82,0.58][i%3]); p.setdefault("y",[0.4,0.25,0.3][i%3]); p.setdefault("s",0.8); p.setdefault("d",0.15*i)
        pr.append(p)
    if pr: v["props"]=pr
    if big: v.update(big=big,bigx=kw.pop("bigx",0.68),bigy=kw.pop("bigy",0.3),bigs=kw.pop("bigs",130))
    if head: v["head"]=head; v["wipe"]=True
    if bg: v["bg"]=bg
    v["ground"]=kw.pop("ground",0.8 if not bg else 0.82)
    v.update(kw)
    f={"t":t,"v":v,"esc":"A"}
    if pant: f["pantalla"]=pant
    F.append(f)

# --- INTRO
b("Tienes al menos diez memorias distintas dentro de la cabeza.", "shock","shock",["brain"], big="10", bigc="#f6c23e")
b("Y una de ellas te está mintiendo ahora mismo.", "think","smirk",[{"k":"question","float":True}])
b("Hoy vamos a ver todos los tipos de memoria, de la que dura menos de un segundo a la que dura toda la vida.", "point","happy",["clock","calendar"])
b("Y al final, la que más te importa para aprobar.", "cheer","happy",["gradeA"])
b("Vamos a ello.", "walk","happy",[], walk=0.05, pal=1)

# --- 1 SENSORIAL ICONICA
b("Número uno: la memoria icónica.", "stand","neutral",[{"k":"bulb","anim":True}], head="1. MEMORIA ICÓNICA")
b("Cada cosa que ves deja una foto en tu cerebro.", "point","happy",[{"k":"phone"}])
b("Pero esa foto se borra en menos de un segundo.", "shock","shock",[], big="<1 s", bigc="#3a7bd5")
b("En mil novecientos sesenta, George Sperling enseñaba a la gente una cuadrícula de letras durante un instante.", "read","focus",["card","card"], pant="En 1960, George Sperling enseñaba a la gente una cuadrícula de letras durante un instante.", bg="lab")
b("Si les pedía todas las letras, solo recordaban unas cuatro.", "shrug","sad",[], big="4", bg="lab")
b("Pero si justo después les señalaba una sola fila, la recordaban casi entera.", "pointup","shock",[{"k":"check"}], bg="lab")
b("Es decir: lo habían visto todo. Simplemente, la foto se borró antes de poder leerla.", "facepalm","sad",[{"k":"cross"}], bg="lab")
b("Por eso puedes leer un párrafo entero y no saber qué decía.", "sitsad","dead",["book"])

# --- 2 ECOICA
b("Número dos: la memoria ecoica.", "stand","neutral",[], head="2. MEMORIA ECOICA")
b("Es lo mismo, pero con el oído. Y aguanta un poco más: unos segundos.", "think","neutral",[{"k":"clock"}], big="~3 s", bigc="#3fb06b")
b("¿Te ha pasado que alguien te pregunta algo, dices: ¿qué?, y antes de que te lo repita ya lo has entendido?", "shrug","shock",[{"k":"question"}], two=dict(x=0.72,pose="point",face="angry"), x=0.3)
b("Eso es tu memoria ecoica, rebobinando el sonido.", "point","smirk",[{"k":"exclaim"}])

# --- 3 CORTO PLAZO
b("Número tres: la memoria a corto plazo.", "stand","neutral",[], head="3. CORTO PLAZO")
b("Es donde guardas un número de teléfono mientras lo marcas.", "hold","focus",[], hold="phone")
b("En mil novecientos cincuenta y nueve, Lloyd y Margaret Peterson pidieron a estudiantes recordar tres letras.", "read","focus",[{"k":"card"}], pant="En 1959, Lloyd y Margaret Peterson pidieron a estudiantes recordar tres letras.", bg="lab")
b("Pero mientras esperaban, les hacían contar hacia atrás de tres en tres, para que no pudieran repetirlas.", "dizzy","dead",[{"k":"question"}], bg="lab")
b("A los tres segundos, acertaban casi siempre.", "cheer","happy",[{"k":"check"}], big="80%", bigc="#3fb06b", bg="lab", pant="A los 3 segundos, acertaban casi siempre.")
b("A los dieciocho segundos, apenas uno de cada diez.", "fall","dead",[{"k":"cross"}], big="10%", bg="lab", pant="A los 18 segundos, apenas 1 de cada 10.")
b("Dieciocho segundos. Lo que tardas en mirar una notificación.", "shock","shock",[{"k":"phone"}], big="18 s", pant="18 segundos. Lo que tardas en mirar una notificación.")
b("Así que si estudias con el móvil al lado, cada vibración es un borrado.", "facepalm","sad",[{"k":"phone"},{"k":"exclaim"}])

# --- 4 TRABAJO
b("Número cuatro: la memoria de trabajo.", "stand","neutral",[], head="4. MEMORIA DE TRABAJO")
b("No solo guarda cosas: las usa.", "think","focus",[{"k":"bulb","anim":True}])
b("Es la que trabaja cuando haces una cuenta de cabeza, o cuando sigues una explicación de clase.", "write","focus",["exam"], bg="classroom", board="27 x 4 = ?")
b("En mil novecientos setenta y cuatro, Alan Baddeley y Graham Hitch la describieron como un pequeño equipo:", "point","neutral",[], pant="En 1974, Alan Baddeley y Graham Hitch la describieron como un pequeño equipo:", bg="classroom", board="BADDELEY & HITCH")
b("una parte para los sonidos, otra para las imágenes, y un jefe que reparte la atención.", "pointup","happy",[{"k":"zzz","s":0.0001},{"k":"bulb"},{"k":"brain"}], bg="classroom")
b("Y tiene un límite muy pequeño.", "sad","sad",[{"k":"battery","anim":"low"}])
b("Durante años se dijo que eran siete cosas, más o menos dos.", "shrug","neutral",[], big="7±2")
b("Hoy muchos investigadores creen que, en realidad, son unas cuatro.", "shock","shock",[], big="4", bigc="#8a5cd6")
b("Por eso, cuando un profesor explica diez cosas seguidas, a partir de la quinta ya no te enteras.", "sitsad","dead",["notes"], bg="classroom", board="1 2 3 4 5 6 7 8 9 10", boards=64)
b("Truco: agrupa. Un número de nueve cifras son tres grupos de tres. Y tres grupos sí caben.", "point","smirk",[{"k":"check"}], big="3·3·3", bigc="#3fb06b")

# --- 5 EPISODICA
b("Ahora pasamos a la memoria a largo plazo, que tiene varios cajones.", "walk","happy",[], walk=0.04, pal=2)
b("Número cinco: la memoria episódica.", "stand","neutral",[], head="5. EPISÓDICA")
b("Son tus recuerdos de cosas que te pasaron a ti: con un sitio, un momento y una emoción.", "think","happy",[{"k":"heart"},{"k":"calendar"}])
b("Tu primer día de instituto. Aquella vez que hiciste el ridículo en clase.", "facepalm","sad",[], bg="classroom", board="¿QUIÉN SABE LA RESPUESTA?", boards=58)
b("El psicólogo Endel Tulving la separó de los demás tipos en mil novecientos setenta y dos.", "read","focus",["book"], pant="El psicólogo Endel Tulving la separó de los demás tipos en 1972.")
b("Es como viajar en el tiempo, pero hacia atrás.", "run","happy",[{"k":"clock"}])

# --- 6 SEMANTICA
b("Número seis: la memoria semántica.", "stand","neutral",[], head="6. SEMÁNTICA")
b("Son los datos que sabes, aunque no recuerdes cuándo los aprendiste.", "think","neutral",["book","notes"])
b("Sabes que París es la capital de Francia. Pero, ¿te acuerdas del día en que lo aprendiste?", "shrug","smirk",[{"k":"question"}])
b("Exacto. Eso es semántica.", "point","happy",[{"k":"check"}])
b("Y aquí va la clave para estudiar: casi todo lo que te sale en un examen es memoria semántica.", "pointup","focus",["exam"], big="EXAMEN", bigs=110)
b("Pero se construye mejor si primero lo conviertes en episodio: un ejemplo, una historia, algo que te pase a ti.", "cheer","happy",[{"k":"bulb","anim":True}])

# --- 7 PROCEDIMENTAL
b("Número siete: la memoria procedimental.", "stand","neutral",[], head="7. PROCEDIMENTAL")
b("Montar en bici, escribir en el teclado, atarte los cordones.", "run","happy",[{"k":"gamepad"}])
b("Sabes hacerlo, pero intenta explicarlo con palabras.", "shrug","dead",[{"k":"question"}])
b("La prueba más famosa es la de un paciente llamado Henry Molaison.", "stand","neutral",[], bg="lab")
b("Tras una operación de cerebro en los años cincuenta, Henry no podía formar recuerdos nuevos.", "sad","sad",[{"k":"brain"}], bg="lab")
b("La psicóloga Brenda Milner le pidió que dibujara una estrella mirando solo su reflejo en un espejo.", "write","focus",[{"k":"pencil"}], bg="lab")
b("Cada día, Henry juraba que era la primera vez que lo hacía.", "shrug","shock",[{"k":"question"}], bg="lab")
b("Y cada día lo hacía mejor.", "cheer","happy",[{"k":"arrowup"}], bg="lab")
b("Su mano recordaba lo que su mente había olvidado.", "pointup","smirk",[{"k":"exclaim"}], bg="lab")
b("Por eso los problemas de matemáticas se aprenden haciéndolos, no mirando cómo se hacen.", "write","focus",["exam",{"k":"check"}], bg="classroom", board="x² + 2x = 8")

# --- 8 PRIMING
b("Número ocho: el priming, o memoria implícita.", "stand","neutral",[], head="8. PRIMING")
b("Es lo que has visto o oído hace poco y te influye sin que te des cuenta.", "think","smirk",[{"k":"bulb"}])
b("Si hace un rato has leído la palabra amarillo, reconocerás antes la palabra plátano.", "point","happy",[], big="AMARILLO", bigc="#f6c23e", bigs=100)
b("No lo decides tú. Tu cerebro ya tenía la puerta medio abierta.", "shrug","neutral",[{"k":"question"}])
b("Por eso un repaso rápido justo antes de empezar un examen te ayuda a arrancar.", "read","happy",["notes"])

# --- 9 PROSPECTIVA
b("Número nueve: la memoria prospectiva.", "stand","neutral",[], head="9. PROSPECTIVA")
b("Es acordarte de hacer algo en el futuro.", "think","neutral",[{"k":"calendar"}])
b("Entregar el trabajo el jueves. Llevar la calculadora al examen.", "shock","shock",[{"k":"alarm","anim":True}])
b("Y es de las que más fallan, porque nadie te avisa del momento justo.", "facepalm","sad",[{"k":"cross"}])
b("El truco es atarla a algo que vas a ver seguro: la calculadora, encima de las llaves.", "point","smirk",[{"k":"check"}])
b("O, mejor aún, una alarma en el móvil. Tu cerebro no es una agenda.", "hold","happy",[{"k":"alarm","anim":True}], hold="phone")

# --- 10 FLASH
b("Número diez: las memorias flash.", "stand","neutral",[], head="10. MEMORIAS FLASH")
b("Son esos recuerdos de noticias tan impactantes que crees recordar con todo detalle dónde estabas.", "shock","shock",[{"k":"exclaim"}])
b("Al día siguiente del once de septiembre de dos mil uno, dos investigadores de la Universidad de Duke pidieron a estudiantes que escribieran cómo se enteraron.", "write","focus",["notes"], pant="Al día siguiente del 11 de septiembre de 2001, dos investigadores de la Universidad de Duke pidieron a estudiantes que escribieran cómo se enteraron.", bg="lab")
b("Semanas y meses después, les volvieron a preguntar.", "think","neutral",[{"k":"calendar"}], bg="lab")
b("Sus recuerdos habían cambiado tanto como los de un día cualquiera.", "sad","sad",[{"k":"arrowdown"}], bg="lab")
b("La diferencia es que de ese recuerdo seguían totalmente seguros.", "cheer","smirk",[], big="100%", bigc="#f6c23e", bg="lab")
b("Sentirte seguro de un recuerdo no significa que sea verdad.", "pointup","focus",[{"k":"exclaim"}])

# --- 11 FALSA
b("Y número once: la memoria falsa. La que te miente.", "stand","smirk",[], head="11. MEMORIA FALSA")
b("En mil novecientos setenta y cuatro, Elizabeth Loftus enseñó a varias personas el vídeo de un accidente de coche.", "read","focus",[{"k":"phone"}], pant="En 1974, Elizabeth Loftus enseñó a varias personas el vídeo de un accidente de coche.", bg="lab")
b("A unos les preguntó a qué velocidad iban los coches cuando se golpearon. A otros, cuando se estrellaron.", "point","neutral",[], two=dict(x=0.72,pose="think",face="neutral"), x=0.3, bg="lab")
b("Solo con cambiar esa palabra, los del grupo estrellaron calcularon más velocidad.", "shock","shock",[{"k":"arrowup"}], bg="lab")
b("Y una semana después, más gente de ese grupo recordaba cristales rotos. En el vídeo no había ninguno.", "facepalm","dead",[{"k":"cross"}], bg="lab")
b("Años después, Loftus fue más lejos: consiguió que una de cada cuatro personas de su estudio dijera recordar haberse perdido de pequeña en un centro comercial.", "shock","shock",[], big="1 de 4", bigs=110, pant="Años después, Loftus fue más lejos: consiguió que 1 de cada 4 personas de su estudio dijera recordar haberse perdido de pequeña en un centro comercial.")
b("Algo que nunca les había pasado.", "sad","sad",[{"k":"question"}])
b("Tu memoria no es una grabación. Cada vez que recuerdas algo, lo vuelves a construir.", "pointup","focus",[{"k":"brain","float":True}])

# --- EXTRA: POSICION SERIAL
b("Antes de terminar, un extra que casi nadie conoce: el efecto de posición.", "pointup","smirk",[{"k":"exclaim"}], head="EXTRA: EFECTO DE POSICIÓN")
b("En mil novecientos sesenta y dos, Bennet Murdock leía listas de palabras y pedía recordarlas en cualquier orden.", "read","focus",["notes"], pant="En 1962, Bennet Murdock leía listas de palabras y pedía recordarlas en cualquier orden.", bg="lab")
b("La gente recordaba muy bien las primeras palabras, y también las últimas.", "cheer","happy",[{"k":"check"},{"k":"check"}], bg="lab")
b("Las del medio se perdían.", "sad","sad",[{"k":"cross"}], bg="lab")
b("Las primeras, porque les dio tiempo a repasarlas. Las últimas, porque seguían frescas en la memoria a corto plazo.", "point","focus",[{"k":"graph"}], bg="lab")
b("¿Y qué parte de un tema estudias siempre peor? La del medio.", "facepalm","dead",["book"])
b("Así que cambia el orden cada vez que repases. Que la mitad del tema también tenga su turno de ser la primera.", "point","happy",[{"k":"arrowup"}])

# --- CIERRE / CONSEJOS
b("Vale. ¿Y cuál es la que más importa para aprobar?", "think","smirk",[{"k":"question"}], head="¿CUÁL IMPORTA MÁS?")
b("La semántica. Pero solo llega ahí lo que pasa antes por la memoria de trabajo.", "point","focus",[{"k":"brain"},{"k":"book"}])
b("Así que, resumen para estudiar mejor:", "stand","happy",[{"k":"notes"}], pal=3)
b("Uno: quita el móvil de la mesa. Dieciocho segundos de distracción ya son un borrado.", "point","focus",[{"k":"phone"},{"k":"cross"}], big="1", bigs=110, pant="1: quita el móvil de la mesa. 18 segundos de distracción ya son un borrado.")
b("Dos: estudia en bloques pequeños. Tu memoria de trabajo solo carga unas cuatro cosas a la vez.", "write","focus",["notes"], big="2", bigs=110, pant="2: estudia en bloques pequeños. Tu memoria de trabajo solo carga unas 4 cosas a la vez.")
b("Tres: convierte los datos en historias y ejemplos. Lo episódico se pega mejor.", "cheer","happy",[{"k":"heart"}], big="3", bigs=110, pant="3: convierte los datos en historias y ejemplos. Lo episódico se pega mejor.")
b("Cuatro: practica haciendo, no mirando.", "write","focus",[{"k":"pencil"}], big="4", bigs=110, pant="4: practica haciendo, no mirando.")
b("Y cinco: no te fíes de lo seguro que te sientes. Ponte a prueba sin mirar los apuntes.", "pointup","smirk",["exam",{"k":"check"}], big="5", bigs=110, pant="Y 5: no te fíes de lo seguro que te sientes. Ponte a prueba sin mirar los apuntes.")
b("Si te ha servido, aquí tienes todas las técnicas de estudio ordenadas de peor a mejor.", "point","happy",[{"k":"trophy"}])
b("Y si te suscribes, tu memoria prospectiva no tendrá que acordarse de buscarnos.", "cheer","happy",[{"k":"gradeA"}], confetti=True)

g={"titulo":"Todos los tipos de memoria explicados","lang":"es","cfg":0.0,"expresividad":0.5,"frases":F,
"fuentes":[
"Sperling, G. (1960). The information available in brief visual presentations. Psychological Monographs, 74(11). (Informe parcial: la imagen se desvanece en menos de un segundo; informe total ≈ 4 elementos.)",
"Peterson, L. R. y Peterson, M. J. (1959). Short-term retention of individual verbal items. Journal of Experimental Psychology, 58, 193-198. (≈80 % a los 3 s; ≈10 % a los 18 s con repaso bloqueado.)",
"Baddeley, A. D. y Hitch, G. (1974). Working memory. Psychology of Learning and Motivation, 8, 47-89.",
"Miller, G. A. (1956). The magical number seven, plus or minus two. Psychological Review, 63, 81-97. · Cowan, N. (2001). The magical number 4 in short-term memory. Behavioral and Brain Sciences, 24, 87-114.",
"Tulving, E. (1972). Episodic and semantic memory. En Organization of Memory, Academic Press.",
"Milner, B. (1962) y Corkin, S.: aprendizaje del dibujo en espejo del paciente H.M. (Henry Molaison) sin recuerdo consciente de las sesiones.",
"Talarico, J. M. y Rubin, D. C. (2003). Confidence, not consistency, characterizes flashbulb memories. Psychological Science, 14, 455-461.",
"Loftus, E. F. y Palmer, J. C. (1974). Reconstruction of automobile destruction. Journal of Verbal Learning and Verbal Behavior, 13, 585-589.",
"Loftus, E. F. y Pickrell, J. E. (1995). The formation of false memories. Psychiatric Annals, 25, 720-725. (6 de 24 participantes, el 25 %.)",
"Murdock, B. B. (1962). The serial position effect of free recall. Journal of Experimental Psychology, 64, 482-488.",
"Priming de repetición y semántico: Meyer, D. E. y Schvaneveldt, R. W. (1971). Journal of Experimental Psychology, 90, 227-234."]}
json.dump(g,open("guion.json","w"),ensure_ascii=False,indent=1)
w=sum(len(f["t"].split()) for f in F); c=sum(len(f["t"]) for f in F)
print(len(F),"frases",w,"palabras",round(c/15+0.3*len(F)),"s aprox")
