# Guion del Short es-s03 (efecto foco). Ejecuta: python3 gen.py
import json
F=[]
def b(t, v, pant=None):
    f={"t":t,"v":v,"esc":"A"}
    if pant: f["pantalla"]=pant
    F.append(f)
G=0.64
b("Mañana tienes exposición y crees que toda la clase va a fijarse en cada fallo.",
  {"bg":"stage","spot":0.5,"chars":[{"x":0.5,"pose":"shock","face":"shock","hold":"notes"}],"props":[{"k":"eye","x":0.25,"y":0.3,"s":0.7},{"k":"eye","x":0.75,"y":0.26,"s":0.7,"d":0.2}],"ground":G})
b("Spoiler: no.", {"bg":"stage","spot":0.5,"chars":[{"x":0.5,"pose":"shrug","face":"smirk"}],"big":"NO","bigx":0.5,"bigy":0.3,"bigs":200,"bigc":"#3fb06b","ground":G,"wipe":True})
b("En el año dos mil, unos psicólogos de Cornell hicieron una prueba cruel.",
  {"head":"CORNELL, 2000","bg":"lab","chars":[{"x":0.32,"pose":"read","face":"focus","hold":"notes"},{"id":"b","x":0.72,"pose":"think","face":"smirk","flip":True}],"ground":G,"wipe":True},
  pant="En el año 2000, unos psicólogos de Cornell hicieron una prueba cruel.")
b("Le pusieron a un estudiante una camiseta con la cara de Barry Manilow. Nada de moda.",
  {"chars":[{"x":0.3,"pose":"facepalm","face":"sad"}],"props":[{"k":"shirt","x":0.68,"y":0.4,"s":1.3},{"k":"cross","x":0.82,"y":0.26,"s":0.6,"d":0.6}],"ground":G})
b("Y le hicieron entrar en una sala llena de gente.",
  {"bg":"stage","spot":0.5,"chars":[{"x":0.5,"pose":"walk","face":"shock","walk":0.12}],"ground":G})
b("Luego le preguntaron: ¿cuántos se han fijado en tu camiseta?",
  {"bg":"stage","spot":0.5,"chars":[{"x":0.5,"pose":"think","face":"neutral"}],"props":[{"k":"question","x":0.78,"y":0.3,"s":0.8,"float":True}],"ground":G})
b("Él dijo: más o menos la mitad.", {"chars":[{"x":0.3,"pose":"point","face":"sad"}],"big":"50 %","bigx":0.62,"bigy":0.3,"bigs":170,"bigc":"#e8483f","ground":G})
b("En realidad, solo una de cada cuatro personas.", {"chars":[{"x":0.3,"pose":"shock","face":"shock"}],"big":"1 de 4","bigx":0.62,"bigy":0.3,"bigs":150,"bigc":"#3fb06b","props":[{"k":"arrowdown","x":0.8,"y":0.44,"s":0.8,"d":0.4}],"ground":G,"wipe":True},
  pant="En realidad, solo 1 de cada 4 personas.")
b("Es el efecto foco: crees que llevas un foco encima y que todos te miran.",
  {"head":"EFECTO FOCO","bg":"stage","spot":0.5,"chars":[{"x":0.5,"pose":"stand","face":"shock"}],"props":[{"k":"eye","x":0.22,"y":0.3,"s":0.6},{"k":"eye","x":0.78,"y":0.3,"s":0.6,"d":0.2}],"ground":G,"wipe":True})
b("Pero cada uno está pendiente de su propio foco.",
  {"chars":[{"x":0.25,"pose":"read","face":"focus","hold":"phone"},{"id":"b","x":0.72,"pose":"think","face":"sad","flip":True}],"props":[{"k":"zzz","x":0.5,"y":0.28,"s":0.7,"float":True}],"ground":G})
b("Si te trabas en la exposición, casi nadie se acordará mañana.",
  {"bg":"classroom","board":"EXPOSICIÓN","boards":70,"chars":[{"x":0.84,"pose":"shrug","face":"smirk","flip":True}],"props":[{"k":"check","x":0.3,"y":0.5,"s":0.8,"d":0.3}],"ground":G})
b("Respira, sigue, y que el protagonista sea tu tema.",
  {"bg":"stage","spot":0.5,"chars":[{"x":0.5,"pose":"cheer","face":"happy","confetti":True}],"props":[{"k":"gradeA","x":0.8,"y":0.32,"s":0.7,"d":0.4}],"ground":G})
b("En el canal tienes los diez sesgos que te engañan al estudiar.",
  {"chars":[{"x":0.3,"pose":"pointup","face":"happy"}],"props":[{"k":"brain","x":0.7,"y":0.36,"s":0.9,"float":True}],"big":"10","bigx":0.7,"bigy":0.2,"bigs":110,"ground":G},
  pant="En el canal tienes los 10 sesgos que te engañan al estudiar.")
g={"titulo":"Nadie se fijó en tu camiseta: el efecto foco","lang":"es","cfg":0.0,"expresividad":0.5,"frases":F,
 "fuentes":["Gilovich, T., Medvec, V. H. y Savitsky, K. (2000). The spotlight effect in social judgment: An egocentric bias in estimates of the salience of one's own actions and appearance. Journal of Personality and Social Psychology, 78(2), 211-222. (Estudiantes de Cornell con una camiseta de Barry Manilow estimaron que la notaría en torno a la mitad de los observadores; la notó en torno a una cuarta parte, 23-25 % según las fuentes.)"]}
json.dump(g,open("guion.json","w"),ensure_ascii=False,indent=1)
c=sum(len(f["t"]) for f in F); print(len(F),"frases",c,"caracteres ≈",round(c/13),"s")
