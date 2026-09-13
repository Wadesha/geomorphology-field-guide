# -*- coding: utf-8 -*-
"""《地貌学及第四纪地质学》重构站 —— 静态站点生成器
用法：python build_site.py   输出至 ./docs（GitHub Pages 目录）
"""
import os, html, json, shutil
from site_data import (BOOK, AGENTS, REMAP, CASES, CONFUSIONS, TIMELINE)

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, 'docs')
AGENT_D = {a[0]: a for a in AGENTS}
E = html.escape


def css():
    return """
*{box-sizing:border-box}
:root{
  --bg:#fbfaf7; --panel:#ffffff; --panel2:#f5f2ec; --ink:#23201c; --muted:#6b6459;
  --line:#e6e1d7; --line2:#d8d2c5; --accent:#8a6d3b; --shadow:0 1px 2px rgba(0,0,0,.04),0 8px 24px rgba(0,0,0,.05);
}
html[data-theme=dark]{
  --bg:#15171a; --panel:#1c1f23; --panel2:#22262b; --ink:#e9e6e0; --muted:#9b948a;
  --line:#2d3137; --line2:#3a3f46; --accent:#c9a86a; --shadow:0 1px 2px rgba(0,0,0,.3),0 8px 24px rgba(0,0,0,.35);
}
body{margin:0;background:var(--bg);color:var(--ink);
  font-family:"Songti SC","Source Han Serif SC","Noto Serif CJK SC",Georgia,"PingFang SC","Microsoft YaHei",serif;
  font-size:15.5px;line-height:1.78;-webkit-font-smoothing:antialiased}
a{color:inherit}
.wrap{max-width:1120px;margin:0 auto;padding:0 20px}
nav{position:sticky;top:0;z-index:50;background:var(--bg);
  background:color-mix(in srgb,var(--bg) 88%,transparent);
  backdrop-filter:blur(10px);border-bottom:1px solid var(--line)}
nav .wrap{display:flex;align-items:center;gap:18px;height:54px;flex-wrap:wrap}
nav .brand{font-weight:700;letter-spacing:.02em;font-size:16px;text-decoration:none;white-space:nowrap}
nav .links{display:flex;gap:16px;flex-wrap:wrap;font-size:14.5px}
nav .links a{text-decoration:none;color:var(--muted);padding:2px 0;border-bottom:2px solid transparent}
nav .links a:hover,nav .links a.on{color:var(--ink);border-color:var(--accent)}
nav .spacer{flex:1}
.tg{background:var(--panel2);border:1px solid var(--line);color:var(--muted);border-radius:6px;
  padding:4px 10px;font-size:13px;cursor:pointer;font-family:inherit}
h1,h2,h3,h4{line-height:1.35;margin:0 0 .5em}
h1{font-size:32px;letter-spacing:.01em}
h2{font-size:21px;margin-top:2em;padding-bottom:.35em;border-bottom:1px solid var(--line)}
h3{font-size:17px;margin-top:1.6em}
p{margin:.7em 0}
small,.small{font-size:13px;color:var(--muted)}
.muted{color:var(--muted)}
.hero{padding:52px 0 26px}
.hero h1{font-size:38px;max-width:22em}
.hero p.lead{font-size:17px;color:var(--muted);max-width:44em}
.stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));gap:12px;margin:26px 0 8px}
.stat{background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:14px 16px;box-shadow:var(--shadow)}
.stat b{display:block;font-size:26px;line-height:1.2}
.stat span{font-size:12.5px;color:var(--muted)}
.card{background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:16px 18px;box-shadow:var(--shadow)}
.grid{display:grid;gap:14px}
.g2{grid-template-columns:repeat(auto-fit,minmax(320px,1fr))}
.g3{grid-template-columns:repeat(auto-fit,minmax(250px,1fr))}
table{width:100%;border-collapse:collapse;font-size:14px;margin:.8em 0}
th,td{text-align:left;padding:8px 10px;border-bottom:1px solid var(--line);vertical-align:top}
th{background:var(--panel2);font-weight:600;font-size:13.5px;white-space:nowrap}
tbody tr:hover{background:var(--panel2)}
.tag{display:inline-block;font-size:12px;padding:2px 8px;border-radius:20px;border:1px solid var(--line2);
  color:var(--muted);background:var(--panel2);white-space:nowrap}
.dot{display:inline-block;width:9px;height:9px;border-radius:50%;margin-right:6px;vertical-align:1px}
a.case{display:block;text-decoration:none;color:inherit;border:1px solid var(--line);border-radius:10px;
  background:var(--panel);padding:15px 17px;box-shadow:var(--shadow);transition:transform .12s}
a.case:hover{transform:translateY(-2px);border-color:var(--line2)}
a.case h3{margin:.2em 0 .3em;font-size:17.5px}
a.case .meta{font-size:12.5px;color:var(--muted);display:flex;gap:10px;flex-wrap:wrap;align-items:center}
a.case p{margin:.5em 0 0;font-size:14px;color:var(--muted)}
.layout{display:grid;grid-template-columns:minmax(0,1fr) 310px;gap:26px;align-items:start;margin-top:18px}
@media(max-width:900px){.layout{grid-template-columns:1fr}.hero h1{font-size:28px}}
aside{position:sticky;top:70px}
aside .box{background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:14px 16px;margin-bottom:14px}
aside h4{margin:0 0 .5em;font-size:14px;letter-spacing:.05em;color:var(--muted);text-transform:uppercase}
ol.steps{counter-reset:s;list-style:none;padding:0;margin:.6em 0}
ol.steps li{position:relative;padding:10px 0 10px 44px;border-bottom:1px dashed var(--line)}
ol.steps li:last-child{border-bottom:0}
ol.steps li:before{counter-increment:s;content:counter(s);position:absolute;left:0;top:10px;width:28px;height:28px;
  border-radius:50%;background:var(--panel2);border:1px solid var(--line2);display:flex;align-items:center;
  justify-content:center;font-size:13px;color:var(--muted)}
ul.tick{list-style:none;padding:0;margin:.5em 0}
ul.tick li{padding:6px 0 6px 20px;border-bottom:1px dashed var(--line);position:relative}
ul.tick li:before{content:"";position:absolute;left:2px;top:15px;width:7px;height:7px;border-radius:2px;background:var(--accent);opacity:.6}
ul.tick li:last-child{border-bottom:0}
.note{background:var(--panel2);border-left:3px solid var(--accent);padding:12px 15px;border-radius:0 8px 8px 0;margin:1em 0;font-size:14px}
.warn{background:var(--panel2);border-left:3px solid #b4574f;padding:12px 15px;border-radius:0 8px 8px 0;margin:1em 0;font-size:14px}
.kv{display:grid;grid-template-columns:auto 1fr;gap:6px 12px;font-size:13.5px}
.kv dt{color:var(--muted);white-space:nowrap}
.kv dd{margin:0}
.src{font-size:13px;color:var(--muted)}
.src li{margin:.35em 0;word-break:break-all}
footer{border-top:1px solid var(--line);margin-top:60px;padding:26px 0 40px;color:var(--muted);font-size:13px}
input.f{width:100%;padding:9px 12px;border:1px solid var(--line2);border-radius:8px;background:var(--panel);
  color:var(--ink);font-family:inherit;font-size:14px;margin-bottom:14px}
.tl{position:relative;padding-left:22px}
.tl:before{content:"";position:absolute;left:6px;top:6px;bottom:6px;width:2px;background:var(--line2)}
.tl .it{position:relative;padding:0 0 18px 8px}
.tl .it:before{content:"";position:absolute;left:-20px;top:8px;width:11px;height:11px;border-radius:50%;
  background:var(--bg);border:2px solid var(--accent)}
.tl .it b{font-size:15px}
.tl .it .when{font-size:12.5px;color:var(--accent);font-weight:600}
.anchor{display:block;height:60px;margin-top:-60px;visibility:hidden}
"""


