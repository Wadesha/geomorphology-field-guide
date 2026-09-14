# -*- coding: utf-8 -*-
"""地貌现场手册（全国版）—— 静态站点生成器
用法：python build_site.py   输出至 ./docs（GitHub Pages 目录）
数据与渲染分离：本文件只负责把 site_data.py 渲染成 docs/index.html。

版式：单页标签式（与淮海站同款）。顶排短名卡片切换模块，实例模块内有第二排
地点短名卡片；正文是连续散文，数字逐条标注来源，冲突口径并列不合并。
"""
import os, html
from site_data import (AGENTS, CASES, CONFUSIONS, TIMELINE)

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, 'docs')
AGENT_D = {a[0]: a for a in AGENTS}
E = html.escape

MODULES = [('cases', '实例'), ('prins', '原理'), ('field', '判定'),
           ('time', '时间轴'), ('srcs', '来源'), ('home', '总览')]

# 每处实例的卡片短名（顶排卡片空间有限，只放 2—4 字）
SHORT = {
    'luochuan-loess': '洛川', 'badain-jaran': '巴丹吉林', 'hailuogou-glacier': '海螺沟',
    'lushan-glacier-debate': '庐山之争', 'qinghai-tibet-permafrost': '青藏冻土',
    'guilin-fenglin': '桂林', 'yellow-river-delta': '黄河口', 'yongdinghe-fan': '永定河扇',
    'xintan-landslide': '新滩滑坡', 'fenwei-graben': '汾渭地堑', 'nihewan': '泥河湾',
    'wudalianchi-volcano': '五大连池', 'xuancheng-red-earth': '网纹红土',
    'zoige-peatland': '若尔盖',
}


def short(c):
    return SHORT.get(c['slug'], c['name'][:3])


def css():
    return """
*{box-sizing:border-box}
:root{
  --bg:#fbfaf7; --panel:#f6f3ed; --ink:#23201c; --muted:#6b6459; --line:#e3ddd1;
  --rule:#d3cbbd; --accent:#8a6d3b; --accent-soft:#f1ead9;
}
html[data-theme=dark]{
  --bg:#15171a; --panel:#1e2126; --ink:#e9e6e0; --muted:#9b948a; --line:#2c3036;
  --rule:#3b4046; --accent:#c9a86a; --accent-soft:#2e2a20;
}
body{margin:0;background:var(--bg);color:var(--ink);
  font-family:"Songti SC","Source Han Serif SC","Noto Serif CJK SC",Georgia,"PingFang SC","Microsoft YaHei",serif;
  font-size:15px;line-height:1.62;-webkit-font-smoothing:antialiased}
a{color:inherit;text-decoration:none;border-bottom:1px solid var(--rule)}
a:hover{color:var(--accent);border-color:var(--accent)}
.wrap{max-width:960px;margin:0 auto;padding:0 18px}
nav{position:sticky;top:0;z-index:50;background:var(--bg);border-bottom:1px solid var(--line);
  padding-bottom:5px}
.topbar{max-width:1000px;margin:0 auto;display:flex;align-items:center;gap:14px;height:38px;padding:0 18px;flex-wrap:wrap}
.topbar .brand{font-weight:700;font-size:14.5px;white-space:nowrap;border:0;letter-spacing:.02em}
.topbar .spacer{flex:1}
.tg{background:none;border:1px solid var(--line);color:var(--muted);border-radius:5px;
  padding:2px 8px;font-size:12px;cursor:pointer;font-family:inherit}
.cards{max-width:1000px;margin:0 auto;padding:1px 18px 0;display:flex;gap:5px;flex-wrap:wrap}
.cards button{font-family:inherit;font-size:13px;line-height:1.3;color:var(--muted);
  background:var(--panel);border:1px solid var(--line);border-radius:7px;
  padding:3px 10px;cursor:pointer;transition:all .12s ease}
.cards button:hover{color:var(--accent);border-color:var(--accent)}
.cards button.on{color:var(--accent);border-color:var(--accent);background:var(--accent-soft);font-weight:700}
.cards.sub{padding-top:5px}
.cards.sub button{font-size:12.5px;padding:2px 8px;border-radius:6px}
.view{display:none}
.view.on{display:block}
.casebody{display:none}
.casebody.on{display:block}
main{padding-bottom:10px}
.hero{padding:16px 0 4px}
h1{font-size:23px;line-height:1.3;margin:0 0 .3em;letter-spacing:.01em}
h2{font-size:17.5px;line-height:1.35;margin:1.15em 0 .5em;padding-bottom:.25em;border-bottom:1px solid var(--line)}
h3{font-size:15.5px;line-height:1.4;margin:.95em 0 .3em}
h4{font-size:14.5px;margin:.8em 0 .25em}
p{margin:0 0 .55em;text-indent:2em;text-align:justify}
p.lead,p.kicker,p.plain{text-indent:0}
p.lead{color:var(--muted);font-size:15px;line-height:1.6;margin-bottom:.7em}
p.kicker{font-size:12.5px;color:var(--muted);margin-bottom:.25em}
p.plain{color:var(--muted);font-size:13.5px}
.small{font-size:13px;color:var(--muted)}
p.ref{font-size:13px;text-indent:0;color:var(--muted);line-height:1.5;word-break:break-word}
p.ref a{border-bottom-style:dotted}
footer{border-top:1px solid var(--line);margin-top:24px;padding:14px 0 26px;color:var(--muted);font-size:12.5px}
footer .wrap{max-width:960px}
footer p{text-indent:0;line-height:1.6}
"""


