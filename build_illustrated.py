from pathlib import Path
from bs4 import BeautifulSoup
from PIL import Image
import json,shutil
root=Path('.')
if not Path('text-reader.html').exists(): shutil.copyfile('index.html','text-reader.html')
source=BeautifulSoup(Path('text-reader.html').read_text(encoding='utf-8'),'html.parser')
captions=[
('A Boy in Greece','Long ago, in Greece, there was a boy named Theseus. He lived with his mom, Aethra.'),
('The Big Rock','One day, his mom took him to a big rock. His dad had left a gift under it.'),
('One More Try','Theseus pushed the rock. He pushed again, and at last the rock moved!'),
('A Gift from His Father','Under the rock were a sword and a pair of shoes. They had belonged to his dad, King Aegeus of Athens.'),
('Ready to Go','Aethra told Theseus he was ready to meet his dad. Theseus wanted to make his mom proud.'),
('The Long Road','Theseus could take a boat to Athens. But he chose the long road, even though it was not safe.'),
('Courage on the Road','Bad men hurt people on the road. Theseus was scared, but he fought them and stopped them.'),
('A Safer Journey','Theseus helped keep the road safe. At last, he came to Athens.'),
('Home at Last','King Aegeus saw the sword and shoes and knew his son. They gave each other a big hug.'),
('The Sad Children','Theseus saw a group of sad kids. They had to go to Crete, where the Minotaur lived in a huge maze.'),
('A Brave Choice','The young people sent to the maze did not come home. Theseus felt scared, but he chose to go and help.'),
('Ariadne’s Gift','Princess Ariadne was kind and smart. She gave Theseus a ball of red thread to help him find his way out.'),
('Into the Maze','Theseus let the thread fall as he walked. The dark path went left, then right, then left again.'),
('The Minotaur','Suddenly, the Minotaur was there! Theseus took out his sword and stood tall, even though his hands shook.'),
('The Way Out','Theseus won the fight and followed the thread back. He led the kids out of the maze, and they were free.'),
('Sailing Away','Theseus and Ariadne sailed away together. They came to an island called Naxos.'),
('A Friend Left Behind','Theseus left Ariadne on the island. She had helped save his life, but now she was alone.'),
('The Forgotten Sail','Theseus had promised to put up a white sail if he came home safe. But he forgot, and the ship still had its black sail.'),
('A Father’s Grief','King Aegeus saw the black sail and thought his son was dead. In his grief, he jumped into the sea and never came back.'),
('A Promise Lost','When Theseus got home, he heard the news and cried. He had won a big fight, but he had lost his dad.'),
('One Big Team','Theseus became king and helped bring the towns near Athens together. People could do more when they worked as a team.'),
('A Very Bad Plan','Theseus and Pirithous tried to take Persephone away without asking her. Hades caught them in the land of the dead, and they were stuck.'),
('Help from Heracles','Later, Heracles came and saved Theseus. Being brave had not made his bad plan right.'),
('The Lie','Phaedra told a terrible lie about Hippolytus. Theseus became angry and did not stop to hear his son’s side.'),
('Too Late to Listen','Theseus asked Poseidon to punish his son, and Hippolytus died. Later, Theseus learned that his son had done nothing wrong.'),
('The Last Journey','As an old man, Theseus left Athens and went to Skyros. There, King Lycomedes pushed him off a cliff, and Theseus died.'),
('What Makes a Hero?','Many years later, people brought his bones to Athens and honored him. His story reminds us that a real hero is kind, fair, and true.')]
manifest=[]
for g in range(1,4):
 p=Path(f'source_images/grid-{g:02d}.png')
 if not p.exists(): continue
 im=Image.open(p);w,h=im.size
 for i in range(9):
  n=(g-1)*9+i+1;r,c=divmod(i,3)
  xs=[0,381,804,w] if g==2 else [0,round(w/3),round(2*w/3),w]; ys=[0,421,827,h] if g==2 else [0,round(h/3),round(2*h/3),h]
  tile=im.crop((xs[c]+2,ys[r]+2,xs[c+1]-2,ys[r+1]-2))
  out=f'assets/scenes/scene-{n:02d}.webp';tile.save(out,'WEBP',quality=92)
  title,txt=captions[n-1];manifest.append(dict(id=n,grid=g,row=r,column=c,title=title,text=txt,image=out,native_grid=[w,h]))
article=source.select_one('article');hero=article.select_one('.hero');hero.insert_after(BeautifulSoup('<p><a href="text-reader.html">Read the complete original text</a> · <a href="characters.html">Character Bible</a></p>','html.parser'))
for s in article.select('.chapter'): s.decompose()
end=article.select_one('.end')
for item in manifest:
 s=source.new_tag('section',attrs={'class':'chapter scene','id':f'scene-{item["id"]}'})
 img=source.new_tag('img',src=item['image'],alt=item['title'],loading='lazy',width='800',height='800');s.append(img)
 title=source.new_tag('h2');title.string=item['title'];s.append(title)
 p=source.new_tag('p');p.string=item['text'];s.append(p);end.insert_before(s)
nav=source.select_one('.toc nav');nav.clear()
for item in manifest:
 a=source.new_tag('a',href=f'#scene-{item["id"]}');a.string=item['title'];nav.append(a)
source.select_one('.toc strong').string='Scenes'
style=source.new_tag('style');style.string='.scene img{display:block;width:100%;height:auto;border-radius:12px;margin-bottom:24px}.scene{padding:clamp(16px,4vw,36px)}.scene h2{font-size:1.5rem}.scene p{font-size:var(--size,1.16rem)}';source.head.append(style)
Path('index.html').write_text(str(source),encoding='utf-8')
Path('scene-manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
for p in [Path('index.html'),Path('text-reader.html')]: shutil.copyfile(p,Path('dist')/p.name)
shutil.copytree('assets/scenes','dist/assets/scenes',dirs_exist_ok=True)
assert len(manifest)==len(source.select('.scene'))
assert all(Path(x['image']).exists() for x in manifest)
print(f'Built {len(manifest)} image-first scenes; original text preserved in text-reader.html')
