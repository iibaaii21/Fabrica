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

BOARD=dict(x=0.84, flip=True)

# --- INTRO
b("Hay cosas sobre el cerebro que te enseñaron en clase, y son mentira.", "shock","shock",[{"k":"brain","float":True}], big="!", bigc="#e8483f")
b("Y no te las contó cualquiera: muchas se las creen hasta los profesores.", "point","smirk",[{"k":"book"}], bg="classroom")
b("Hoy vamos a ver diez mitos del cerebro, ordenados de menos a más dañinos para tus estudios.", "point","happy",[{"k":"brain"},{"k":"arrowup"}], pant="Hoy vamos a ver 10 mitos del cerebro, ordenados de menos a más dañinos para tus estudios.")
b("Cada uno con el experimento que lo desmonta.", "read","focus",[{"k":"flask","anim":True}], bg="lab")
b("Y el número uno seguramente te lo hicieron hacer en el colegio, con un test y todo.", "pointup","smirk",[{"k":"exam"}], big="#1", bigc="#f6c23e")
b("Vamos allá.", "walk","happy",[], walk=0.05, pal=1)

# --- 10 PEZ
b("Número diez: los peces de colores solo recuerdan tres segundos.", "stand","neutral",[{"k":"fish","anim":True}], head="10. EL PEZ DE COLORES", bg="lab")
b("Es el insulto favorito cuando alguien olvida algo: tienes memoria de pez.", "shrug","smirk",[{"k":"fish","anim":True},{"k":"question","float":True}])
b("Pero en experimentos, a peces de colores se les ha enseñado a empujar una palanca para conseguir comida.", "read","focus",[{"k":"fish","anim":True},{"k":"check"}], bg="lab")
b("E incluso a usarla solo a la hora del día en que funcionaba.", "think","focus",[{"k":"clock"},{"k":"fish","anim":True}], bg="lab")
b("El biólogo Culum Brown, que estudia la mente de los peces, explica que recuerdan lo aprendido durante meses.", "point","happy",[{"k":"calendar"}], big="meses", bigs=120, bigc="#3fb06b")
b("Así que si olvidas a qué venías, no tienes memoria de pez. El pez te gana.", "facepalm","sad",[{"k":"fish","anim":True}])

# --- 9 AZÚCAR
b("Número nueve: el azúcar te pone hiperactivo.", "cheer","happy",[{"k":"candy","anim":True}], head="9. EL AZÚCAR")
b("Cumpleaños, tarta, y alguien dice: normal que estén así, es el azúcar.", "shock","happy",[{"k":"candy","anim":True},{"k":"exclaim"}], two=dict(x=0.62,pose="cheer",face="happy"))
b("En mil novecientos noventa y cinco, un análisis juntó dieciséis estudios en los que los niños tomaban azúcar o un sustituto sin saber cuál.", "read","focus",["notes"], bg="lab", big="16", bigs=110, pant="En 1995, un análisis juntó 16 estudios en los que los niños tomaban azúcar o un sustituto sin saber cuál.")
b("Resultado: el azúcar no cambiaba ni su comportamiento ni su rendimiento.", "shrug","smirk",[{"k":"cross"}], bg="lab")
b("Y lo mejor: en otro experimento, todos los niños tomaron un placebo, pero a la mitad de las madres les dijeron que era azúcar.", "think","focus",[{"k":"candy"},{"k":"question","float":True}], bg="lab")
b("Esas madres vieron a sus hijos mucho más movidos. El efecto estaba en quien miraba.", "shock","shock",[{"k":"eye"}], big="👀", bigs=120)
b("Al estudiar: un dulce no te arruina la tarde, pero tampoco te da superpoderes.", "write","focus",[{"k":"candy"},{"k":"notes"}])

