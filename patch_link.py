from pathlib import Path
for f in [Path('index.html'),Path('dist/index.html')]:
 s=f.read_text(encoding='utf-8')
 s=s.replace('<div class="brand">THE STORY HOME · MYTHS FOR YOUNG READERS</div>','<div class="brand"><a href="index.html" style="color:inherit;text-decoration:none">THE STORY HOME · MYTHS FOR YOUNG READERS</a></div>')
 s=s.replace('<button onclick="read()" id="read">▶ Read aloud</button>','<button onclick="read()" id="read">▶ Read aloud</button><a href="characters.html" style="display:inline-block;border:1px solid #e7dcc8;background:#fffdf7;color:#202a35;border-radius:999px;padding:8px 12px;font:600 .85rem system-ui;text-decoration:none">✦ Character Bible</a>')
 f.write_text(s,encoding='utf-8')