def js():
    return """
(function(){var t=localStorage.getItem('gmtheme');if(t)document.documentElement.setAttribute('data-theme',t);
else if(matchMedia('(prefers-color-scheme:dark)').matches)document.documentElement.setAttribute('data-theme','dark');})();
function toggleTheme(){var c=document.documentElement.getAttribute('data-theme')==='dark'?'light':'dark';
document.documentElement.setAttribute('data-theme',c);localStorage.setItem('gmtheme',c);}
var CASES=%s;
function route(){
  var h=decodeURIComponent(location.hash.replace(/^#\\/?/,''));
  var view='cases',caso=null;
  if(h.slice(0,2)==='c/'){view='cases';caso=h.slice(2);}
  else if(h) view=h;
  if(!document.getElementById('v-'+view)) view='cases';
  if(view==='cases'&&(caso===null||CASES.indexOf(caso)<0)) caso=CASES[0];
  var vs=document.querySelectorAll('.view');
  for(var i=0;i<vs.length;i++) vs[i].classList.remove('on');
  document.getElementById('v-'+view).classList.add('on');
  var bs=document.querySelectorAll('.cards[data-k=mod] button');
  for(var j=0;j<bs.length;j++) bs[j].classList.toggle('on',bs[j].getAttribute('data-v')===view);
  var cs=document.querySelectorAll('.cards[data-k=case] button');
  for(var k=0;k<cs.length;k++) cs[k].classList.toggle('on',cs[k].getAttribute('data-c')===caso);
  document.getElementById('casebar').style.display=(view==='cases')?'flex':'none';
  var cts=document.querySelectorAll('.casebody');
  for(var m=0;m<cts.length;m++) cts[m].classList.remove('on');
  if(view==='cases'){
    var el=document.getElementById('case-'+caso);
    if(el) el.classList.add('on');
  }
  window.scrollTo(0,0);
}
window.addEventListener('hashchange',route);
route();
""" % json_dumps([c['slug'] for c in CASES])


def json_dumps(arr):
    return '[' + ','.join('"%s"' % a for a in arr) + ']'


