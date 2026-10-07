import re, sys, json, html
from urllib.parse import quote
src = open(sys.argv[1], encoding='utf-8').read()
tpl = src[src.index('</helmet>')+len('</helmet>'):src.index('</x-dc>')]
head_extra = src[src.index('<link rel="preconnect"'):src.index('</helmet>')].strip()
assert head_extra.endswith('</style>'); head_extra = head_extra[:-len('</style>')]

WA = 'https://api.whatsapp.com/send?phone=5519982437674&text='
def wa(p=''): return WA + quote('Olá! Vim pelo site e gostaria de um orçamento' + (' de ' + p if p else '') + '.', safe='')
U = 'images/'
sys_ = [
 dict(name='Tela de Fachada', imgs=['WhatsApp-Image-2020-09-01-at-15.19.15-768x1024-1.jpeg','WhatsApp-Image-2023-01-30-at-13.11.15-1-768x1024.jpeg'],
  desc='Produzida com monofilamentos de polietileno de alta densidade, protege calçadas e áreas vizinhas à obra contra a queda de materiais, reboco, alvenaria ou ferramentas.',
  items=['Suporte metálico (locação e venda)','Modulação de tela','Equipe técnica para instalação','ART de instalação']),
 dict(name='Rede Piso a Piso · Sistema U', imgs=['WhatsApp-Image-2023-01-30-at-13.11.15-768x1024.jpeg','WhatsApp-Image-2023-01-30-at-13.11.15-1-768x1024.jpeg'],
  desc='Segurança aos operários em todo o perímetro dos pavimentos, com fechamento total dos vãos antes da alvenaria. Ótimo custo-benefício, instalação e manutenção rápidas. Atende à ABNT NBR 14718.',
  items=['Instalação e ascensão por equipe própria','Projeto','ART de instalação','Instalação rápida']),
 dict(name='SLQA', imgs=['WhatsApp-Image-2020-09-01-at-15.19.10-768x1024-1.jpeg'],
  desc='Impede a queda de objetos ou pessoas nos três últimos pavimentos em construção — a área de maior risco da obra. O sistema acompanha a subida da estrutura, envolvendo todo o perímetro em rede de proteção.',
  items=['Equipe técnica para instalação','Projeto','ART de instalação','Acompanha a subida da torre']),
 dict(name='Espera de Ancoragem', imgs=['ancoragemCerta-1.png'],
  desc='Pontos de ancoragem definitivos que resistem às cargas geradas em uma queda. Usados para descida de profissionais em fachadas e sustentação de balancins. Itens obrigatórios pela NR-35 e NR-18.',
  items=['Equipe técnica para instalação','ART de instalação','Laudo técnico','Teste de arranque']),
 dict(name='Proteção de Vizinhos', imgs=['WhatsApp-Image-2020-09-01-at-15.19.32-768x1024-1.jpeg'],
  desc='Garante a segurança de transeuntes e edificações vizinhas. Instalado com suportes e redes, evita a queda de detritos e ferramentas. Confeccionado sob medida, com mão de obra capacitada.',
  items=['Confecção sob medida','Equipe técnica para instalação','ART de instalação','Suportes e redes']),
]
telas = [
 ('Tela Hexagonal / Viveiros','Construção e agro','c80da883d9d29abe646323cc4a4ea494.jpg','Arame galvanizado em malha hexagonal. Isolamento de canteiros e elevadores, agricultura e criação de animais.'),
 ('Amarração de Alvenaria','Estrutura','8067124050.jpg','Tela soldada galvanizada, fio 1,24 mm e malha 15×15 mm. Evita fissuras entre estrutura e alvenaria.'),
 ('Telas Plásticas','Cercamento provisório','5.jpg','Mais barata, resistente à corrosão e fácil de instalar. Demarca obras e protege pedestres e patrimônio.'),
 ('Tela Soldada','Segurança patrimonial','tela-soldada-2.jpg','Fios zincados a fogo com tripla camada e eletrossoldados. Malha que não abre, para áreas industriais e residenciais.'),
 ('Tela Guarda-Corpo','Sinalização','fixsafe-tela-guarda-corpo-sinalizacao-3.png','Laranja com faixas brancas para máxima visibilidade. Delimita áreas de risco e extremidades de lajes.'),
 ('Alambrado Revestido PVC','Cercamento','669370601011075.jpg','Ideal para casas e terrenos irregulares. Instalação em mourões de madeira, concreto ou metal.'),
]
e = html.escape
out = tpl