# --- 8 10 %
b("Número ocho: solo usamos el diez por ciento del cerebro.", "think","focus",[{"k":"brain","float":True}], head="8. EL 10 %", big="10 %", bigc="#e8483f", pant="Número ocho: solo usamos el 10 % del cerebro.")
b("Es la base de media película: si desbloqueas el resto, te vuelves un genio.", "cheer","happy",[{"k":"bulb","anim":True}], bg="stage", spot=0.32)
b("Pero en los escáneres cerebrales nunca se ha encontrado una zona que esté siempre apagada.", "read","focus",[{"k":"brain"},{"k":"graph"}], bg="lab")
b("No todo trabaja a la vez, igual que no usas todos los músculos a la vez. Pero cada parte tiene su función.", "point","happy",[{"k":"brain"},{"k":"check"}])
b("Además, el cerebro pesa más o menos el dos por ciento de tu cuerpo, y gasta alrededor del veinte por ciento de tu energía en reposo.", "shock","shock",[{"k":"battery"}], big="2 % → 20 %", bigs=100, pant="Además, el cerebro pesa más o menos el 2 % de tu cuerpo, y gasta alrededor del 20 % de tu energía en reposo.")
b("La evolución no mantiene un órgano tan caro para usar solo un trocito.", "shrug","smirk",[{"k":"brain"}])
b("Al estudiar: no hay un noventa por ciento escondido. Lo que hay es práctica.", "write","focus",["notes",{"k":"pencil"}], pant="Al estudiar: no hay un 90 % escondido. Lo que hay es práctica.")

# --- 7 IZQUIERDO / DERECHO
b("Número siete: hay gente de cerebro izquierdo y gente de cerebro derecho.", "stand","neutral",[{"k":"brain"}], head="7. IZQUIERDO O DERECHO", pal=2)
b("Los de izquierdo serían lógicos y de números; los de derecho, creativos y de arte.", "point","happy",[{"k":"scale","anim":"left"}], two=dict(x=0.62,pose="cheer",face="happy"))
b("Es verdad que algunas funciones están más en un lado. El lenguaje, por ejemplo, suele estar más a la izquierda.", "think","focus",[{"k":"book"}], bg="lab")
b("Pero en dos mil trece, en la Universidad de Utah, analizaron escáneres de más de mil personas.", "read","focus",["notes"], bg="lab", big="1.011", bigs=110, pant="Pero en 2013, en la Universidad de Utah, analizaron escáneres de más de 1.000 personas.")
b("Y no encontraron personas con un hemisferio entero dominante. Usamos los dos.", "shrug","smirk",[{"k":"scale"},{"k":"check"}], bg="lab")
b("Al estudiar: que te digan que eres de letras no significa que tu cerebro no sirva para mates.", "point","happy",[{"k":"exam"},{"k":"arrowup"}])

# --- 6 MEMORIA FOTOGRÁFICA
b("Número seis: la memoria fotográfica.", "stand","neutral",[{"k":"eye"}], head="6. MEMORIA FOTOGRÁFICA")
b("Ese compañero que mira el libro una vez y lo recuerda como una foto.", "read","happy",[{"k":"book"}], two=dict(x=0.62,pose="shock",face="shock"))
b("Pues nunca se ha demostrado que exista en adultos de verdad.", "shrug","smirk",[{"k":"cross"}], bg="lab")
b("Lo más parecido es la imagen eidética: algunos niños mantienen una imagen unos segundos después de verla.", "think","focus",[{"k":"eye"},{"k":"clock"}], bg="lab")
b("Según los estudios, pasa en torno al dos o al diez por ciento de los niños, y casi desaparece en adultos.", "point","happy",[{"k":"graph"}], big="2-10 %", bigs=110, pant="Según los estudios, pasa en torno al 2 o al 10 % de los niños, y casi desaparece en adultos.")
b("Los campeones de memoria no tienen fotos en la cabeza: usan técnicas, como colocar cada dato en un lugar imaginario.", "cheer","happy",[{"k":"trophy"}])
b("Al estudiar: tu compañero no es un escáner. Seguramente repasa más de lo que dice.", "shrug","smirk",[{"k":"notes"}])