def shell(body):
    mod_cards = ''
    for k, n in MODULES:
        cls = ' class="on"' if k == 'cases' else ''
        dest = 'c/' if k == 'cases' else k
        mod_cards += (f'<button data-v="{k}"{cls} '
                      f'onclick="location.hash=\'{dest}\'">{E(n)}</button>')
    case_cards = ''.join(
        f'<button data-c="{c["slug"]}" onclick="location.hash=\'c/{c["slug"]}\'">{E(short(c))}</button>'
        for c in CASES)
    return f"""<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>地貌现场手册</title>
<meta name="description" content="地貌现场手册：{len(AGENTS)} 类营力原理 + {len(CASES)} 个中国现存实例 + 野外判定对照。">
<style>{css()}</style></head><body>
<nav>
<div class="topbar"><span class="brand">地貌现场手册</span><span class="spacer"></span>
<button class="tg" onclick="toggleTheme()">明 / 暗</button></div>
<div class="cards" data-k="mod">{mod_cards}</div>
<div class="cards sub" data-k="case" id="casebar" style="display:flex">{case_cards}</div>
</nav>
<main>{body}</main>
<footer><div class="wrap">
<p>本站数据来自公开来源并逐条标注出处；同一指标的多个口径一律并列呈现、不作换算；凡查不到来源的数字一概不写。这是读书笔记性质的二次整理，实地情况请以现场为准。</p>
</div></footer>
<script>{js()}</script>
</body></html>"""


def case_links(cs, sep='、'):
    return sep.join(f'<a href="#c/{c["slug"]}">{E(short(c))}</a>' for c in cs)


# ─────────────────────────────────────────── 总览

def body_home():
    nsrc = sum(len(c['sources']) for c in CASES)

    agents = ''
    for a in AGENTS:
        rel = [c for c in CASES if c['agent'] == a[0]]
        tail = (f'全国范围内归入这一类的实例有{case_links(rel)}。'
                if rel else '这一类暂无选入的实例，把它保留在原理层，是为了读别处的地方时不缺参照。')
        agents += f'<h3>{E(a[1])}</h3>\n<p>{E(a[4])}{tail}</p>\n'

    return f'''
<section class="hero wrap">
<h1>中国大地上，{len(CASES)} 处能亲手核对的现场</h1>
<p class="lead">这是一份给实地用的地貌指南：把中国常见的地貌现象归成 {len(AGENTS)} 类营力，每类落到几处现存、可到达的具体地点；每处都给出坐标与可达性、现场观察要点、成因机制、实测数字与来源，实例与数据全部来自公开来源。</p>
<p>{len(CASES)} 处地点从黄土高原铺到南海之滨、从青藏冻土带到东北火山群；所有实测数字出自 {nsrc} 条公开来源，逐条标注出处；同一指标的多个口径并列呈现，不换算、不取单值；查不到来源的数字一概不写。</p>
</section>

<div class="wrap">
<h2>{len(AGENTS)} 类营力与它们的实例</h2>
{agents}
<p class="plain">说明：营力分类是为方便查阅而作的归纳，同一处地貌常是几种营力接力或叠加的结果，分类不构成对成因的排他判断。</p>
</div>
'''


# ─────────────────────────────────────────── 原理