def js_toggle():
    return """
(function(){var t=localStorage.getItem('gmtheme');if(t)document.documentElement.setAttribute('data-theme',t);
else if(matchMedia('(prefers-color-scheme:dark)').matches)document.documentElement.setAttribute('data-theme','dark');})();
function toggleTheme(){var c=document.documentElement.getAttribute('data-theme')==='dark'?'light':'dark';
document.documentElement.setAttribute('data-theme',c);localStorage.setItem('gmtheme',c);}
"""


def page(title, body, active='', root='', extra=''):
    nav_items = [('index.html', '总览', 'index'), ('principles.html', '原理', 'principles'),
                 ('cases/index.html', '实例', 'cases'), ('field.html', '野外判定', 'field'),
                 ('timeline.html', '时间轴', 'timeline'), ('sources.html', '来源', 'sources')]
    links = ''.join(
        f'<a href="{root}{u}" class="{"on" if a==active else ""}">{n}</a>' for u, n, a in nav_items)
    return f"""<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{E(title)}</title>
<meta name="description" content="基于《{E(BOOK['title'])}》（{E(BOOK['author'])}）重构的地貌学现场手册：11 类营力原理 + 14 个中国现存实例 + 野外判定对照。">
<style>{css()}</style></head><body>
<script>{js_toggle()}</script>
<nav><div class="wrap">
<a class="brand" href="{root}index.html">地貌现场手册</a>
<div class="links">{links}</div><div class="spacer"></div>
<button class="tg" onclick="toggleTheme()">明 / 暗</button>
</div></nav>
<main class="wrap">{body}</main>
<footer><div class="wrap">
<p>内容依据：{E(BOOK['author'])}《{E(BOOK['title'])}》（{BOOK['pages']} 页，{BOOK['chapters']} 章，{BOOK['toc_entries']} 条目录条目，OCR：{E(BOOK['ocr'])}），
实例数据来自公开来源，逐条标注出处。</p>
<p>本站为读书笔记性质的二次整理，非教材替代品。所有冲突数据并列呈现、不作换算；无来源的数字不写入。</p>
</div></footer>
{extra}
</body></html>"""


