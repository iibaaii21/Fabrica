import json
F=[]
G=0.6
def b(t,**v): v.setdefault('ground',G); F.append({'t':t,'v':v,'esc':'A'})
C=lambda pose,face='neutral',x=0.5,**k: dict(x=x,pose=pose,face=face,**k)
P=lambda k,x,y,s=1,**kk: dict(k=k,x=x,y=y,s=s,**kk)
b("You studied for two hours. One hour later, half of it is gone.",chars=[C('shock','shock',0.42)],props=[P('book',0.74,0.32,0.8)],big="-50%",bigx=0.72,bigy=0.24,bigs=130)
b("That's not you being dumb. That's the forgetting curve.",chars=[C('point','smirk',0.3)],props=[P('graph',0.68,0.38,0.9)])
b("Back in eighteen eighty five, a psychologist called Ebbinghaus tested his own memory,",chars=[C('read','neutral',0.4,hold='notes')],big="1885",bigx=0.72,bigy=0.24,bigs=120,bigc='#f6c23e')
b("and found that memories drop fast at first, and then more slowly.",chars=[C('sad','sad',0.35)],props=[P('graph',0.66,0.38,0.85),P('arrowdown',0.8,0.25,0.5,d=0.3)])
b("Rereading your notes doesn't fix it. It just makes them feel familiar.",chars=[C('read','neutral',0.4,hold='book')],props=[P('cross',0.78,0.3,0.8,d=0.3)])
b("What fixes it is closing the book, and forcing yourself to remember.",chars=[C('think','focus',0.4)],props=[P('book',0.75,0.38,0.8),P('cross',0.75,0.38,0.5,d=0.4)])
b("Then do it again tomorrow, and again in three days.",chars=[C('point','happy',0.3)],props=[P('calendar',0.6,0.3,0.55,label='Day 1'),P('calendar',0.78,0.3,0.55,d=0.5,label='Day 3')])
b("Every time you pull it back out, the curve gets flatter.",chars=[C('cheer','happy',0.42)],props=[P('arrowup',0.78,0.32,1)])
b("I ranked every study technique from useless to genius. Full video on the channel.",chars=[C('pointup','smirk',0.4)],props=[P('trophy',0.75,0.33,0.9,float=1)])
json.dump({'titulo':'Why You Forget What You Studied 1 Hour Ago','lang':'en','frases':F,
 'fuentes':['Ebbinghaus (1885), Über das Gedächtnis; forgetting curve','Dunlosky et al. (2013), Psychological Science in the Public Interest']},open('s2/guion.json','w'),ensure_ascii=False,indent=1)
print(len(F),sum(len(f['t'].split()) for f in F))
