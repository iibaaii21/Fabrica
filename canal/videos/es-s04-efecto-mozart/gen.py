# Guion del Short es-s04 (efecto Mozart). Ejecuta: python3 gen.py
import json
F=[]
def b(t, v, pant=None):
    f={"t":t,"v":v,"esc":"A"}
    if pant: f["pantalla"]=pant
    F.append(f)
G=0.64
b("¿Estudiar escuchando a Mozart te hace más listo?",
  {"bg":"hall","chars":[{"x":0.32,"pose":"think","face":"smirk"}],"props":[{"k":"headphones","x":0.7,"y":0.34,"s":0.9,"anim":True},{"k":"question","x":0.82,"y":0.18,"s":0.6,"float":True,"d":0.3}],"ground":G})
b("Hasta un gobernador se lo creyó.", {"chars":[{"x":0.5,"pose":"shrug","face":"smirk"}],"big":"🤔","bigx":0.5,"bigy":0.28,"bigs":150,"ground":G,"wipe":True})
b("En mil novecientos noventa y tres, la revista Nature publicó un experimento.",
  {"head":"NATURE, 1993","bg":"lab","chars":[{"x":0.3,"pose":"read","face":"focus","hold":"notes"}],"props":[{"k":"flask","x":0.75,"y":0.42,"s":0.9,"anim":True}],"ground":G,"wipe":True},
  pant="En 1993, la revista Nature publicó un experimento.")
b("Estudiantes que oían diez minutos de Mozart antes de un test de razonamiento espacial.",
  {"bg":"hall","chars":[{"x":0.28,"pose":"stand","face":"happy"}],"props":[{"k":"piano","x":0.68,"y":0.46,"s":0.9,"anim":True},{"k":"clock","x":0.7,"y":0.22,"s":0.6,"d":0.3}],"ground":G},
  pant="Estudiantes que oían 10 minutos de Mozart antes de un test de razonamiento espacial.")
b("Y sacaron mejor nota que en silencio.", {"chars":[{"x":0.3,"pose":"cheer","face":"happy"}],"props":[{"k":"arrowup","x":0.72,"y":0.4,"s":0.9,"d":0.2},{"k":"exam","x":0.62,"y":0.5,"s":0.7}],"ground":G})
b("Pero el efecto duraba unos quince minutos.", {"chars":[{"x":0.3,"pose":"facepalm","face":"sad"}],"big":"15 min","bigx":0.64,"bigy":0.3,"bigs":140,"bigc":"#e8483f","ground":G,"wipe":True},
  pant="Pero el efecto duraba unos 15 minutos.")
b("Daba igual: la prensa lo vendió como «Mozart te hace más listo».",
  {"chars":[{"x":0.3,"pose":"shock","face":"shock"}],"props":[{"k":"cd","x":0.7,"y":0.36,"s":1.0,"anim":True},{"k":"brain","x":0.84,"y":0.22,"s":0.5,"float":True,"d":0.3}],"ground":G})
b("En mil novecientos noventa y ocho, el gobernador de Georgia pidió dinero para regalar música clásica a cada bebé.",
  {"head":"GEORGIA, 1998","chars":[{"x":0.26,"pose":"point","face":"happy"}],"props":[{"k":"baby","x":0.62,"y":0.44,"s":0.9},{"k":"cd","x":0.82,"y":0.32,"s":0.7,"anim":True,"d":0.4}],"ground":G,"wipe":True},
  pant="En 1998, el gobernador de Georgia pidió dinero para regalar música clásica a cada bebé.")
b("En dos mil diez se juntaron casi cuarenta estudios con más de tres mil personas.",
  {"head":"2010","bg":"library","chars":[{"x":0.3,"pose":"read","face":"focus","hold":"book"}],"props":[{"k":"graph","x":0.72,"y":0.4,"s":0.9,"d":0.2}],"big":"+3.000","bigx":0.7,"bigy":0.18,"bigs":100,"ground":G,"wipe":True},
  pant="En 2010 se juntaron casi 40 estudios con más de 3.000 personas.")
b("Conclusión: lo que ayudaba era estar más despierto y animado, no Mozart.",
  {"chars":[{"x":0.32,"pose":"stand","face":"happy"}],"props":[{"k":"coffee","x":0.7,"y":0.42,"s":0.8},{"k":"heart","x":0.82,"y":0.26,"s":0.6,"d":0.3},{"k":"cross","x":0.56,"y":0.24,"s":0.5,"d":0.6}],"ground":G})
b("Para estudiar, mejor sin letra o en silencio.",
  {"bg":"library","chars":[{"x":0.3,"pose":"read","face":"focus","hold":"book"}],"props":[{"k":"note","x":0.72,"y":0.36,"s":0.9,"anim":True},{"k":"check","x":0.84,"y":0.24,"s":0.6,"d":0.3}],"ground":G})
b("En el canal: diez mitos del cerebro que te creíste.",
  {"chars":[{"x":0.3,"pose":"pointup","face":"happy"}],"props":[{"k":"brain","x":0.7,"y":0.36,"s":0.9,"float":True}],"big":"10","bigx":0.7,"bigy":0.2,"bigs":110,"ground":G},
  pant="En el canal: 10 mitos del cerebro que te creíste.")
g={"titulo":"¿Mozart te hace más listo? El efecto Mozart","lang":"es","cfg":0.0,"expresividad":0.5,"frases":F,
 "fuentes":["Rauscher, F. H., Shaw, G. L. y Ky, K. N. (1993). Music and spatial task performance. Nature, 365, 611. (Estudiantes universitarios; 10 minutos de la Sonata para dos pianos en re mayor K. 448 antes de tareas de razonamiento espacial del Stanford-Binet, frente a silencio y a una cinta de relajación; efecto de unos 10-15 minutos.)",
  "Enero de 1998: el gobernador de Georgia, Zell Miller, pidió al parlamento estatal 105.000 dólares para dar una cinta o CD de música clásica a cada recién nacido (NPR, 13/01/1998; Deseret News, 14/01/1998).",
  "Pietschnig, J., Voracek, M. y Formann, A. K. (2010). Mozart effect–Shmozart effect: A meta-analysis. Intelligence, 38, 314-323. (Unos 40 estudios, más de 3.000 participantes: sin mejora cognitiva específica por escuchar a Mozart.)",
  "Thompson, W. F., Schellenberg, E. G. y Husain, G. (2001). Arousal, mood, and the Mozart effect. Psychological Science, 12, 248-251. (El efecto se explica por activación y estado de ánimo.)",
  "Perham, N. y Currie, H. (2014). Does listening to preferred music improve reading comprehension performance? Applied Cognitive Psychology, 28, 279-284. (Peor comprensión con música con letra que con instrumental o en silencio.)"]}
json.dump(g,open("guion.json","w"),ensure_ascii=False,indent=1)
c=sum(len(f["t"]) for f in F); print(len(F),"frases",c,"caracteres ≈",round(c/13),"s")