# --- 5 APRENDER DURMIENDO
b("Número cinco: puedes aprender escuchando audios mientras duermes.", "stand","neutral",[{"k":"headphones","anim":True},{"k":"zzz","float":True}], head="5. APRENDER DURMIENDO", bg="bedroom")
b("Lo vendían con cintas para aprender idiomas durmiendo.", "point","happy",[{"k":"cd","anim":True}], bg="bedroom")
b("En mil novecientos cincuenta y seis, Charles Simon y William Emmons lo probaron midiendo la actividad cerebral.", "read","focus",["notes"], bg="lab", pant="En 1956, Charles Simon y William Emmons lo probaron midiendo la actividad cerebral.")
b("Leían palabras a gente dormida. Cuando estaban dormidos de verdad, al despertar no recordaban nada.", "shock","shock",[{"k":"bed"},{"k":"cross"}], bg="bedroom")
b("Solo recordaban algo si estaban medio despiertos.", "think","focus",[{"k":"alarm","anim":True}], bg="bedroom")
b("Lo que sí hace el sueño es fijar lo que estudiaste despierto.", "point","happy",[{"k":"pillow"},{"k":"check"}], bg="bedroom")
b("Al estudiar: el audio de noche, fuera. Estudia de día y duerme bien.", "write","focus",[{"k":"moon"},{"k":"notes"}])

# --- 4 ENTRENAMIENTO CEREBRAL
b("Número cuatro: los juegos de entrenamiento cerebral te hacen más listo.", "stand","neutral",[{"k":"gamepad"},{"k":"brain"}], head="4. JUEGOS DE CEREBRO", pal=4)
b("Unos minutos al día de puzles en el móvil y tu cerebro sube de nivel. O eso dicen los anuncios.", "cheer","happy",[{"k":"phone"},{"k":"arrowup"}])
b("En dos mil diez, la revista Nature publicó un experimento con un programa de la BBC.", "read","focus",["notes"], bg="lab", pant="En 2010, la revista Nature publicó un experimento con un programa de la BBC.")
b("Más de once mil personas entrenaron durante seis semanas.", "point","happy",[{"k":"calendar"}], big="11.430", bigs=110, pant="Más de 11.000 personas entrenaron durante 6 semanas.")
b("Mejoraron en los juegos que practicaban. Pero en las pruebas distintas, no mejoraron más que un grupo que solo buscaba respuestas en internet.", "shrug","smirk",[{"k":"gamepad"},{"k":"cross"}], bg="lab")
b("Es decir: te haces bueno en el juego, no en todo lo demás.", "facepalm","sad",[{"k":"trophy"}])
b("Al estudiar: si quieres mejorar en física, practica física.", "write","focus",[{"k":"exam"},{"k":"check"}])

# --- 3 MULTITAREA
b("Número tres: se te da bien hacer varias cosas a la vez.", "stand","neutral",[{"k":"phone"},{"k":"book"}], head="3. MULTITAREA")
b("Apuntes, móvil, una serie de fondo y el grupo de clase sonando.", "read","shock",[{"k":"phone","anim":True},{"k":"notes"},{"k":"exclaim"}])
b("En dos mil nueve, en Stanford, compararon a gente que hace mucha multitarea con gente que hace poca.", "read","focus",["notes"], bg="lab", pant="En 2009, en Stanford, compararon a gente que hace mucha multitarea con gente que hace poca.")
b("Los multitarea lo hacían peor al cambiar de tarea y les costaba más ignorar lo que no importaba.", "shock","shock",[{"k":"cross"},{"k":"arrowdown"}], bg="lab")
b("Ojo: es una comparación, no prueba que la multitarea sea la causa. Pero no hay ninguna pista de que te haga mejor.", "think","focus",[{"k":"scale"}], bg="lab")
b("Tu cerebro no hace dos cosas a la vez: salta de una a otra, y en cada salto pierdes algo.", "point","happy",[{"k":"brain"},{"k":"arrowdown"}])
b("Al estudiar: el móvil en otra habitación, no boca abajo en la mesa.", "write","focus",[{"k":"phone"},{"k":"cross"}])

# --- 2 MÚSICA CON LETRA
b("Número dos: estudiar con tu música favorita te ayuda a concentrarte.", "stand","happy",[{"k":"headphones","anim":True}], head="2. MÚSICA CON LETRA", bg="hall")
b("Y si es Mozart, mejor todavía. O eso dicen.", "point","smirk",[{"k":"piano","anim":True}], bg="hall")
b("Lo del efecto Mozart ya lo desmontamos en un Short: el efecto era pequeño, duraba minutos y no se repite.", "shrug","smirk",[{"k":"cd","anim":True},{"k":"cross"}])
b("Pero hay algo más importante: la letra.", "think","focus",[{"k":"note","anim":True}], bg="hall")
b("En dos mil catorce, unos estudiantes leyeron textos con música con letra, música sin letra o en silencio.", "read","focus",["notes"], bg="library", pant="En 2014, unos estudiantes leyeron textos con música con letra, música sin letra o en silencio.")
b("Con letra entendieron peor. Y daba igual que la canción les gustara o no.", "shock","shock",[{"k":"cross"},{"k":"note"}], bg="library")
b("Tu cerebro procesa las palabras de la canción aunque no quieras, y compiten con las del libro.", "point","happy",[{"k":"brain"},{"k":"book"}])
b("Al estudiar: silencio o música sin letra. La lista con letra, para el descanso.", "write","focus",[{"k":"headphones"},{"k":"check"}])