def agent_tag(aid):
    a = AGENT_D[aid]
    return f'<span class="tag"><span class="dot" style="background:{a[3]}"></span>{E(a[1])}</span>'


def build_index():
    st = [('17', '原书章数'), ('11', '营力系统'), (str(len(CASES)), '现存实例'),
          ('6', '易混淆对照'), (str(len(TIMELINE)), '时间锚点')]
    stats = ''.join(f'<div class="stat"><b>{a}</b><span>{b}</span></div>' for a, b in st)

    remap = ''.join(
        f'<tr><td>{E(a)}</td><td>{E(b)}</td><td><a href="{c}">打开 →</a></td></tr>' for a, b, c in REMAP)

    cards = ''
    for c in CASES:
        a = AGENT_D[c['agent']]
        cards += f'''<a class="case" href="cases/{c['slug']}.html" data-agent="{c['agent']}" data-name="{E(c['name'])}">
<h3>{E(c['name'])}</h3>
<div class="meta"><span class="dot" style="background:{a[3]}"></span>{E(a[1])}<span>·</span><span>{E(c['place'][:22])}</span></div>
<p>{E(c['sub'])}</p></a>'''

    filt = ''.join(f'<option value="{a[0]}">{E(a[1])}</option>' for a in AGENTS)

    body = f'''
<section class="hero">
<h1>把一本书，拆成 {len(CASES)} 个能去的地方</h1>
<p class="lead">《{E(BOOK['title'])}》按学科体系写成：先基本问题，后分论各营力，再讲中国第四纪与研究方法。
这套结构适合上课，不适合"我要去看"。本站把它<b>重构</b>为三层：营力原理（为什么会这样）→ 现存实例（去哪里看、看什么数字）→ 野外判定（怎么认、怎么防认错）。
每个实例都给出可核对的实测数据与出处，冲突数据并列不合并。</p>
<div class="stats">{stats}</div>
</section>

<h2 id="how">重构逻辑：从章节顺序到问题顺序</h2>
<div class="grid g3">
<div class="card"><h3>① 原理层</h3><p class="muted">把 17 章压缩为 11 类营力系统，每类回答四个问题：控制变量是什么、作用过程如何推进、留下什么产物、野外怎么认。</p></div>
<div class="card"><h3>② 实例层</h3><p class="muted">{len(CASES)} 个中国境内现存的、可到达的地点。每处给出坐标、实测数字、现场观察清单、成因机制链与争议点。</p></div>
<div class="card"><h3>③ 判定层</h3><p class="muted">把最容易被认错的 {len(CONFUSIONS)} 组地貌/堆积物做成对照表 —— 冰碛还是泥石流、风成还是水成、构造沉降还是人为沉降。</p></div>
</div>

<h2>原书章节 → 本站模块</h2>
<table><thead><tr><th>原书位置</th><th>本站对应</th><th></th></tr></thead><tbody>{remap}</tbody></table>

<h2>营力 × 实例</h2>
<table><thead><tr><th>营力系统</th><th>原书章节</th><th>控制变量</th><th>实例</th></tr></thead><tbody>
{''.join(f'<tr><td><span class="dot" style="background:{a[3]}"></span>{E(a[1])}</td><td class="small">{E(a[2])}</td>'
         f'<td class="small">{E(a[4])}</td><td class="small">' +
         ('、'.join(f'<a href="cases/{c["slug"]}.html">{E(c["name"])}</a>' for c in CASES if c['agent'] == a[0]) or '—') +
         '</td></tr>' for a in AGENTS)}
</tbody></table>

<h2 id="cases">全部实例</h2>
<input class="f" id="q" placeholder="输入关键词或地点筛选…">
<select class="f" id="fa"><option value="">全部营力</option>{filt}</select>
<div class="grid g3" id="cl">{cards}</div>
<p class="small" id="none" style="display:none">没有匹配的实例。</p>
'''
    js = '''<script>
var q=document.getElementById('q'),fa=document.getElementById('fa'),
cs=[].slice.call(document.querySelectorAll('#cl a.case')),none=document.getElementById('none');
function run(){var k=q.value.trim().toLowerCase(),a=fa.value,n=0;
cs.forEach(function(el){var ok=(!k||el.textContent.toLowerCase().includes(k))&&(!a||el.dataset.agent===a);
el.style.display=ok?'':'none';if(ok)n++;});none.style.display=n?'none':'';}
q.addEventListener('input',run);fa.addEventListener('change',run);
</script>'''
    return page('地貌现场手册 · 总览', body, 'index', extra=js)