def body_prins():
    frames = [
        ('内力与外力',
         '内力（构造运动、火山活动）制造高差与格局，是「舞台」；外力（风化、流水、冰川、风、海浪）削平高差，是「演员」。地貌是二者当前比值的快照——抬升快于剥蚀则山长高，反之则被削平。青藏高原是内力搭台、冰川与流水登场的样本，华北平原则是外力铺了千万年的成品。'),
        ('成因、形态与年代',
         '看一处地貌，要回答三个问题：什么营力造成的（成因）、现在长什么样（形态）、什么时候造成的（年代）。三者缺一，解释就不完整。庐山之争的实质，正是「形态」无法单独裁定「成因」。'),
        ('规模等级与地域分带',
         '地貌是有等级的：大地貌如山系、盆地、高原，中地貌如谷地、扇体、湖盆，小地貌如冲沟、沙丘、溶洞。同一营力在不同气候带的表现可以完全不同——同为风成堆积，北方铺成黄土高原，南方却混进了湿热风化的网纹红土。'),
        ('时间是隐藏变量',
         '速率乘以时间等于结果。青藏铁路冻土段是毫米每年，若尔盖泥炭是零点六毫米每年，黄河三角洲造陆最快时是每年几十平方公里。动手解释之前先算量级，很多看似「不可能」的现象，其实只是「时间不够」。'),
    ]
    fr = ''.join(f'<h3>{E(t)}</h3>\n<p>{E(d)}</p>\n' for t, d in frames)

    blocks = ''
    for aid, name, chap, color, ctrl in AGENTS:
        rel = [c for c in CASES if c['agent'] == aid]
        tail = (f'这一类的实例是{case_links(rel)}。'
                if rel else '这一类暂无选入的实例，把它保留在原理层，是为了读别处的地方时不缺参照。')
        blocks += f'<h3 id="{aid}">{E(name)}</h3>\n<p>{E(ctrl)}{tail}</p>\n'

    return f'''
<section class="hero wrap">
<h1>原理：营力、过程与产物</h1>
<p class="lead">地貌形态是内外地质营力相互作用的结果：内力给出骨架与高差，外力按各自的规律去削、去搬、去堆。本页把 {len(AGENTS)} 类营力各讲一节，每节只回答四件事：控制变量、作用过程、留下的产物、野外怎么认。</p>
</section>

<div class="wrap">
<h2>读地貌的四条底层框架</h2>
{fr}

<h2>{len(AGENTS)} 类营力系统</h2>
{blocks}

<h2>怎么用这套框架读一处地方</h2>
<p>先定营力：眼前的形态，多半是几种营力接力或叠加的结果，比如黄河三角洲等于河流供沙加海洋改造，再叠上人工改道与调水调沙。再找控制变量：把「为什么会这样」翻译成「哪个变量变了」——桂林峰林与峰丛的差别，追到最后是地下水位的深浅。然后问年代：形态相似不等于同时形成，五大连池十四座火山，最老二百万年、最新三百年，摆在同一个视野里。最后做排除：列出所有能造成相似形态的成因，逐条排除，冰碛还是泥石流、构造沉降还是人为沉降，靠的都是这一步。</p>
<p>本页的原理表述是通用的地貌学结论；实例数据全部来自各处标注的公开来源，凡无来源的数字一律不写。原理与实例之间不是一一对应关系：一类营力可以解释多处地点，一处地点也常常需要几类营力合起来解释。</p>
</div>
'''


# ─────────────────────────────────────────── 实例

# 现场观察段的开篇导语：按营力分别措辞，避免 14 个实例用同一句话开头
OBS_LEAD = {
    'weathering': '风化剖面现场，先看颜色与结构的变化，再用手感分辨风化强度的分带。',
    'slope': '斜坡灾害现场，看陡崖、裂缝与堆积体，重点在它们的接触关系与规模。',
    'fluvial': '流水地貌现场，先看地面高低，再看土质的粗细与分选，然后找水流方向的证据。',
    'karst': '岩溶现场，看岩性、溶蚀痕迹，以及山体与水面、地下水位之间的关系。',
    'glacial': '冰川现场，看冰体、冰碛与植被演替的次序，重点在「正在变化」的痕迹。',
    'periglacial': '冻土现场，看工程措施与地基的对应关系，再看地表变形的痕迹。',
    'aeolian': '风沙现场，先看颗粒粗细与层理，再看植被与水分条件，最后判断沙的来路。',
    'coastal': '海岸现场，看河海两股力量留下的分带，以及岸线正在向哪个方向推进。',
    'lacustrine': '沼泽现场，看「水与地面」的关系：积水多深、排水多慢、底下攒的是什么。',
    'tectonic': '构造现场，找直线状的地形痕迹、地面错台的走向，以及形变速率的量级。',
    'quaternary': '地层现场，看剖面的厚薄与层数，再问每一层对应多长的时间。',
}


def coord_clause(coord):
    """coord 字段有时是经纬度、有时是尺度数据，按内容决定怎么起句，避免出现「坐标总面积…」。"""
    txt = E(coord)
    if '°' in coord:
        sep = '' if coord.rstrip().endswith(('。', '；')) else '。'
        return f'坐标{txt}{sep}'
    if coord.rstrip().endswith(('。', '；')):
        return txt
    return f'{txt}。'


