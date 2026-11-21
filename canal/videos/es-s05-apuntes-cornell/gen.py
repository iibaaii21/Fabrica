# Guion del Short es-s05: apuntes con el método Cornell. Ejecuta: python3 gen.py
import json
F=[]
def b(t, v, pant=None, tono=None):
    f={"t":t,"v":v,"esc":"A"}
    if pant: f["pantalla"]=pant
    if tono: f["tono"]=tono
    F.append(f)
G=0.64
b("Tus apuntes de clase no sirven para estudiar. Arréglalo con una hoja.",
  {"bg":"classroom","board":"APUNTES","boards":70,"chars":[{"x":0.84,"pose":"facepalm","face":"sad","flip":True}],"ground":G}, tono="gancho, directo")
b("Es el método Cornell, de Walter Pauk, profesor de la Universidad de Cornell.",
  {"head":"MÉTODO CORNELL","chars":[{"x":0.3,"pose":"point","face":"happy"}],"props":[{"k":"notes","x":0.7,"y":0.4,"s":1.1}],"ground":G,"wipe":True})
b("Divide la hoja: columna estrecha a la izquierda, ancha a la derecha y una franja abajo.",
  {"chars":[{"x":0.26,"pose":"write","face":"focus"}],"props":[{"k":"notes","x":0.68,"y":0.4,"s":1.3},{"k":"pencil","x":0.86,"y":0.3,"s":0.6,"d":0.3}],"big":"✂","bigx":0.68,"bigy":0.2,"bigs":90,"ground":G})
b("En clase, escribe solo en la derecha: ideas clave, con tus palabras.",
  {"bg":"classroom","board":"IDEAS CLAVE","boards":56,"chars":[{"x":0.84,"pose":"write","face":"focus","flip":True}],"ground":G})
b("Ese mismo día, a la izquierda, escribe preguntas sobre lo apuntado.",
  {"chars":[{"x":0.3,"pose":"think","face":"focus"}],"props":[{"k":"question","x":0.7,"y":0.34,"s":0.9,"float":True},{"k":"notes","x":0.82,"y":0.48,"s":0.7,"d":0.2}],"ground":G})
b("Y abajo, un resumen de una o dos frases.",
  {"chars":[{"x":0.3,"pose":"write","face":"happy"}],"props":[{"k":"notes","x":0.7,"y":0.42,"s":1.0},{"k":"check","x":0.84,"y":0.28,"s":0.6,"d":0.3}],"big":"1-2","bigx":0.68,"bigy":0.2,"bigs":100,"ground":G},
  pant="Y abajo, un resumen de 1 o 2 frases.")
b("Para estudiar, tapa la derecha y responde en voz alta las preguntas.",
  {"head":"CÓMO SE ESTUDIA","bg":"library","chars":[{"x":0.3,"pose":"point","face":"focus"}],"props":[{"k":"notes","x":0.7,"y":0.42,"s":1.0},{"k":"eye","x":0.82,"y":0.26,"s":0.5,"d":0.3}],"ground":G,"wipe":True})
b("Siendo sinceros: casi todo lo que hay a favor son experiencias, no grandes estudios.",
  {"chars":[{"x":0.3,"pose":"shrug","face":"neutral"}],"props":[{"k":"scale","x":0.7,"y":0.4,"s":0.9}],"ground":G}, tono="honesto, más bajo")
b("Pero te obliga a hacer lo que sí está probado: ponerte a prueba en vez de releer.",
  {"bg":"lab","chars":[{"x":0.3,"pose":"cheer","face":"happy"}],"props":[{"k":"exam","x":0.7,"y":0.42,"s":0.9},{"k":"check","x":0.84,"y":0.28,"s":0.7,"d":0.3}],"ground":G})
b("Pruébalo en la próxima clase. Y en el canal, cómo preparar un examen en siete días.",
  {"chars":[{"x":0.3,"pose":"pointup","face":"happy"}],"props":[{"k":"calendar","x":0.7,"y":0.4,"s":1.0}],"big":"7 DÍAS","bigx":0.68,"bigy":0.2,"bigs":90,"ground":G},
  pant="Pruébalo en la próxima clase. Y en el canal, cómo preparar un examen en 7 días.")
g={"titulo":"Cómo tomar apuntes en clase: el método Cornell","lang":"es","frases":F,"fuentes":[
"Método Cornell: creado por Walter Pauk (Universidad de Cornell) en los años cincuenta y difundido en su libro «How to Study in College». Columna de pistas a la izquierda, notas a la derecha y resumen abajo (guías de la Universidad de Cincinnati, Wisconsin-Eau Claire y Grand Valley State).",
"Sobre la evidencia: la mayoría de las pruebas a favor del método Cornell son anecdóticas (guía de la Universidad de Cornell / Wikipedia). La autoevaluación sí tiene respaldo fuerte: Roediger y Karpicke (2006); Dunlosky y otros (2013)."]}
json.dump(g,open("guion.json","w"),ensure_ascii=False,indent=1)
w=sum(len(f["t"].split()) for f in F); print(len(F),"frases",w,"palabras ≈",round(w/2.5),"s")