def build_principles():
    blocks = ''
    for aid, name, chap, color, ctrl in AGENTS:
        rel = [c for c in CASES if c['agent'] == aid]
        rel_links = '、'.join(f'<a href="cases/{c["slug"]}.html">{E(c["name"])}</a>' for c in rel) or '—'
        blocks += f'''<div class="card" style="border-left:4px solid {color}">
<h3 id="{aid}"><span class="dot" style="background:{color}"></span>{E(name)}</h3>
<p class="small muted">{E(chap)}</p>
<dl class="kv"><dt>控制变量</dt><dd>{E(ctrl)}</dd>
<dt>关键过程</dt><dd>{E(ctrl.split('。')[0])}。作用强度由上述变量共同决定，任一变量改变，产物随之改变。</dd>
<dt>典型产物</dt><dd>{E('、'.join(c['name'] for c in rel)) if rel else '见实例页'}</dd>
<dt>代表实例</dt><dd>{rel_links}</dd></dl>
</div>'''
    body = f'''
<section class="hero"><h1>原理：营力、过程与产物</h1>
<p class="lead">原书第一、二、三章讲"地貌是什么"：地貌形态是内外地质营力相互作用的结果 —— 内力给出骨架与高差，外力按各自的规律去削、去搬、去堆。
本页把全书分论各章归纳为 11 类营力系统，每类只回答四件事：控制变量、作用过程、留下的产物、野外怎么认。</p></section>

<h2>底层框架</h2>
<div class="grid g2">
<div class="card"><h3>内力 vs 外力</h3><p>内力（构造、火山）制造高差与格局，是"舞台"；外力（风化、流水、冰川、风、海浪）削平高差，是"演员"。
地貌是二者当前比值的快照 —— 抬升快于剥蚀则山长高，反之则被削平。</p></div>
<div class="card"><h3>成因 → 形态 → 年代</h3><p>看一个地貌，要回答三个问题：什么营力造的（成因）、现在长什么样（形态）、什么时候造的（年代）。
三者缺一，解释就不完整。庐山之争的实质，正是"形态"无法单独裁定"成因"。</p></div>
<div class="card"><h3>相对等级与分带</h3><p>地貌有规模等级：大地貌（山系、盆地）→ 中地貌（谷地、扇体）→ 小地貌（冲沟、沙丘）。
同时具有气候分带性与垂直分带性 —— 同一营力在不同气候带的表现可以完全不同。</p></div>
<div class="card"><h3>时间是隐藏变量</h3><p>速率 × 时间 = 结果。青藏铁路冻土段是毫米每年，若尔盖泥炭是 0.6 毫米每年，黄河三角洲是公里每年。
做解释之前先算量级，很多"不可能"其实是"时间不够"。</p></div>
</div>

<h2>11 类营力系统</h2>
<div class="grid g2">{blocks}</div>

<h2>怎么用这套框架读一处地方</h2>
<ol class="steps">
<li><b>先定营力</b>：眼前的形态，可能是几种营力接力或叠加的结果（如黄河三角洲 = 河流供沙 + 海洋改造 + 人类干预）。</li>
<li><b>再找控制变量</b>：把"为什么会这样"翻译成"哪个变量变了"。桂林峰林与峰丛的差别，追到最后是地下水位深浅。</li>
<li><b>然后问年代</b>：形态相似不等于同时形成。五大连池 14 座火山，最老 200 万年、最新 300 年，摆在同一个视野里。</li>
<li><b>最后做排除</b>：列出所有能造成相似形态的成因，逐条排除。冰碛还是泥石流、构造还是人为，靠的都是这一步。</li>
</ol>
<div class="note">本站所有"原理"表述以原书章节体系为骨架，数据全部来自实例页标注的公开来源；凡无来源的数字一律不写。</div>
'''
    return page('原理 · 营力与过程', body, 'principles')