# --- 1 ESTILOS DE APRENDIZAJE
b("Número uno: los estilos de aprendizaje.", "stand","neutral",[{"k":"exam"}], head="1. ESTILOS DE APRENDIZAJE", pal=2)
b("Visual, auditivo o kinestésico. Haces un test, te dicen cuál eres, y te enseñan según tu estilo.", "point","happy",[{"k":"eye"},{"k":"headphones"},{"k":"pencil"}])
b("En una encuesta de dos mil doce, más de nueve de cada diez profesores británicos creían que funciona.", "read","focus",[{"k":"book","x":0.82,"y":0.5}], big="93 %", bigs=120, bigc="#e8483f", pant="En una encuesta de 2012, más de 9 de cada 10 profesores británicos creían que funciona.")
b("Pero en dos mil ocho, cuatro psicólogos revisaron todas las pruebas.", "read","focus",["notes"], bg="lab", pant="Pero en 2008, cuatro psicólogos revisaron todas las pruebas.")
b("Para demostrarlo, haría falta ver que los visuales aprenden mejor con imágenes y los auditivos con audio.", "think","focus",[{"k":"scale","anim":"left"}], bg="lab")
b("Y no encontraron casi ningún estudio bien hecho que lo mostrara. Algunos mostraban justo lo contrario.", "shock","shock",[{"k":"cross"}], bg="lab")
b("Que prefieras algo no significa que aprendas mejor así.", "shrug","smirk",[{"k":"heart"},{"k":"question"}])
b("Lo que funciona es usar el formato que encaja con el contenido: un mapa se aprende viéndolo, un idioma, escuchándolo.", "point","happy",[{"k":"eye"},{"k":"headphones"}])
b("Al estudiar: no te encierres en un estilo. Mezcla dibujos, palabras y ponerte a prueba.", "write","focus",["exam",{"k":"check"}])

# --- EXTRA
b("Extra: ¿por qué nos creemos todo esto?", "think","focus",[{"k":"question","float":True}], head="EXTRA: POR QUÉ NOS LOS CREEMOS")
b("En esa misma encuesta de dos mil doce, los profesores se creían de media casi la mitad de los mitos.", "read","focus",[{"k":"book","x":0.82,"y":0.5}], big="49 %", bigs=120, pant="En esa misma encuesta de 2012, los profesores se creían de media casi la mitad de los mitos.")
b("Y lo curioso: saber más sobre el cerebro en general no les protegía.", "shock","shock",[{"k":"brain"},{"k":"cross"}], bg="classroom")
b("Los mitos que más se creían eran los que venían con productos para colegios.", "point","smirk",[{"k":"ticket"}])
b("Un mito sencillo, que suena a ciencia y que alguien vende, se pega mucho mejor que un estudio aburrido.", "shrug","smirk",[{"k":"bulb","anim":True}])
b("Truco: cuando oigas una frase sobre el cerebro, pregunta: ¿qué experimento lo demostró?", "pointup","happy",[{"k":"flask","anim":True},{"k":"question"}], bg="lab")