# style-hover -> class-based hover rules
hovers = []
def hov(m):
    hovers.append(m.group(1)); return f'class="h{len(hovers)}"'
out = re.sub(r'style-hover="([^"]*)"', hov, out)
hover_css = '\n'.join(f'.h{i+1}:hover{{{ "".join(d.strip()+" !important;" for d in h.split(";") if d.strip()) }}}' for i,h in enumerate(hovers))

# tabs
tabs = ''.join(f'<button type="button" class="sys-tab" role="tab" data-i="{i}" aria-selected="{"true" if i==0 else "false"}">{e(s["name"])}</button>' for i,s in enumerate(sys_))
out = re.sub(r'<sc-for list="\{\{ tabs \}\}".*?</sc-for>', lambda m: tabs, out, flags=re.S)
# system images
def imgs_html(s):
    return ''.join(f'<div style="background:#e2dfdb;overflow:hidden;position:relative;min-height:260px"><div role="img" aria-label="{e(s["name"])}" style="position:absolute;inset:0;background-size:cover;background-position:center;background-image:url({U}{f})"></div></div>' for f in s['imgs'])
out = re.sub(r'<sc-for list="\{\{ cur.imgs \}\}".*?</sc-for>', lambda m: imgs_html(sys_[0]), out, flags=re.S)
item_tpl = '<div style="background:#fff;padding:14px 16px;display:flex;align-items:center;gap:12px;font-weight:600;font-size:16px"><span style="width:8px;height:8px;background:#C41E2A;flex:none"></span>{}</div>'
out = re.sub(r'<sc-for list="\{\{ cur.items \}\}".*?</sc-for>', lambda m: ''.join(item_tpl.format(e(i)) for i in sys_[0]['items']), out, flags=re.S)
out = out.replace('<div style="display:grid;grid-template-columns:{{ cur.cols }}', '<div id="sys-imgs" style="display:grid;grid-template-columns:1fr 1fr')
for k,v in {'{{ cur.num }}':'01 / 05','{{ cur.name }}':e(sys_[0]['name']),'{{ cur.desc }}':e(sys_[0]['desc']),'{{ cur.wa }}':e(wa(sys_[0]['name']))}.items():
    out = out.replace(k, v)
out = out.replace('<span style="font-family:\'Barlow Condensed\',sans-serif;font-weight:700;font-size:18px;letter-spacing:.1em;color:#C41E2A">01 / 05', '<span id="sys-num" style="font-family:\'Barlow Condensed\',sans-serif;font-weight:700;font-size:18px;letter-spacing:.1em;color:#C41E2A">01 / 05')
out = out.replace('<h3 style="margin:0;font-family:\'Barlow Condensed\',sans-serif;font-weight:800;font-size:clamp(36px,3.6vw,48px)', '<h3 id="sys-name" style="margin:0;font-family:\'Barlow Condensed\',sans-serif;font-weight:800;font-size:clamp(36px,3.6vw,48px)')
out = out.replace('<p style="margin:0;font-size:18px;line-height:1.65;color:#444;text-wrap:pretty">'+e(sys_[0]['desc']), '<p id="sys-desc" style="margin:0;font-size:18px;line-height:1.65;color:#444;text-wrap:pretty">'+e(sys_[0]['desc']))
out = out.replace('<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:10px">', '<div id="sys-items" style="display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:10px">',1)
out = out.replace('<a href="'+e(wa(sys_[0]['name']))+'"', '<a id="sys-wa" href="'+e(wa(sys_[0]['name']))+'"',1)

# products
m = re.search(r'<sc-for list="\{\{ telas \}\}"[^>]*>(.*?)</sc-for>', out, re.S)
card = m.group(1)
cards = ''
for n,t,img,d in telas:
    c = card.replace('{{ p.name }}', e(n)).replace('{{ p.tag }}', e(t)).replace('{{ p.desc }}', e(d)).replace('{{ p.wa }}', e(wa(n))).replace('{{ p.img }}', f'url({U}{img})')
    cards += c
out = out[:m.start()] + cards + out[m.end():]

