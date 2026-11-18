from pathlib import Path
import base64
p=Path('dist')
h=(p/'index.html').read_text(encoding='utf-8')
h=h.replace('<link rel="stylesheet" href="style.css">','<style>'+(p/'style.css').read_text(encoding='utf-8')+'</style>')
h=h.replace('<script src="app.js"></script>','<script>'+(p/'app.js').read_text(encoding='utf-8')+'</script>')
h=h.replace('src="tga-logo.png"','src="data:image/png;base64,'+base64.b64encode((p/'tga-logo.png').read_bytes()).decode()+'"')
Path('../TGA_Partner_Dashboard.html').write_text(h,encoding='utf-8')