def build_case(c):
    a = AGENT_D[c['agent']]
    facts = ''.join(f'<tr><th>{E(k)}</th><td><b>{E(v)}</b><br><span class="small muted">{E(n)}</span></td></tr>'
                    for k, v, n in c['facts'])
    obs = ''.join(f'<li>{E(x)}</li>' for x in c['observe'])
    mech = ''.join(f'<li>{E(x)}</li>' for x in c['mech'])
    mean = ''.join(f'<tr><th>{E(k)}</th><td>{E(v)}</td></tr>' for k, v in c['meaning'])
    rel = ''.join(f'<li><a href="{s}.html">{E(next(x["name"] for x in CASES if x["slug"] == s))}</a></li>'
                  for s in c['related'])
    src = ''.join(f'<li><a href="{E(u)}" target="_blank" rel="noopener">{E(t)}</a></li>' for t, u in c['sources'])
    body = f'''
<div style="padding-top:22px">
<div class="small muted"><a href="../index.html">总览</a> · <a href="index.html">实例</a> · {agent_tag(c['agent'])}</div>
<h1 style="margin:.2em 0 .1em">{E(c['name'])}</h1>
<p class="lead muted" style="font-size:17px;margin:0 0 1em">{E(c['sub'])}</p>
<div class="meta" style="display:flex;gap:8px;flex-wrap:wrap;margin-bottom:6px">
<span class="tag">{E(a[1])}</span><span class="tag">{E(a[2])}</span><span class="tag">{E(c['status'])}</span></div>
<p>{E(c['summary'])}</p>
</div>
<div class="layout">
<div>
<h2>现场能看到什么</h2><ul class="tick">{obs}</ul>
<h2>背后的原理</h2><ol class="steps">{mech}</ol>
<h2>这些数字在说什么</h2><table><tbody>{mean}</tbody></table>
<h2>实测数据</h2><table><tbody>{facts}</tbody></table>
<h2>争议与口径</h2><div class="warn">{E(c['dispute'])}</div>
<h2>来源</h2><ul class="src">{src}</ul>
</div>
<aside>
<div class="box"><h4>位置</h4><p style="margin:0;font-size:14px">{E(c['place'])}</p>
<p class="small muted" style="margin:.5em 0 0">{E(c['coord'])}</p></div>
<div class="box"><h4>可达性</h4><p style="margin:0;font-size:14px">{E(c['access'])}</p></div>
<div class="box"><h4>状态</h4><p style="margin:0;font-size:14px">{E(c['status'])}</p></div>
<div class="box"><h4>相关实例</h4><ul style="margin:0;padding-left:18px;font-size:14px">{rel}</ul></div>
<div class="box"><h4>原书对应</h4><p style="margin:0;font-size:14px">{E(a[2])}</p></div>
</aside>
</div>
'''
    return page(f"{c['name']} · 实例", body, 'cases', root='../')


