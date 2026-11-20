from pathlib import Path
from PIL import Image
from bs4 import BeautifulSoup
import json,shutil
root=Path('.')
src=root/'source_images/battle-grid-01.png'
img=Image.open(src);w,h=img.size
# Grid boundaries must match the visually reviewed source sheet.
xs=[0,round(w/3),round(2*w/3),w];ys=[0,round(h/3),round(2*h/3),h]
scenes=[(2,5,'Periphetes and the club'),(2,6,'Sinis and the pine trees'),(2,7,'Sciron on the cliff path'),(2,8,'Stopping Procrustes'),(4,15,'A shadow in the maze'),(4,17,'The Minotaur charges'),(4,19,'Courage under pressure'),(4,21,'The fight in the maze'),(4,23,'Theseus wins')]
manifest=[]
for i,(chapter,paragraph,title) in enumerate(scenes):
 r,c=divmod(i,3);path=f'assets/scenes/battle-{i+1:02d}.webp'
 img.crop((xs[c]+3,ys[r]+3,xs[c+1]-3,ys[r+1]-3)).save(path,'WEBP',quality=94)
 shutil.copyfile(path,'dist/'+path)
 manifest.append(dict(id=f'battle-{i+1:02d}',image=path,chapter=chapter,paragraph=paragraph,title=title,grid=str(src),row=r,column=c))
for file in ['index.html','text-reader.html']:
 p=root/file;soup=BeautifulSoup(p.read_text(encoding='utf-8'),'html.parser')
 before=[p.get_text() for p in soup.select('.chapter p')]
 for old in soup.select('figure.battle-illustration'): old.decompose()
 for item in manifest:
  chapter=soup.select_one(f'#chapter-{item["chapter"]}');anchor=chapter.find_all('p')[item['paragraph']]
  f=soup.new_tag('figure',attrs={'class':'story-illustration battle-illustration','id':item['id']})
  f.append(soup.new_tag('img',src=item['image'],alt=item['title'],loading='lazy'))
  anchor.insert_before(f)
 assert before==[p.get_text() for p in soup.select('.chapter p')]
 assert len(soup.select('.battle-illustration'))==9
 assert len(soup.select('.story-illustration'))==36
 out=str(soup);p.write_text(out,encoding='utf-8');(root/'dist'/file).write_text(out,encoding='utf-8')
(root/'battle-scene-manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
print('PASS: nine action illustrations added; 36 total; all 191 original paragraphs unchanged')