def case_inner(c):
    a = AGENT_D[c['agent']]
    name = E(c['name'])

    obs = E(OBS_LEAD.get(c['agent'], '到了现场，以下几处值得逐一对照。')) + ''.join(E(x) for x in c['observe'])
    mech = ''.join(E(x) for x in c['mech'])
    mean = ''.join(f'{E(k)}，{E(v)}。' for k, v in c['meaning'])
    facts = ''.join(f'{E(k)}，{E(v)}——{E(n)}。' for k, v, n in c['facts'])
    srcs = '；'.join(f'<a href="{E(u)}" target="_blank" rel="noopener">{E(t)}</a>'
                    for t, u in c['sources'])
    rel = '、'.join(f'<a href="#c/{s}">{E(short(next(x for x in CASES if x["slug"] == s)))}</a>'
                    for s in c['related'])
    nsrc = len(c['sources'])
    nfact = len(c['facts'])

    sec = []
    sec.append(f'<p class="kicker">{E(a[1])} · {name}</p>')
    sec.append(f'<h1>{name}</h1>')
    sec.append(f'<p class="lead">{E(c["sub"])}</p>')
    sec.append(f'<p>{name}地处{E(c["place"])}。{coord_clause(c["coord"])}成因上归入{E(a[1])}一类。它的现状是：{E(c["status"])}。到现场去，{E(c["access"])}</p>')
    sec.append(f'<p>{E(c["summary"])}</p>')

    sec.append('<h2>现场能看到什么</h2>')
    sec.append(f'<p>{obs}</p>')

    sec.append('<h2>背后的原理</h2>')
    sec.append(f'<p>{mech}</p>')

    if c['meaning']:
        sec.append('<h2>这些数字在说什么</h2>')
        sec.append(f'<p>{mean}</p>')

    if c['facts']:
        sec.append('<h2>实测数据</h2>')
        sec.append(f'<p>{facts}</p>')

    if c['dispute']:
        sec.append('<h2>争议与口径</h2>')
        sec.append(f'<p>{E(c["dispute"])}</p>')

    sec.append('<h2>来源</h2>')
    sec.append(f'<p class="ref">本页数据出自 {nsrc} 条公开来源：{srcs}。</p>')
    sec.append(f'<p class="ref">相邻的实例还有{rel}，点顶排短名卡片即可切过去看。</p>')
    sec.append(f'<p class="plain">以上观察点与数字均取自公开来源，未做现场复核；实地情况会随季节、水位与工程进展变化，出发前请再核对一次。本页共 {nfact} 组实测数据，全部标注来源。</p>')

    return '\n'.join(sec)


def body_cases():
    intro = (f'<section class="hero wrap"><h1>{len(CASES)} 处现存实例</h1>'
             f'<p class="lead">下面一排短名卡片就是 {len(CASES)} 处中国境内现存、可到达的地点；'
             f'点哪张，下面就出现哪一处的完整内容——坐标与可达性、现场观察要点、成因机制链、'
             f'实测数字、争议口径与来源，一处一页式地摊开。再点顶排其他卡片，随时离开。</p></section>')
    cases = ''.join(
        f'<div class="casebody wrap" id="case-{c["slug"]}">{case_inner(c)}</div>'
        for c in CASES)
    return intro + cases


# ─────────────────────────────────────────── 野外判定