# FAB
out = re.sub(r'<sc-if value="\{\{ showFab \}\}"[^>]*>(.*?)</sc-if>', r'\1', out, flags=re.S)
out = out.replace('{{ wa }}', e(wa()))
# external links safety
out = out.replace('target="_blank"', 'target="_blank" rel="noopener"')
# mobile menu button
MENU_BTN = '<button type="button" id="menu-btn" aria-label="Menu mobile" aria-expanded="false" aria-controls="top-nav" style="display:none;padding:8px 16px;background:transparent;border:1px solid #ddd;color:#222;font-family:\'Barlow Condensed\',sans-serif;font-weight:600;font-size:14px;letter-spacing:.04em;text-transform:uppercase">'
out, n = re.subn(r'<button\b(?:[^>"]|"[^"]*")*aria-label="Menu mobile"(?:[^>"]|"[^"]*")*>', lambda m: MENU_BTN, out, count=1)
assert n == 1, 'menu button not found'
out, n = re.subn(r'(<nav id="top-nav" style=")display:flex;', r'\1', out); assert n == 1
out = out.replace('button {display:block}', '#menu-btn {display:block !important}')
assert '{{' not in out and 'sc-' not in out, re.findall(r'\{\{[^}]*\}\}|<sc-\w+', out)

data = json.dumps([dict(name=s['name'], imgs=[U+f for f in s['imgs']], desc=s['desc'], items=s['items'], wa=wa(s['name'])) for s in sys_], ensure_ascii=False)
page = f'''<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>SP Telas · Proteção coletiva para obras em Hortolândia-SP</title>
<meta name="description" content="Tela de fachada, Rede Piso a Piso Sistema U, SLQA e pontos de ancoragem com projeto, ART e instalação por equipe própria. Atendimento em todo o estado de São Paulo.">
<meta property="og:title" content="SP Telas · Proteção coletiva do térreo à última laje">
<meta property="og:description" content="Sistemas de proteção NR-18 com projeto, ART e instalação por equipe própria.">
<meta property="og:image" content="images/WhatsApp-Image-2020-09-01-at-15.19.15-768x1024-1.jpeg">
<meta property="og:locale" content="pt_BR">
<meta name="theme-color" content="#C41E2A">
<link rel="icon" href="favicon.svg" type="image/svg+xml">
{head_extra.strip()}
#top-nav{{display:flex}}
.sys-tab{{background:none;border:none;cursor:pointer;padding:14px 22px;margin-bottom:-2px;border-bottom:3px solid transparent;color:#555;font-family:'Barlow Condensed',sans-serif;font-weight:700;font-size:18px;letter-spacing:.05em;text-transform:uppercase}}
.sys-tab[aria-selected="true"]{{border-bottom-color:#C41E2A;color:#C41E2A}}
.sys-tab:focus-visible,a:focus-visible,#menu-btn:focus-visible{{outline:2px solid #C41E2A;outline-offset:2px}}
{hover_css}
</style>
</head>
<body>
{out.strip()}
<script>
(function(){{
  var S={data};
  var btn=document.getElementById('menu-btn'),nav=document.getElementById('top-nav');
  btn.addEventListener('click',function(){{var o=nav.classList.toggle('active');btn.setAttribute('aria-expanded',o)}});
  nav.addEventListener('click',function(ev){{if(ev.target.closest('a')){{nav.classList.remove('active');btn.setAttribute('aria-expanded','false')}}}});
  var tabs=document.querySelectorAll('.sys-tab'),$=function(id){{return document.getElementById(id)}};
  function esc(s){{var d=document.createElement('div');d.textContent=s;return d.innerHTML}}
  tabs.forEach(function(b){{b.addEventListener('click',function(){{
    var i=+b.dataset.i,c=S[i];
    tabs.forEach(function(x){{x.setAttribute('aria-selected',x===b)}});
    $('sys-num').textContent=String(i+1).padStart(2,'0')+' / 05';
    $('sys-name').textContent=c.name;$('sys-desc').textContent=c.desc;$('sys-wa').href=c.wa;
    var g=$('sys-imgs');g.style.gridTemplateColumns=c.imgs.length>1?'1fr 1fr':'1fr';
    g.innerHTML=c.imgs.map(function(f){{return '<div style="background:#e2dfdb;overflow:hidden;position:relative;min-height:260px"><div role="img" aria-label="'+esc(c.name)+'" style="position:absolute;inset:0;background-size:cover;background-position:center;background-image:url('+f+')"></div></div>'}}).join('');
    $('sys-items').innerHTML=c.items.map(function(t){{return '<div style="background:#fff;padding:14px 16px;display:flex;align-items:center;gap:12px;font-weight:600;font-size:16px"><span style="width:8px;height:8px;background:#C41E2A;flex:none"></span>'+esc(t)+'</div>'}}).join('');
  }})}});
}})();
</script>
</body>
</html>
'''
open(sys.argv[2],'w',encoding='utf-8').write(page)
print('ok', len(page), 'hovers', len(hovers))
