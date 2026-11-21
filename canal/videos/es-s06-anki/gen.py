# Guion del Short es-s06: Anki en 50 segundos. Ejecuta: python3 gen.py
import json
F=[]
def b(t, v, pant=None, tono=None):
    f={"t":t,"v":v,"esc":"A"}
    if pant: f["pantalla"]=pant
    if tono: f["tono"]=tono
    F.append(f)
G=0.64
b("Hay una aplicación gratis que te pregunta cada cosa justo antes de que se te olvide.",
  {"chars":[{"x":0.3,"pose":"shock","face":"shock"}],"props":[{"k":"phone","x":0.7,"y":0.4,"s":1.1,"anim":True},{"k":"brain","x":0.84,"y":0.24,"s":0.5,"float":True,"d":0.3}],"ground":G}, tono="gancho, intriga")
b("Se llama Anki. Y así se usa en cincuenta segundos.",
  {"head":"ANKI","chars":[{"x":0.3,"pose":"point","face":"happy"}],"props":[{"k":"card","x":0.7,"y":0.4,"s":1.1}],"big":"50 s","bigx":0.68,"bigy":0.3,"bigs":100,"ground":G,"wipe":True},
  pant="Se llama Anki. Y así se usa en 50 segundos.")
b("Es gratis en ordenador, Android y web. En iPhone es de pago.",
  {"chars":[{"x":0.3,"pose":"shrug","face":"neutral"}],"props":[{"k":"phone","x":0.66,"y":0.42,"s":0.9},{"k":"check","x":0.82,"y":0.28,"s":0.6,"d":0.3}],"ground":G}, tono="informativo")
b("Crea un mazo por asignatura. Por ejemplo, Biología.",
  {"chars":[{"x":0.3,"pose":"write","face":"focus"}],"props":[{"k":"book","x":0.7,"y":0.42,"s":1.0}],"big":"1","bigx":0.7,"bigy":0.2,"bigs":100,"ground":G})
b("Añade tarjetas: delante una pregunta, detrás la respuesta. Una idea por tarjeta.",
  {"chars":[{"x":0.3,"pose":"write","face":"happy"}],"props":[{"k":"card","x":0.66,"y":0.42,"s":1.0},{"k":"question","x":0.84,"y":0.28,"s":0.6,"d":0.3}],"big":"2","bigx":0.7,"bigy":0.2,"bigs":100,"ground":G})
b("Cada día, pulsa Estudiar e intenta responder antes de girar la tarjeta.",
  {"bg":"library","chars":[{"x":0.3,"pose":"think","face":"focus"}],"props":[{"k":"card","x":0.7,"y":0.42,"s":1.0}],"big":"3","bigx":0.7,"bigy":0.2,"bigs":100,"ground":G})
b("Luego, sé sincero y dile si te ha costado: desde otra vez, hasta fácil.",
  {"chars":[{"x":0.3,"pose":"point","face":"smirk"}],"props":[{"k":"scale","x":0.7,"y":0.42,"s":0.9,"anim":"left"}],"ground":G},
  pant="Luego, sé sincero y dile si te ha costado: desde «otra vez» hasta «fácil».")
b("Si la fallas, vuelve pronto. Si la sabes, tarda días en volver.",
  {"chars":[{"x":0.3,"pose":"read","face":"focus"}],"props":[{"k":"calendar","x":0.7,"y":0.42,"s":1.0},{"k":"arrowup","x":0.84,"y":0.28,"s":0.6,"d":0.3}],"ground":G})
b("Eso es repetición espaciada, de lo que mejor funciona para memorizar.",
  {"head":"REPETICIÓN ESPACIADA","bg":"lab","chars":[{"x":0.3,"pose":"cheer","face":"happy"}],"props":[{"k":"graph","x":0.7,"y":0.42,"s":1.0},{"k":"check","x":0.84,"y":0.26,"s":0.6,"d":0.3}],"ground":G,"wipe":True})
b("Truco: escribe tú las tarjetas y haz las del día, aunque sean diez.",
  {"chars":[{"x":0.3,"pose":"pointup","face":"happy"}],"props":[{"k":"pencil","x":0.7,"y":0.42,"s":0.9}],"big":"TRUCO","bigx":0.68,"bigy":0.2,"bigs":90,"ground":G},
  pant="Truco: escribe tú las tarjetas y haz las del día, aunque sean 10.")
b("Nadie nos paga por decirlo. Es gratis y funciona.",
  {"chars":[{"x":0.5,"pose":"shrug","face":"smirk"}],"props":[{"k":"heart","x":0.8,"y":0.3,"s":0.7}],"ground":G}, tono="remate, sonriendo")
g={"titulo":"Anki en 50 segundos: la app que te pregunta antes de que olvides","lang":"es","frases":F,"fuentes":[
"Anki: escritorio (Windows, macOS, Linux), AnkiDroid (Android) y AnkiWeb gratis; AnkiMobile (iPhone) de pago único, 24,99 $ en EE. UU. (apps.ankiweb.net y docs.ankiweb.net, consultado el 21/11/2026).",
"Repetición espaciada: Cepeda, N. J. y otros (2008). Spacing effects in learning. Psychological Science, 19(11), 1095-1102; Dunlosky, J. y otros (2013). Psychological Science in the Public Interest, 14(1), 4-58 (práctica espaciada y autoevaluación: utilidad alta)."]}
json.dump(g,open("guion.json","w"),ensure_ascii=False,indent=1)
w=sum(len(f["t"].split()) for f in F); print(len(F),"frases",w,"palabras ≈",round(w/2.5),"s")