def body_field():
    conf = ''
    for name, two, tip in CONFUSIONS:
        pair = [x.strip() for x in name.split('/')]
        a1 = pair[0] if pair else name
        a2 = pair[1] if len(pair) > 1 else '另一种成因'
        lead2 = '再说另外两种' if len(pair) > 2 else f'再说{a2}'
        conf += (f'<h3>{E(name)}</h3>\n'
                 f'<p>先说{E(a1)}。{E(two[0])}。{lead2}。{E(two[1])}。{E(tip)}</p>\n')

    order = [
        ('远看形态', '先看整体轮廓、规模，以及它与周边地形的关系，定下等级：这是大地貌还是小地貌。'),
        ('近看物质', '看粒度、分选、磨圆、层理与胶结程度。堆积物的「手感」往往比形态更可靠。'),
        ('找接触关系', '与下伏、上覆地层是整合还是不整合，是谁切割谁。这是几乎免费的定年信息。'),
        ('量方向', '砾石长轴定向、斜层理倾向、擦痕方向、断裂走向，方向里藏着古水流与古应力。'),
        ('记空间组合', '孤立的形态多半多解，成组出现才有诊断意义——冰斗、U 谷、终碛凑齐了才谈得上冰川。'),
        ('最后问年代', '能测年就测年，不能测年就用相对年代，比如阶地级序、风化程度、覆盖关系。'),
    ]
    od = ''.join(f'<b>{E(t)}</b>，{E(d)}' for t, d in order)

    tools = (
        '罗盘加测距，解决产状、方向与厚度的问题，本站实例里用来量砾石定向、岩层产状与断裂走向；'
        '卷尺与标尺，解决粒度、层厚与位移量，用来量洛川剖面的分层厚度、沙丘的高度与滑坡台阶的高差；'
        'GPS 或手机定位，解决点位与高程的记录，比如宣城网纹红土剖面这类必须写清坐标的采样点；'
        '遥感影像加地形图，解决区域格局与变化速率，黄河三角洲近五十年的岸线变迁、海螺沟冰川末端的后退都靠它；'
        '定点重复拍照，解决变化速率，冰川退缩、冻土路基沉降、沙丘移动都属这一类；'
        '年代学手段，解决定年与对比，古地磁用在泥河湾与网纹红土，碳十四用在洛川与泥炭剖面。'
    )

    return f'''
<section class="hero wrap">
<h1>野外判定：怎么认，怎么防认错</h1>
<p class="lead">这是一份可以直接带到现场的判定手册：{len(CONFUSIONS)} 组高发的易混淆对照，加一份通用的观察顺序。核心原则只有一句——形态相似的成因未必相同，孤立的证据不足以定案。</p>
</section>

<div class="wrap">
<h2>{len(CONFUSIONS)} 组最容易认错的地貌与堆积物</h2>
{conf}

<h2>通用观察顺序</h2>
<p>{od}</p>
<p>这六步的顺序不是随意的：先形态、后物质，是因为形态容易被第一印象带偏；把年代放在最后，是因为前面五步收集到的信息本身就是定年的材料。反过来做，最常见的后果是先入为主——看到泥砾混杂就断定是冰碛，看到地面开裂就断定是构造活动。</p>

<h2>测量与记录的最小工具集</h2>
<p>{tools}</p>

<h2>这套方法的边界</h2>
<p>方法页的价值不在于记住这些条目，而在于养成一个习惯：看到形态，先想它还能怎么形成。这才是从「认得」走到「判得准」的分界线。同时也要承认，判定需要相应条件——没有测年手段时，很多结论只能停在相对先后；没有区域资料时，孤立一点的观察很容易被局部现象误导。本站的实例都标出了数据来源，凡有争议的都并列双方口径，正是出于这个理由。</p>
</div>
'''


# ─────────────────────────────────────────── 时间轴

def body_time():
    # 每个锚点后接一句短评：按营力分组、组内按出现次序轮换措辞，避免同一句式反复出现
    PH = {
        'quaternary': ['第四纪的时钟，从这里开始走字',
                       '人类的脚印，在华北反复出现',
                       '时间尺度跨了三个数量级，摆在同一条线上'],
        'weathering': ['南方的湿热风化，就此留下最厚的一笔'],
        'glacial': ['冰川的进退，把山地重新雕了一遍',
                    '同一处山地，两派学者读出了两个故事',
                    '冰川的争论，至今没有落幕'],
        'lacustrine': ['水慢下来之后，泥炭开始一年一年地攒',
                       '古湖贯通，草原沼泽就此铺开'],
        'coastal': ['入海口再挪一次位置，岸线跟着改口',
                    '又一次改道，把造陆的账本翻开新的一页'],
        'slope': ['一场滑坡，把地貌过程的量级写进了新闻'],
        'periglacial': ['冻土从认识对象变成了工程对象'],
        'karst': ['这片山水，拿到了国际地质学界的入场券'],
    }
    seen = {}
    items = ''
    for when, what, desc, aid in TIMELINE:
        v = PH.get(aid)
        if not v:
            phrase = '中国的地貌面貌在这一步发生变化'
        else:
            i = seen.get(aid, 0)
            phrase = v[i] if i < len(v) else v[-1]
            seen[aid] = i + 1
        items += f'<p><b>{E(when)}</b>，{E(what)}——{E(desc)}。{E(phrase)}。</p>\n'

    return f'''
<section class="hero wrap">
<h1>时间轴：从 258 万年前到今天</h1>
<p class="lead">第四纪的核心不是「很久以前」，而是「气候反复摆动」。这条时间轴把本站 {len(TIMELINE)} 个锚点串起来：构造运动以百万年计，水系改道以百年计，工程活动以十年计——每一个锚点，都能在实地找到落点。</p>
</section>

<div class="wrap">
<h2>{len(TIMELINE)} 个时间锚点</h2>
{items}

<h2>年代口径的处理</h2>
<p>年代的口径常有差异，读起来要留意它究竟指什么。第四纪下限就有 258 万年与 180 万年等不同方案，本站采用通行口径之一；泥河湾最早文化层是否逼近 200 万年，涉及「早期人类何时走出非洲」的重大命题，学界对年代精度保持高度要求。凡遇此类情形，本站一律并列呈现而不取单值，也不代为换算。</p>
<p>另需说明，时间轴上的次序只表示先后关系，不表示等间隔。构造运动以百万年计，冰期旋回以十万年计，历史文献记载以百年计，把它们放在同一条线上，尺度差距是被压缩过的。</p>
</div>
'''