def build_cases_index():
    rows = ''
    for c in CASES:
        a = AGENT_D[c['agent']]
        rows += (f'<tr><td><a href="{c["slug"]}.html"><b>{E(c["name"])}</b></a></td>'
                 f'<td><span class="dot" style="background:{a[3]}"></span>{E(a[1])}</td>'
                 f'<td class="small">{E(c["place"])}</td>'
                 f'<td class="small">{E(c["facts"][0][1])}</td>'
                 f'<td class="small">{E(c["status"])}</td></tr>')
    body = f'''
<section class="hero"><h1>现存实例索引</h1>
<p class="lead">{len(CASES)} 处中国境内现存的、可到达的地点，按营力系统归类。每处都给出坐标、实测数字、现场观察清单、成因机制链、争议口径与来源。
"关键数字"列取该实例第一组实测数据，仅作快速对照，完整数据见各页。</p></section>
<h2>一览表</h2>
<table><thead><tr><th>实例</th><th>营力</th><th>位置</th><th>关键数字</th><th>状态</th></tr></thead><tbody>{rows}</tbody></table>
<h2>卡片</h2>
<div class="grid g3">{''.join(f'<a class="case" href="{c["slug"]}.html"><h3>{E(c["name"])}</h3>'
                              f'<div class="meta">{agent_tag(c["agent"])}</div><p>{E(c["sub"])}</p></a>' for c in CASES)}</div>
'''
    return page('实例索引', body, 'cases', root='../')


def build_field():
    conf = ''
    for name, two, tip in CONFUSIONS:
        conf += f'''<div class="card" style="margin-bottom:14px">
<h3>{E(name)}</h3>
<table><thead><tr><th style="width:50%">A</th><th style="width:50%">B</th></tr></thead>
<tbody><tr><td>{E(two[0])}</td><td>{E(two[1])}</td></tr></tbody></table>
<div class="note"><b>判定要点：</b>{E(tip)}</div></div>'''
    body = f'''
<section class="hero"><h1>野外判定：怎么认，怎么防认错</h1>
<p class="lead">原书第十七章讲研究方法。这里把它压缩成可直接带到现场的东西：一组易混淆对照表，加一份通用的观察顺序。
核心原则只有一句 —— <b>形态相似的成因未必相同，孤立的证据不足以定案</b>。</p></section>

<h2>{len(CONFUSIONS)} 组最容易认错的地貌与堆积物</h2>
{conf}

<h2>通用观察顺序</h2>
<ol class="steps">
<li><b>远看形态</b>：整体轮廓、规模、与周边地形的关系。先定等级 —— 这是大地貌还是小地貌？</li>
<li><b>近看物质</b>：粒度、分选、磨圆、层理、胶结程度。堆积物的"手感"往往比形态更可靠。</li>
<li><b>找接触关系</b>：与下伏、上覆地层是整合还是不整合？切割还是被切割？这是定年代的免费信息。</li>
<li><b>量方向</b>：砾石长轴定向、斜层理倾向、擦痕方向、河谷走向 —— 方向里藏着古水流与古应力。</li>
<li><b>记空间组合</b>：孤立的形态多解，成组出现才有诊断意义（冰斗 + U 谷 + 终碛才是冰川）。</li>
<li><b>最后问年代</b>：能测年就测，不能测就用相对年代（阶地级序、风化程度、覆盖关系）。</li>
</ol>

<h2>测量与记录的最小工具集</h2>
<table><thead><tr><th>工具</th><th>解决什么问题</th><th>本站实例中的应用</th></tr></thead><tbody>
<tr><td>罗盘 + 测距</td><td>产状、方向、厚度</td><td>判断砾石定向、岩层产状、断层走向</td></tr>
<tr><td>卷尺 / 标尺</td><td>粒度、层厚、位移量</td><td>量沙丘落沙坡、泥炭剖面、滑坡台阶</td></tr>
<tr><td>GPS / 手机定位</td><td>点位与高程</td><td>记录剖面坐标（如宣城 30°52′24″N，118°51′55″E）</td></tr>
<tr><td>遥感影像 + 地形图</td><td>区域格局与变化速率</td><td>黄河三角洲 1976—2020 岸线变迁、冰川末端变化</td></tr>
<tr><td>重复观测（照片定点）</td><td>变化速率</td><td>海螺沟退缩、冻土路基沉降、沙丘移动</td></tr>
<tr><td>年代学手段</td><td>定年与对比</td><td>古地磁（泥河湾、网纹红土）、¹⁴C（洛川、泥炭）</td></tr>
</tbody></table>

<div class="note">方法页的价值不在"记住这些表"，而在养成一个习惯：<b>看到形态先想还能怎么形成</b>。这才是从"认得"到"判得准"的分界线。</div>
'''
    return page('野外判定', body, 'field')


