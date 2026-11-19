import json
F=[]
def b(t,head=None,chars=None,props=None,big=None,**kw):
    v={}
    if head: v['head']=head
    if chars: v['chars']=chars
    if props: v['props']=props
    if big: v['big']=big
    v.update(kw); F.append({'t':t,'v':v,'esc':'A'})
C=lambda pose,face='neutral',x=0.35,**k: dict(x=x,pose=pose,face=face,**k)
P=lambda k,x,y,s=1,**kk: dict(k=k,x=x,y=y,s=s,**kk)
# ---------- HOOK ----------
b("Most students spend hours studying, and remember almost nothing.",chars=[C('read','neutral',0.35,hold='book')],props=[P('clock',0.7,0.38,1.1)])
b("And it's not because they're lazy.",chars=[C('shrug','neutral',0.45)])
b("It's because they're using the wrong techniques.",chars=[C('sitsad','sad',0.4)],props=[P('gradeF',0.7,0.45,1)])
b("So today, we're ranking every study technique, from completely useless,",head="EVERY STUDY TECHNIQUE",chars=[C('point','smirk',0.3)],props=[P('cross',0.68,0.45,1)])
b("to the one that's basically a cheat code.",chars=[C('cheer','happy',0.5)],props=[P('trophy',0.78,0.45,1,float=1)])
b("And stick around, because number one is the thing most students do the least.",chars=[C('think','smirk',0.35)],props=[P('question',0.7,0.35,1.2)])
b("But first, you need to know what you're fighting against.",chars=[C('stand','focus',0.4)])
b("In eighteen eighty five, a German psychologist called Hermann Ebbinghaus memorized lists of nonsense syllables, and tested how fast he forgot them.",chars=[C('read','neutral',0.3,hold='notes')],big="1885",bigx=0.7,bigy=0.25,bigs=110,bigc='#f6c23e')
b("The result is called the forgetting curve. Memories fade fast at first, and then more slowly.",chars=[C('point','neutral',0.3)],props=[P('graph',0.68,0.42,1.3)])
b("Within the first hour, a big chunk of what you learned can already be gone.",chars=[C('shock','shock',0.35)],props=[P('graph',0.7,0.42,1.1),P('arrowdown',0.86,0.3,0.7,d=0.3)])
b("The good news is that some techniques flatten that curve. The bad news is that most students use the other ones.",chars=[C('shrug','smirk',0.4)])
# 14 rereading
b("Number fourteen. Rereading.",head="#14 REREADING",chars=[C('read','neutral',0.4,hold='book')])
b("You read the chapter. Then you read it again. And again.",chars=[C('read','neutral',0.35,hold='book')],props=[P('book',0.62,0.4,0.8),P('book',0.75,0.4,0.8,d=0.4),P('book',0.88,0.4,0.8,d=0.8)])
b("By the third time, everything feels familiar, so your brain thinks you've learned it.",chars=[C('stand','smirk',0.4)],props=[P('brain',0.7,0.38,1.1,float=1),P('check',0.84,0.25,0.7,d=0.5)])
b("But familiar is not the same as remembered.",chars=[C('shock','shock',0.4)],props=[P('cross',0.72,0.4,1)])
b("In a famous review of learning techniques from twenty thirteen, rereading was rated as low utility.",chars=[C('point','neutral',0.3)],props=[P('exam',0.65,0.4,1,label='2013 review')],big="LOW UTILITY",bigx=0.68,bigy=0.18,bigs=90)
b("It feels productive. It mostly isn't.",chars=[C('facepalm','sad',0.45)])
b("If you really want to reread, do it after you've tried to remember the material first. Then it actually helps.",chars=[C('point','neutral',0.3)],props=[P('book',0.7,0.42,1),P('check',0.84,0.3,0.6,d=0.4)])
# 13 highlighting
b("Number thirteen. Highlighting.",head="#13 HIGHLIGHTING",chars=[C('write','focus',0.4)],props=[P('desk',0.47,0.72,1),P('notes',0.53,0.6,0.6)])
b("You grab a yellow marker, and suddenly the entire page is yellow.",chars=[C('hold','happy',0.35,hold='pencil')],props=[P('notes',0.68,0.42,1.2)],big="100% YELLOW",bigx=0.7,bigy=0.18,bigs=80,bigc='#f6c23e')
b("Highlighting tells you what looks important. It doesn't put it inside your head.",chars=[C('shrug','neutral',0.4)],props=[P('brain',0.72,0.4,1)])
b("Same review, same verdict. Low utility.",chars=[C('stand','smirk',0.4)],big="LOW UTILITY",bigx=0.7,bigy=0.3,bigs=90)
b("And the worst part is that highlighting makes you lazy, because the marker does the thinking for you.",chars=[C('sitsad','sad',0.4)],props=[P('pencil',0.7,0.4,1)])
b("If you love your highlighter, use it only after you've finished reading, and only for one sentence per page.",chars=[C('pointup','smirk',0.35)],big="1 PER PAGE",bigx=0.7,bigy=0.3,bigs=80,bigc='#3a7bd5')
# 12 cramming
b("Number twelve. The all nighter.",head="#12 CRAMMING",chars=[C('write','focus',0.4)],props=[P('desk',0.47,0.72,1),P('coffee',0.6,0.6,0.6,anim=1),P('clock',0.75,0.3,0.9)])
b("It's three in the morning, the exam is at nine, and you're on your fifth coffee.",chars=[C('dizzy','dead',0.4)],props=[P('coffee',0.65,0.5,0.8,anim=1),P('coffee',0.75,0.5,0.8,d=0.2),P('coffee',0.85,0.5,0.8,d=0.4)],big="3:00 AM",bigx=0.7,bigy=0.2,bigs=90)
b("The problem is that your brain stores memories while you sleep.",chars=[C('sleep','sleep',0.5,y=0.7)],props=[P('bed',0.52,0.72,1.3),P('brain',0.75,0.3,0.9,float=1)])
b("Skip the sleep, and you skip the saving.",chars=[C('sad','sad',0.4)],props=[P('battery',0.7,0.4,1,anim='low')])
b("You might pass tomorrow. In a week, it's gone.",chars=[C('shrug','neutral',0.4)],props=[P('calendar',0.72,0.4,1,label='1 week later')])
b("Cramming works like a short term loan. You get the money now, and you pay it back with interest later.",chars=[C('hold','smirk',0.35,hold='exam')],props=[P('arrowdown',0.72,0.4,1)])
b("Usually during the final exam, when you need all that stuff again.",chars=[C('shock','shock',0.4)],props=[P('gradeF',0.72,0.42,1)])
# 11 multitasking
b("Number eleven. Studying with your phone next to you.",head="#11 MULTITASKING",chars=[C('read','neutral',0.35,hold='book')],props=[P('phone',0.62,0.45,1)])
b("One notification. Just one. And forty minutes later you're watching videos about how bridges are built.",chars=[C('hold','happy',0.4,hold='phone')],props=[P('gamepad',0.72,0.35,0.9,d=0.6)],big="40 MIN",bigx=0.75,bigy=0.6,bigs=80)
b("Every time you switch tasks, your brain pays a switching cost, and you lose focus that takes a while to get back.",chars=[C('dizzy','dead',0.45)],props=[P('arrowdown',0.75,0.4,1)])
b("Put the phone in another room. Not face down. Another room.",chars=[C('point','angry',0.3)],props=[P('phone',0.75,0.45,0.8),P('cross',0.75,0.45,0.9,d=0.3)])
b("Same goes for studying with a show playing in the background. Your brain is not doing two things. It's doing two things badly.",chars=[C('dizzy','dead',0.4)],props=[P('gamepad',0.72,0.4,0.9)])
# 10 summarizing
b("Number ten. Summarizing.",head="#10 SUMMARIZING",chars=[C('write','focus',0.4)],props=[P('desk',0.47,0.72,1),P('notes',0.53,0.6,0.6)])
b("Writing a summary can help, but only if you do it well.",chars=[C('stand','neutral',0.4)],props=[P('notes',0.7,0.4,1)])
b("Most people just copy the book in fewer words, which is basically rereading with extra steps.",chars=[C('facepalm','sad',0.4)],props=[P('book',0.65,0.4,0.9),P('notes',0.8,0.4,0.9)])
b("The review rated it low utility too, mostly because it's hard to do right.",chars=[C('shrug','neutral',0.4)],big="LOW UTILITY",bigx=0.7,bigy=0.25,bigs=80)
b("The trick is to close the book first, and summarize from memory. Now you're actually working.",chars=[C('write','focus',0.35)],props=[P('desk',0.42,0.72,1),P('book',0.72,0.4,0.8),P('cross',0.72,0.4,0.5,d=0.4)])
# 9 mnemonics
b("Number nine. Mnemonics.",head="#9 MNEMONICS",chars=[C('think','neutral',0.35)],props=[P('bulb',0.7,0.35,1)])
b("Silly sentences and acronyms, where the first letter of each word reminds you of something.",chars=[C('point','happy',0.3)],big="M.V.E.M.J.S.U.N.",bigx=0.66,bigy=0.3,bigs=70,bigc='#3a7bd5')
b("They're great for short lists, like the order of the planets.",chars=[C('cheer','happy',0.4)],props=[P('check',0.75,0.4,1)])
b("But they won't help you understand anything. They're a shortcut, not a strategy.",chars=[C('stand','smirk',0.4)],props=[P('cross',0.72,0.4,0.8)])
b("Knowing that a sentence about pizza stands for the planets doesn't mean you know anything about the planets.",chars=[C('facepalm','sad',0.4)],props=[P('question',0.72,0.35,1)])
# 8 mind maps
b("Number eight. Mind maps.",head="#8 MIND MAPS",chars=[C('point','neutral',0.3)],props=[P('bulb',0.6,0.3,0.6),P('book',0.75,0.45,0.6,d=0.2),P('brain',0.88,0.3,0.6,d=0.4)])
b("You put one idea in the middle, and draw branches to everything connected to it.",chars=[C('write','focus',0.35)],props=[P('desk',0.42,0.72,1),P('notes',0.48,0.6,0.6),P('graph',0.72,0.35,0.9)])
b("They're good for organizing a topic and seeing the big picture.",chars=[C('stand','happy',0.4)],props=[P('check',0.72,0.4,0.9)])
b("Just don't spend three hours making it pretty. That's arts and crafts, not studying.",chars=[C('facepalm','sad',0.4)],props=[P('pencil',0.72,0.4,1)])
# 7 pomodoro
b("Number seven. The Pomodoro technique.",head="#7 POMODORO",chars=[C('stand','neutral',0.35)],props=[P('clock',0.7,0.4,1.2)])
b("Work for twenty five minutes, take a five minute break, and repeat.",chars=[C('write','focus',0.35)],props=[P('desk',0.42,0.72,1),P('clock',0.72,0.3,0.9)],big="25 + 5",bigx=0.75,bigy=0.6,bigs=90,bigc='#e8483f')
b("It won't make you remember more, but it makes starting a lot less painful.",chars=[C('shrug','neutral',0.4)],props=[P('arrowup',0.72,0.4,0.9)])
b("And for most people, starting is the hardest part.",chars=[C('think','smirk',0.4)])
b("Twenty five minutes sounds easy. Your brain agrees to it. And once you've started, you usually keep going.",chars=[C('write','happy',0.35)],props=[P('desk',0.42,0.72,1),P('clock',0.72,0.3,0.9)])
b("Just make sure the five minute break doesn't turn into a two hour break.",chars=[C('sleep','sleep',0.5,y=0.7)],props=[P('bed',0.52,0.72,1.3),P('phone',0.75,0.4,0.7)])
# 6 feynman
b("Number six. The Feynman technique.",head="#6 FEYNMAN TECHNIQUE",chars=[C('point','neutral',0.3)],props=[P('bulb',0.7,0.35,1,anim=1)])
b("Pick a topic, and explain it in simple words, as if you were teaching a twelve year old.",chars=[C('point','happy',0.3),dict(id='kid',x=0.68,pose='think',face='neutral',s=0.7,flip=True)])
b("The moment you get stuck, you've found exactly what you don't understand yet.",chars=[C('shock','shock',0.35)],props=[P('question',0.7,0.35,1.1)])
b("Go back, fill that gap, and try again.",chars=[C('read','focus',0.4,hold='book')])
b("If you can't explain it simply, you don't understand it well enough yet. And that's fine. Now you know.",chars=[C('shrug','happy',0.4)],props=[P('bulb',0.72,0.35,1,anim=1)])
# 5 elaboration
b("Number five. Asking why.",head="#5 ASKING WHY",chars=[C('think','neutral',0.35)],props=[P('question',0.62,0.3,0.9),P('question',0.75,0.38,0.8,d=0.3),P('question',0.86,0.3,0.7,d=0.6)])
b("Instead of just memorizing a fact, you ask yourself why it's true.",chars=[C('think','focus',0.4)],props=[P('notes',0.72,0.4,1)])
b("Researchers call this elaborative interrogation, and it connects new information to things you already know.",chars=[C('point','neutral',0.3)],props=[P('brain',0.7,0.4,1.1,float=1)])
b("Rated moderate utility. Not magic, but genuinely useful.",chars=[C('stand','happy',0.4)],big="MODERATE",bigx=0.7,bigy=0.25,bigs=90,bigc='#f08a2c')
b("For example, instead of memorizing that hot air rises, ask why. Because it's less dense. Why? And now you're actually learning physics.",chars=[C('point','focus',0.3)],props=[P('arrowup',0.68,0.4,1),P('question',0.82,0.3,0.8,d=0.4)])
# 4 interleaving
b("Number four. Interleaving.",head="#4 INTERLEAVING",chars=[C('stand','neutral',0.35)],props=[P('book',0.62,0.4,0.7),P('notes',0.74,0.4,0.7),P('exam',0.86,0.4,0.7)])
b("Instead of doing twenty problems of the same type, you mix different types together.",chars=[C('write','focus',0.35)],props=[P('desk',0.42,0.72,1),P('card',0.7,0.3,0.8),P('card',0.82,0.38,0.8,d=0.3)])
b("It feels harder, and that's exactly why it works.",chars=[C('dizzy','dead',0.4)],props=[P('arrowup',0.72,0.4,1)])
b("Your brain has to figure out which method to use, just like in a real exam.",chars=[C('think','focus',0.35)],props=[P('exam',0.7,0.42,1)])
b("Because in the exam, nobody tells you which chapter the question came from.",chars=[C('shock','shock',0.4)],props=[P('exam',0.72,0.42,1),P('question',0.85,0.3,0.7,d=0.3)])
# 3 sleep
b("Number three. Sleep.",head="#3 SLEEP",chars=[C('sleep','sleep',0.5,y=0.7)],props=[P('bed',0.52,0.72,1.3),P('zzz',0.64,0.45,1,float=1)])
b("Yes, sleep is a study technique.",chars=[C('point','smirk',0.35)],props=[P('bed',0.7,0.72,1)])
b("While you sleep, your brain replays what you learned and moves it into long term memory.",chars=[C('sleep','sleep',0.4,y=0.7)],props=[P('bed',0.42,0.72,1.3),P('brain',0.72,0.32,1,float=1),P('arrowup',0.86,0.32,0.7,d=0.4)])
b("A good night of sleep before an exam beats an extra night of studying almost every time.",chars=[C('cheer','happy',0.45)],props=[P('gradeA',0.75,0.42,1)])
b("Which means that technically, going to bed early is studying. You're welcome.",chars=[C('stand','smirk',0.4)],props=[P('bed',0.72,0.72,1),P('zzz',0.78,0.45,0.8,float=1)])
# 2 spaced repetition
b("Number two. Spaced repetition.",head="#2 SPACED REPETITION",chars=[C('stand','neutral',0.35)],props=[P('calendar',0.7,0.4,1.2)])
b("Instead of studying something five times in one day, you study it once today, again tomorrow, then in three days, then in a week.",chars=[C('point','neutral',0.3)],props=[P('calendar',0.6,0.4,0.7,label='Day 1'),P('calendar',0.72,0.4,0.7,d=0.6,label='Day 2'),P('calendar',0.84,0.4,0.7,d=1.2,label='Day 5')])
b("Every time you come back right before you forget, the memory gets stronger, and fades more slowly.",chars=[C('think','happy',0.3)],props=[P('graph',0.68,0.4,1.2)])
b("The review gave it the highest rating possible. High utility.",chars=[C('cheer','happy',0.4)],big="HIGH UTILITY",bigx=0.7,bigy=0.25,bigs=90,bigc='#3fb06b')
b("Flashcard apps are built entirely around this idea.",chars=[C('hold','happy',0.4,hold='phone')],props=[P('card',0.72,0.4,1)])
b("Ten minutes a day, spread across the week, beats three hours the night before.",chars=[C('point','happy',0.3)],big="10 MIN > 3 H",bigx=0.7,bigy=0.3,bigs=90,bigc='#3fb06b')
# 1 active recall
b("And number one. Active recall.",head="#1 ACTIVE RECALL",chars=[C('cheer','happy',0.45)],props=[P('trophy',0.75,0.42,1.2,float=1)])
b("Close the book, and try to remember what you just studied, without looking.",chars=[C('think','focus',0.35)],props=[P('book',0.7,0.45,1),P('cross',0.7,0.45,0.6,d=0.4)])
b("Write it down, say it out loud, or answer practice questions.",chars=[C('write','focus',0.35)],props=[P('desk',0.42,0.72,1),P('card',0.72,0.3,0.9),P('exam',0.85,0.42,0.8,d=0.3)])
b("It's uncomfortable, because you'll realize how much you don't know.",chars=[C('sad','sad',0.4)],props=[P('question',0.72,0.35,1)])
b("But every time you pull a memory out of your brain, you make it easier to find next time.",chars=[C('pointup','happy',0.35)],props=[P('brain',0.7,0.4,1.1,float=1),P('arrowup',0.84,0.3,0.8,d=0.4)])
b("In the same review, practice testing got the highest rating. And here's the twist.",chars=[C('point','smirk',0.3)],big="HIGH UTILITY",bigx=0.7,bigy=0.25,bigs=90,bigc='#3fb06b')
b("It's the technique students use the least, because rereading just feels easier.",chars=[C('facepalm','sad',0.4)],props=[P('book',0.72,0.45,1)])
# outro
b("So here's the plan. Test yourself, space it out, and sleep.",chars=[C('point','happy',0.3)],props=[P('card',0.6,0.4,0.7),P('calendar',0.74,0.4,0.7,d=0.3),P('bed',0.88,0.5,0.6,d=0.6)])
b("Less time studying. More stuff actually remembered.",chars=[C('cheer','happy',0.45)],props=[P('gradeA',0.75,0.42,1)])
b("If this helped, you already know what to do next. Test yourself on it tomorrow.",chars=[C('point','smirk',0.3)],props=[P('calendar',0.72,0.4,1)])
b("Now close this video, and try to remember all fourteen. Good luck.",chars=[C('stand','smirk',0.4)],props=[P('question',0.72,0.35,1)])
json.dump({'titulo':'Every Study Technique Ranked from Useless to Genius','lang':'en','frases':F,
 'fuentes':['Dunlosky, Rawson, Marsh, Nathan & Willingham (2013), Improving Students\' Learning With Effective Learning Techniques, Psychological Science in the Public Interest, doi:10.1177/1529100612453266','APS press release: Which Study Strategies Make the Grade?']},open('l1/guion.json','w'),ensure_ascii=False,indent=1)
print(len(F),'frases',sum(len(f['t'].split()) for f in F),'palabras')