# --- RESUMEN
b("Resumen para tus estudios:", "stand","happy",[{"k":"notes"}], head="RESUMEN", pal=3)
b("Uno: no te encierres en un estilo, mezcla formatos y ponte a prueba.", "write","focus",["exam",{"k":"check","x":0.84,"y":0.5}], big="1", bigs=110)
b("Dos: silencio o música sin letra.", "read","focus",[{"k":"headphones","x":0.84,"y":0.5}], big="2", bigs=110)
b("Tres: el móvil, fuera de la habitación.", "point","happy",[{"k":"phone","x":0.84,"y":0.5}], big="3", bigs=110)
b("Cuatro: practica lo que vas a examinar, no juegos.", "write","focus",[{"k":"exam","x":0.84,"y":0.5}], big="4", bigs=110)
b("Y cinco: estudia de día y duerme de noche.", "shrug","happy",[{"k":"moon","x":0.84,"y":0.5}], big="5", bigs=110)
b("Si te ha gustado, aquí tienes los diez sesgos que te engañan al estudiar.", "point","happy",[{"k":"brain"}], pant="Si te ha gustado, aquí tienes los 10 sesgos que te engañan al estudiar.")
b("Y suscríbete. Eso sí que usa el cien por cien de tu dedo.", "cheer","happy",[{"k":"gradeA"}], confetti=True, pant="Y suscríbete. Eso sí que usa el 100 % de tu dedo.")

g={"titulo":"10 mitos del cerebro que te creíste en clase","lang":"es","cfg":0.0,"expresividad":0.5,"frases":F,"fuentes":[
"Peces de colores: experimento de la Universidad de Plymouth (1994) con una palanca que daba comida a una hora concreta; Culum Brown (Universidad Macquarie) sobre memoria de peces de al menos tres meses.",
"Wolraich, M. L., Wilson, D. B. y White, J. W. (1995). The effect of sugar on behavior or cognition in children: a meta-analysis. JAMA, 274(20), 1617-1621. (16 estudios publicados; no descarta efectos pequeños en subgrupos.)",
"Hoover, D. W. y Milich, R. (1994). Effects of sugar ingestion expectancies on mother-child interactions. Journal of Abnormal Child Psychology, 22. (35 niños de 5-7 años; todos tomaron placebo.)",
"Mito del 10 %: Scientific American y Britannica, «Do we really use only 10 percent of our brains?»; ninguna región del cerebro aparece siempre inactiva en neuroimagen. Cerebro: ~2 % del peso corporal y ~20 % del metabolismo en reposo (Kety 1957; Sokoloff 1960; Attwell y Laughlin 2001).",
"Nielsen, J. A., Zielinski, B. A., Ferguson, M. A., Lainhart, J. E. y Anderson, J. S. (2013). An evaluation of the left-brain vs. right-brain hypothesis with resting state functional connectivity MRI. PLoS ONE, 8(8), e71275. (1.011 personas de 7 a 29 años.)",
"Haber, R. N. (1979). Twenty years of haunting eidetic imagery: where's the ghost? Behavioral and Brain Sciences, 2, 583-629. (Imagen eidética en ~2-10 % de los niños, casi nula en adultos.)",
"Simon, C. W. y Emmons, W. H. (1956). The non-recall of material presented during sleep. American Journal of Psychology, 69(1), 76-81.",
"Owen, A. M. y otros (2010). Putting brain training to the test. Nature, 465, 775-778. (11.430 participantes, 6 semanas.)",
"Ophir, E., Nass, C. y Wagner, A. D. (2009). Cognitive control in media multitaskers. PNAS, 106(37), 15583-15587.",
"Perham, N. y Currie, H. (2014). Does listening to preferred music improve reading comprehension performance? Applied Cognitive Psychology, 28, 279-284.",
"Pietschnig, J., Voracek, M. y Formann, A. K. (2010). Mozart effect–Shmozart effect: A meta-analysis. Intelligence, 38, 314-323.",
"Pashler, H., McDaniel, M., Rohrer, D. y Bjork, R. (2008). Learning styles: Concepts and evidence. Psychological Science in the Public Interest, 9(3), 105-119.",
"Dekker, S., Lee, N. C., Howard-Jones, P. y Jolles, J. (2012). Neuromyths in education: Prevalence and predictors of misconceptions among teachers. Frontiers in Psychology, 3, 429. (242 profesores de Reino Unido y Países Bajos; de media creían el 49 % de los mitos; 93 % de los británicos aceptó el de los estilos de aprendizaje.)"]}
json.dump(g,open("guion.json","w"),ensure_ascii=False,indent=1)
w=sum(len(f["t"].split()) for f in F); c=sum(len(f["t"]) for f in F)
print(len(F),"frases",w,"palabras",round(c/13),"s aprox")