def build_timeline():
    items = ''
    for when, what, desc, aid in TIMELINE:
        a = AGENT_D[aid]
        items += f'''<div class="it"><div class="when">{E(when)}</div><b>{E(what)}</b>
<div class="small muted"><span class="dot" style="background:{a[3]}"></span>{E(a[1])}</div>
<div style="font-size:14px">{E(desc)}</div></div>'''
    body = f'''
<section class="hero"><h1>时间轴：从 258 万年前到今天</h1>
<p class="lead">第四纪的核心不是"很久以前"，而是"气候反复摆动"。这条时间轴把全书第四纪部分与本站实例串起来：
每个锚点都有对应的实地可看之处。</p></section>
<h2>锚点</h2>
<div class="tl">{items}</div>
<div class="note">年代的口径时有差异（如第四纪下限有 2.58 Ma 与 1.8 Ma 等不同方案，本站采用通行口径之一），
泥河湾最早层位是否达到 200 万年亦在讨论中。凡存争议处，本站并列呈现而不取单值。</div>
'''
    return page('时间轴', body, 'timeline')


def build_sources():
    rows = ''
    for c in CASES:
        for t, u in c['sources']:
            rows += f'<tr><td>{E(c["name"])}</td><td><a href="{E(u)}" target="_blank" rel="noopener">{E(t)}</a></td></tr>'
    body = f'''
<section class="hero"><h1>来源清单</h1>
<p class="lead">本站所有实测数字均来自以下公开来源，共 {sum(len(c['sources']) for c in CASES)} 条。
采集方式：以原书章节为线索逐类联网检索，优先采用期刊论文、政府部门、景区官方与主流媒体的实测数据；
同一指标出现多个数值时并列呈现，不做加权或换算。</p></section>
<h2>按实例</h2>
<table><thead><tr><th style="width:150px">实例</th><th>来源</th></tr></thead><tbody>{rows}</tbody></table>
<h2>底本</h2>
<table><tbody>
<tr><th>书名</th><td>{E(BOOK['title'])}</td></tr>
<tr><th>作者</th><td>{E(BOOK['author'])}</td></tr>
<tr><th>规模</th><td>{BOOK['pages']} 页，{BOOK['chapters']} 章，{BOOK['toc_entries']} 条目录条目</td></tr>
<tr><th>文字层</th><td>{E(BOOK['ocr'])}（扫描件原图未做任何重压缩或替换）</td></tr>
</tbody></table>
<div class="warn"><b>说明：</b>书中参考文献页在原扫描件中即已截断（书内第 374 页仅存 1 页），这是原件缺页，非处理引入。
本站实例数据不依赖该参考文献，全部另采公开来源。</div>
'''
    return page('来源清单', body, 'sources')


def main():
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    os.makedirs(os.path.join(OUT, 'cases'), exist_ok=True)

    def w(p, s):
        open(os.path.join(OUT, p), 'w', encoding='utf-8').write(s)

    w('index.html', build_index())
    w('principles.html', build_principles())
    w('field.html', build_field())
    w('timeline.html', build_timeline())
    w('sources.html', build_sources())
    w('cases/index.html', build_cases_index())
    for c in CASES:
        w(f"cases/{c['slug']}.html", build_case(c))
    open(os.path.join(OUT, '.nojekyll'), 'w').write('')
    print('pages:', 6 + len(CASES), 'cases:', len(CASES),
          'sources:', sum(len(c['sources']) for c in CASES))


if __name__ == '__main__':
    main()