# ─────────────────────────────────────────── 来源

def body_srcs():
    blocks = ''
    for c in CASES:
        srcs = '；'.join(f'<a href="{E(u)}" target="_blank" rel="noopener">{E(t)}</a>' for t, u in c['sources'])
        blocks += (f'<h3><a href="#c/{c["slug"]}">{E(c["name"])}</a>　{E(c["place"])}</h3>\n'
                   f'<p class="ref">{len(c["sources"])} 条：{srcs}。</p>\n')

    nsrc = sum(len(c['sources']) for c in CASES)
    return f'''
<section class="hero wrap">
<h1>来源清单</h1>
<p class="lead">本站所有实测数字都出自下列公开来源，共 {nsrc} 条，按实例排列。采集方式是按营力类别逐类联网检索，优先采用期刊论文、政府部门、景区官方与主流媒体的实测数据；同一指标出现多个数值时并列呈现，不做加权也不做换算。</p>
</section>

<div class="wrap">
<h2>按实例分列</h2>
{blocks}

<h2>使用边界</h2>
<p>本站的营力框架是通用地貌学的归纳，实例与数据全部来自上列公开来源；同一指标的多个口径并列呈现，不作换算，也不代人取舍。学术争议只列双方论据与出处，本站不作裁决。</p>
<p>最后一点提醒：这些来源多为机构发布或媒体报道，其中的数字经二次转述，与原始论文口径可能有出入；本站只保证「在此处如此陈述」，不代人判断其权威程度。需要引用于正式场合时，请回到原始文献核对。</p>
</div>
'''


def main():
    # 注意：不要用 shutil.rmtree（本机沙箱会把它改写成回收站操作并失败）。
    # 改为「就地覆盖 + 只清掉本次不再产出的多余文件」。
    body = ''.join(
        f'<section class="view" id="v-{k}">{b}</section>'
        for k, b in [('home', body_home()), ('prins', body_prins()),
                     ('cases', body_cases()), ('field', body_field()),
                     ('time', body_time()), ('srcs', body_srcs())])
    pages = {'index.html': shell(body)}

    # 清理旧产物中不在本次清单内的文件（逐个删除，失败不影响构建）
    stale = []
    for dp, dn, fn in os.walk(OUT):
        for f in fn:
            rel = os.path.relpath(os.path.join(dp, f), OUT).replace('\\', '/')
            if rel not in pages and rel != '.nojekyll':
                stale.append(os.path.join(dp, f))
    for p in stale:
        try:
            os.remove(p)
        except OSError:
            pass

    for rel, s in pages.items():
        with open(os.path.join(OUT, rel), 'w', encoding='utf-8') as fh:
            fh.write(s)
    open(os.path.join(OUT, '.nojekyll'), 'w').write('')
    if stale:
        print('removed stale:', len(stale))
    print('pages: 1 (single-page tabs)  cases:', len(CASES),
          'sources:', sum(len(c['sources']) for c in CASES))


if __name__ == '__main__':
    main()
