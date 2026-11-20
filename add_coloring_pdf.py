from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4,landscape
from PIL import Image
from bs4 import BeautifulSoup
import shutil,fitz
root=Path('.');out=root/'downloads';out.mkdir(exist_ok=True)
image=Path(r'C:\Users\고보민\Downloads\루브르의 테세우스와 미노타우로스.png')
shutil.copyfile(image,'assets/theseus-coloring.png')
pdf=out/'theseus-minotaur-coloring-a4.pdf'
w,h=landscape(A4);margin=12
c=canvas.Canvas(str(pdf),pagesize=(w,h));c.setTitle('Theseus and the Minotaur - Coloring Page')
iw,ih=Image.open(image).size;scale=min((w-2*margin)/iw,(h-2*margin)/ih);dw,dh=iw*scale,ih*scale
c.drawImage(str(image),(w-dw)/2,(h-dh)/2,width=dw,height=dh);c.showPage();c.save()
assert dw<=w-2*margin+.01 and dh<=h-2*margin+.01
with fitz.open(pdf) as doc:
 assert len(doc)==1
 doc[0].get_pixmap(matrix=fitz.Matrix(1.3,1.3)).save('coloring-pdf-preview.png')
for file in ['index.html','text-reader.html']:
 p=root/file;s=BeautifulSoup(p.read_text(encoding='utf-8'),'html.parser')
 before=[x.get_text() for x in s.select('.chapter p')]
 section=BeautifulSoup('''<section class="chapter" id="coloring-download"><h2>Coloring Page</h2><p>Bring Theseus and the Minotaur to life with your own colors. Print this one-page PDF on A4 paper in landscape orientation.</p><a href="downloads/theseus-minotaur-coloring-a4.pdf" download="theseus-minotaur-coloring-a4.pdf" style="display:inline-block;padding:12px 20px;background:#254f69;color:white;border-radius:999px;text-decoration:none;font:600 1rem system-ui">Download Coloring PDF</a><figure class="story-illustration"><a href="downloads/theseus-minotaur-coloring-a4.pdf"><img src="assets/theseus-coloring.png" alt="Printable coloring page of Theseus and the Minotaur in a museum" loading="lazy"/></a></figure></section>''','html.parser').section
 s.select_one('.end').insert_before(section)
 nav=s.select_one('.toc nav');a=s.new_tag('a',href='#coloring-download');a.string='Coloring PDF';nav.append(a)
 assert [x.get_text() for x in s.select('.chapter:not(#coloring-download) p')]==before
 p.write_text(str(s),encoding='utf-8');shutil.copyfile(p,root/'dist'/file)
(root/'dist/downloads').mkdir(exist_ok=True)
shutil.copyfile(pdf,root/'dist'/pdf)
shutil.copyfile('assets/theseus-coloring.png','dist/assets/theseus-coloring.png')
print('PASS: 1 landscape A4 page, full image within margins, download and preview linked')
