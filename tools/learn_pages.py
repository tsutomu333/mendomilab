#!/usr/bin/env python3
"""解説ページ（learn）を作る。python3 tools/learn_pages.py"""
import json, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

GTAG=next(l for l in open('/home/claude/mendomilab/about/index.html').read().split('\n') if 'G-SGX5EJT1CN' in l)

def page(lang, path, rel, title, desc, h1, body, faq, crumbs, alt, og=None):
    ld = [{"@context": "https://schema.org", "@type": "Article", "headline": h1,
           "inLanguage": lang, "author": {"@type": "Person", "name": "Tsutomu Takagi" if lang == 'en' else "高木 務"},
           "publisher": {"@type": "Organization", "name": "Mendomi Lab"},
           "datePublished": "2026-11-23", "mainEntityOfPage": "https://mendomilab.com/" + path},
          {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
              {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]},
          {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
              {"@type": "ListItem", "position": i + 1, "name": n, "item": u} for i, (n, u) in enumerate(crumbs)]}]
    faq_html = ''.join(f'<h3>{q}</h3>\n<p>{a}</p>\n' for q, a in faq)
    if lang == 'ja':
        top = rel + 'ja/'
        nav = (f'<a href="{top}#games">ゲーム</a><a href="{top}consult/">相談する</a>'
               f'<a href="{top}about/">Mendomi Labについて</a><a class="lang" href="{rel}{alt or ""}" hreflang="en">English</a>')
        foot = (f'<div><a href="{top}about/">Mendomi Labについて</a><a href="{top}consult/">相談する</a>'
                f'<a href="{top}privacy/">プライバシー</a><a href="{top}tokushoho/">特定商取引法にもとづく表記</a></div>\n'
                '  <div>Mendomi Lab は A&amp;T Works のプロジェクトです</div>\n'
                '  <div>© 2026 Mendomi Lab. トヨタ自動車株式会社・株式会社OJTソリューションズとは関係ありません。</div>')
        faqh = 'よくある質問'
    else:
        top = rel
        nav = (f'<a href="{top}#games">Games</a><a href="{top}consult/">Work with me</a>'
               f'<a href="{top}about/">About</a><a class="lang" href="{rel}{alt or "ja/"}" hreflang="ja">日本語</a>')
        foot = (f'<div><a href="{top}about/">About</a><a href="{top}consult/">Work with me</a>'
                f'<a href="{top}privacy/">Privacy</a></div>\n'
                '  <div>Mendomi Lab is a project of A&amp;T Works</div>\n'
                '  <div>© 2026 Mendomi Lab. Not affiliated with Toyota Motor Corporation or OJT Solutions Inc.</div>')
        faqh = 'Questions'
    crumb_html = ' › '.join([f'<a href="{rel}{u.split("mendomilab.com/")[1]}">{n}</a>' for n, u in crumbs[:-1]] + [crumbs[-1][0]])
    en_url, ja_url = (path, alt) if lang == 'en' else (alt, path)
    alts = (f'<link rel="alternate" hreflang="en" href="https://mendomilab.com/{en_url}">\n'
            f'<link rel="alternate" hreflang="ja" href="https://mendomilab.com/{ja_url}">\n') if alt else ''
    html = f'''<!DOCTYPE html>
<html lang="{lang}">
<head>
{GTAG}
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<link rel="icon" href="{rel}favicon.svg" type="image/svg+xml">
<meta name="description" content="{desc}">
<link rel="canonical" href="https://mendomilab.com/{path}">
{alts}<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="https://mendomilab.com/{path}">
<meta property="og:type" content="article">
<meta property="og:image" content="https://mendomilab.com/assets/social/{og or ('og_ja_sp' if lang == 'ja' else 'og_sp')}.png">
<meta name="twitter:card" content="summary_large_image">
<link rel="stylesheet" href="{rel}assets/site.css">
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
</head>
<body>
<header class="site"><div class="wrap">
  <a class="logo" href="{top}"><span class="mark">面</span><span class="name">Mendomi<small>Lab</small></span></a>
  <nav>{nav}</nav>
</div></header>

<main class="wrap prose">
  <p class="crumb" style="font-size:.85em;opacity:.7">{crumb_html}</p>
  <h1>{h1}</h1>
{body}
<h2>{faqh}</h2>
{faq_html}</main>

<footer class="site"><div class="wrap">
  {foot}
</div></footer>
</body>
</html>
'''
    out = os.path.join(ROOT, path, 'index.html')
    os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out, 'w').write(html)
    print('wrote', path)


# ---------- 日本語：平準化とは ----------
JA_BODY = '''  <p class="lead"><b>平準化とは 造る量と種類を 日ごと・時間ごとにならして造ることです。</b>同じものを何日もまとめて造るのではなく 毎日 少しずついろいろな種類を造ります。トヨタ生産方式（TPS）の土台の1つで <a href="../kanban/">ジャストインタイムとかんばん</a>は 平準化ができていることが前提になっています。</p>

<h2>数字で見る平準化の例</h2>
<p>1週間（5日）で100台を造る工場があるとします。内訳は A車60台 B車20台 C車20台です。</p>
<table><thead><tr><th></th><th>月</th><th>火</th><th>水</th><th>木</th><th>金</th></tr></thead><tbody>
<tr><td>まとめて造る</td><td>A 20</td><td>A 20</td><td>A 20</td><td>B 20</td><td>C 20</td></tr>
<tr><td>平準化して造る</td><td>A12 B4 C4</td><td>A12 B4 C4</td><td>A12 B4 C4</td><td>A12 B4 C4</td><td>A12 B4 C4</td></tr>
</tbody></table>
<p>1日の台数はどちらも20台です。ちがうのは 種類の組み合わせです。平準化では 1日の中の順番もならして「A B A C A」を4回くり返すように造ります。</p>
<p>これは<b>種類の平準化</b>です。もう1つ<b>量の平準化</b>もあります。注文が 月40 火20 水10 木20 金10台とばらついても 毎日20台ずつ造る計画にします。月曜日に足りない分は 完成品の在庫や納期の調整で受け止めます。</p>
<h2>平準化ポスト（ヘイジュンカボックス）の例</h2>
<p>平準化ポストは かんばんを入れる棚です。横に時間の枠 縦に種類がならびます。上の例で1日8時間に20台なら 1台あたり24分です。24分ごとの枠に A B A C A の順でかんばんを1枚ずつ入れ 運ぶ人が24分ごとに1枚ずつ取り出して工程に届けます。こうすると工程には 波ではなく一定のペースで仕事が届きます。</p>

<h2>なぜ平準化するのか：困るのは前の工程とサプライヤー</h2>
<p>完成車の工場だけを見ると まとめて造るほうが楽に見えます。段取り替え（造る種類の切りかえ）が週に2回ですむからです。</p>
<p>でも B車にしか使わない部品を造るサプライヤーから見ると話がかわります。</p>
<ul>
<li><b>まとめて造る</b>：木曜日に20台分が一度に必要で ほかの日は0台。木曜日に間に合わせるには 20台分を1日で造れる人と設備を持つか 木曜日までに造りためて在庫を持つなどの対応がいります。</li>
<li><b>平準化して造る</b>：毎日4台分ずつ。1日に造れる量は4台分あれば足ります（まとめて造るときの5分の1）。造りためる在庫も小さくできます。</li>
</ul>
<p>つまり まとめて造ると 前の工程とサプライヤーに「いちばん忙しい日に合わせた人と設備」か「在庫」のコストを押しつけることになります。このコストは 最後には部品の値段にのって お客様の側にもどってきます。</p>
<p>トヨタではこれを ムラ（ばらつき）がムリ（無理な負荷）につながり ムリがムダ（使わない人と設備・在庫）につながる と説明します。現場ではムダ・ムラ・ムリの3つをまとめて「ダラリ」（ム<b>ダ</b>・ム<b>ラ</b>・ム<b>リ</b>）と呼ぶこともあります。平準化は 生産計画のムラを小さくする手段です。</p>

<h2>平準化と標準化の違い</h2>
<table><thead><tr><th></th><th>平準化</th><th>標準化</th></tr></thead><tbody>
<tr><td>ならすもの</td><td>造る量と種類（いつ 何を 何台）</td><td>作業のやり方（だれが どの順で どう作業するか）</td></tr>
<tr><td>目的</td><td>前の工程やサプライヤーの負荷を一定に近づける</td><td>よいやり方をそろえて 品質と作業時間のばらつきを小さくし 改善の基準にする</td></tr>
<tr><td>TPSでの例</td><td>平準化ポスト（ヘイジュンカボックス） 混流生産</td><td>標準作業 標準作業票</td></tr>
</tbody></table>
<p>言葉は似ていますが ならす対象がちがいます。ただし つながってもいます。毎日同じ量と組み合わせで造れると 作業も標準にしやすくなります。</p>

<h2>現場でよくある誤解</h2>
<ol>
<li><b>「お客様の注文をならすこと」ではない</b>：注文の波はなくせません。ならすのは自社の<b>造る順番</b>です。注文の波は 完成品の在庫や 納期の調整などで受け止めます。</li>
<li><b>段取り替えを短くしないとできない</b>：毎日すべての種類を造るので 切りかえの回数がふえます。段取り替えの時間を短くすることと 平準化はセットです。</li>
<li><b>量の平準化と種類の平準化は別</b>：月ごとに全体の量が大きくかわるときは 1日に造る台数とタクトタイム（稼働時間を必要な台数で割った 1台あたりの時間）を見直します。種類の平準化だけでは吸収できません。</li>
</ol>

<h2>平準化を体験してみる</h2>
<p>平準化のよさは 説明を聞くより 自分で順番を変えてコストが動くのを見るほうがわかります。<a href="../../games/supplier/">サプライヤーのパズル</a>は トヨタの生産を題材にした架空の例で 組み立ての順番を変えると 2つのサプライヤーの人 設備 在庫のコストがどう変わるかを見る無料のブラウザゲームです。研修で使うと「このコストを決めたのはサプライヤー？ それともトヨタ？」という問いから話が深まります。</p>
<p><a class="btn primary" href="../../play/supplier/">無料で遊ぶ</a><a class="btn ghost" href="../../games/supplier/">ゲームの説明を見る</a></p>
<p>7つのムダの中でいちばん悪いと言われる造りすぎについては <a href="../tsukurisugi-no-muda/">造りすぎのムダとは？</a> にまとめています。</p>

<h2>書いた人</h2>
<p>高木 務（Mendomi Lab）。トヨタの子会社のコンサル会社で20年以上 トヨタの現場で長く働いた人たちと組んで 30社以上の工場の改善をしてきました。研修や職場への導入の相談は <a href="../../consult/">相談する</a> からどうぞ。</p>
'''
JA_FAQ = [
    ("平準化とは何ですか？", "造る量と種類を 日ごと・時間ごとにならして造ることです。同じものを何日もまとめて造らず 毎日少しずついろいろな種類を造ります。トヨタ生産方式の土台の1つです。"),
    ("平準化と標準化の違いは何ですか？", "平準化がならすのは造る量と種類（いつ 何を 何台）です。標準化がそろえるのは作業のやり方（だれが どの順で どう作業するか）です。"),
    ("平準化のメリットは何ですか？", "前の工程とサプライヤーの負荷が一定に近づき いちばん忙しい日に合わせた人と設備や 造りためる在庫を小さくできます。そのコストが下がることが いちばん大きなメリットです。"),
    ("平準化ポスト（ヘイジュンカボックス）とは何ですか？", "かんばんを 時間の枠ごとに 決めた種類の順番で入れておく棚です。決まった時間ごとに取り出して工程に届け 造る順番と量をならします。"),
]

# ---------- 英語：heijunka examples ----------
EN_BODY = '''  <p class="lead"><b>Heijunka means leveling both the volume and the mix of what you build, day by day and hour by hour.</b> Instead of running one model for days and then switching, you build a little of each model every day. It is one of the foundations of the Toyota Production System — just-in-time and kanban assume it is in place. Below are concrete heijunka examples with numbers.</p>

<h2>Example 1: a week of production, batched vs. leveled</h2>
<p>A plant builds 100 units a week over 5 days: 60 of model A, 20 of B and 20 of C.</p>
<table><thead><tr><th></th><th>Mon</th><th>Tue</th><th>Wed</th><th>Thu</th><th>Fri</th></tr></thead><tbody>
<tr><td>Batched</td><td>A 20</td><td>A 20</td><td>A 20</td><td>B 20</td><td>C 20</td></tr>
<tr><td>Leveled (heijunka)</td><td>A12 B4 C4</td><td>A12 B4 C4</td><td>A12 B4 C4</td><td>A12 B4 C4</td><td>A12 B4 C4</td></tr>
</tbody></table>
<p>Both plans build 20 units a day. Only the mix changes. Within the day, the leveled plan repeats the sequence <b>A B A C A</b> four times. This is <b>mix leveling</b>.</p>
<p><b>Volume leveling</b> is the other half. Even if orders arrive as 40, 20, 10, 20 and 10 units across the week, you still plan 20 a day and cover Monday's shortfall with finished-goods stock or adjusted delivery dates.</p>

<h2>Example 2: what the supplier sees</h2>
<p>Seen from the final assembly line, batching looks easier: only two changeovers a week. Now look at a supplier that makes a part used only on model B.</p>
<ul>
<li><b>Batched:</b> it needs 20 sets on Thursday and zero on the other days. To be ready, it must either keep enough people and machines to make 20 sets in one day, or build them ahead by Thursday and hold the stock.</li>
<li><b>Leveled:</b> it needs 4 sets every day. Daily capacity for 4 sets is enough — one fifth of the batched peak — and much less stock is built ahead.</li>
</ul>
<p>Batching pushes cost upstream — capacity for the peak or inventory — and that cost comes back in the part price. Toyota explains it as <b>mura</b> (unevenness) creating <b>muri</b> (overburden), which creates <b>muda</b> (waste: idle people and machines, inventory). Heijunka reduces the mura in the production plan itself.</p>

<h2>Example 3: the heijunka box</h2>
<p>A heijunka box (leveling box) is a rack of slots: one column per time interval and one row per model. In Example 1, 20 units in an 8-hour day means one unit every 24 minutes. Use 24-minute columns and one card per unit, and place the cards in the A, B, A, C, A rows across five columns, repeated four times — 12 A, 4 B and 4 C a day. A material handler collects one column every 24 minutes and delivers it to the process, so work arrives at a steady pace instead of in waves. (In practice a slot often holds several cards, one per container.)</p>

<h2>Example 4: outside the factory</h2>
<ul>
<li><b>A bakery</b> that bakes every bread type in small rounds through the morning, instead of all baguettes at 6 a.m., can spread the load on ovens and staff and restock shelves more often.</li>
<li><b>An office team</b> that processes a few of every request type each day, instead of all invoices on Monday, can spread its workload more evenly through the week.</li>
</ul>
<p>These are simplified illustrations, but the principle is the same: smooth the mix so the people and resources behind you see a more even load.</p>

<h2>Common misunderstandings</h2>
<ol>
<li><b>It is not leveling customer demand.</b> You cannot remove the waves in orders. You level <em>your build sequence</em> and absorb the waves with finished-goods stock, adjusted lead times or both.</li>
<li><b>It needs short changeovers.</b> Building every model every day means more changeovers. Reducing changeover time (SMED) and heijunka go together.</li>
<li><b>Volume leveling and mix leveling are different.</b> If total monthly volume changes a lot, revisit the daily production rate and the takt time (available time divided by required units). Leveling the mix alone cannot absorb that.</li>
</ol>

<h2>Try heijunka yourself</h2>
<p>Heijunka is easier to understand when you change the build order yourself and see how costs change. <a href="../../games/suppliers-puzzle/">The Supplier's Puzzle</a> is a free browser game set in a fictional scenario inspired by Toyota production: you run two suppliers, change the build order, and see how staffing, equipment and inventory costs change. In a workshop it opens one powerful question: <em>"Who chose this cost — the supplier or Toyota?"</em></p>
<p><a class="btn primary" href="https://ttmtkg.itch.io/the-suppliers-puzzle">Play free</a><a class="btn ghost" href="https://mendomilab.gumroad.com/l/supplier-puzzle-pro">Pro for trainers ($49)</a></p>
<p>See all our <a href="../lean-simulation-games/">lean simulation games for training</a>.</p>

<h2>How to run it in a 30-minute session</h2>
<ol>
<li><b>Round 1:</b> build in big batches — one model for days, then the next. Write down the staffing, equipment and inventory costs.</li>
<li><b>Round 2:</b> change only the build order to a leveled mix. Keep everything else the same.</li>
<li><b>Compare:</b> put the two results side by side and ask who chose each cost.</li>
</ol>
<h2>What to look for on a real floor</h2>
<ul>
<li>The monthly total is stable, but the daily schedule swings a lot. That gap is where leveling helps.</li>
<li>Overtime on some days and idle people on others.</li>
<li>Upstream processes or suppliers keeping extra stock "in case the big order comes".</li>
<li>Long changeovers. Leveling the mix needs short changeovers, so they are usually the first thing to work on.</li>
</ul>

<h2>About the author</h2>
<p>Tsutomu Takagi (Mendomi Lab). For more than 20 years I worked at a consulting company that is a Toyota subsidiary, teaming up with people who spent long careers on Toyota's shop floors and improving more than 30 factories. If you want help bringing these ideas into your training or workplace, <a href="../../consult/">get in touch</a>.</p>
'''
EN_FAQ = [
    ("What is a simple heijunka example?", "A plant that builds 60 A, 20 B and 20 C in a week can run A for three days, then B, then C — or build 12 A, 4 B and 4 C every day in the sequence A B A C A. The second plan is heijunka."),
    ("What is the difference between heijunka and leveling?", "They are the same idea. Heijunka is the Japanese term used in the Toyota Production System for leveling production volume and mix."),
    ("What does a heijunka box do?", "It holds kanban cards in slots by time interval and model, in the leveled order, so work is released to the line at a steady pace."),
    ("How is heijunka related to mura, muri and muda?", "Uneven schedules (mura) overburden people and machines (muri), which leads to waste such as idle capacity and inventory (muda). Heijunka reduces that unevenness in the plan itself."),
]

EN9_BODY = """
<p class="lead"><b>Mendomi (面倒見, <i>mendōmi</i>) is a Japanese word for looking after people.</b> At work it means a leader or senior who takes care of the people around them, at work and beyond, until trust grows to the point where people think, "For this boss, I'll go the extra mile." On Toyota-style shop floors it is a quality people expect from a good leader.</p>

<h2>The word, piece by piece</h2>
<table>
<thead><tr><th>Part</th><th>Reading</th><th>Meaning</th></tr></thead>
<tbody>
<tr><td>面倒</td><td>mendō</td><td>trouble, bother, the work of caring for someone</td></tr>
<tr><td>見</td><td>mi</td><td>to look, to watch over</td></tr>
<tr><td>面倒見がいい</td><td>mendōmi ga ii</td><td>"good at looking after people" (a common compliment)</td></tr>
</tbody>
</table>
<p>So <em>mendomi</em> literally means taking on the bother of watching over someone. It is not the same as being kind or soft. A leader with good mendomi will also tell you clearly when something is wrong, because they care how you grow.</p>

<h2>Mendomi in the Toyota Production System</h2>
<p>The Toyota Way has two pillars: <b>continuous improvement</b> and <b>respect for people</b>. Mendomi is how respect for people looks on the shop floor, day to day:</p>
<ul>
<li>A team leader notices a new member struggling and stays with them until they can do the job.</li>
<li>A supervisor asks "why?" with the team instead of blaming the person when a problem appears.</li>
<li>A senior teaches the reason behind a standard, not only the steps.</li>
<li>A manager checks how people are doing outside work too, because life affects work.</li>
</ul>
<p>Lean tools such as kanban, 5S and standardized work only last when people trust their leaders enough to stop the line, report problems and suggest improvements. That trust is built through mendomi.</p>

<h2>Why it matters for lean programs</h2>
<p>Many lean programs copy the tools and stop there. Working for more than 20 years alongside people who led Toyota shop floors, I came to feel that the real source of their strength was mendomi: leaders who develop people one by one. When that is missing, improvements fade once the consultant leaves.</p>

<h2>How to practice mendomi as a leader</h2>
<ol>
<li><b>Watch</b>: go to where the work happens and see each person, not only the numbers.</li>
<li><b>Stay</b>: when someone is stuck, stay with them until they can do it themselves.</li>
<li><b>Explain why</b>: share the reason behind each rule so people can improve it.</li>
<li><b>Follow up</b>: come back the next day and the next week. Care that stops after one talk is not mendomi.</li>
</ol>

<h2>Try lean thinking in a game</h2>
<ul>
<li><a href="../../games/overproduction-factory/">Overproduction Factory</a>: feel why building too much loses money.</li>
<li><a href="../../games/suppliers-puzzle/">The Supplier's Puzzle</a>: feel why level production (heijunka) helps your supplier.</li>
</ul>
<p>Related: <a href="../lean-vs-toyota-production-system/">Lean vs Toyota Production System</a> / <a href="../7-wastes-of-lean/">7 wastes of lean</a> / <a href="../../about/">About Mendomi Lab</a></p>
"""
EN9_FAQ = [
    ("What does mendomi mean?", "Mendomi (面倒見) is a Japanese word for looking after people. At work it means a leader or senior who cares for and develops the people around them until they trust each other."),
    ("How do you pronounce mendomi?", "men-doh-mee. The middle o is long: mendōmi."),
    ("Is mendomi a Toyota term?", "It is an everyday Japanese word, not a Toyota trademark. On Toyota-style shop floors it is a quality people expect from good leaders, and it is how the Toyota Way pillar of respect for people shows up day to day."),
    ("Is mendomi the same as being kind?", "No. A leader with good mendomi also tells you clearly when something is wrong, because they care about how you grow."),
]

if __name__ == '__main__':
    page('ja', 'ja/learn/heijunka/', '../../../',
         '平準化とは？わかりやすく解説｜標準化との違いとトヨタの例｜Mendomi Lab',
         '平準化とは 造る量と種類を日ごとにならして造ること。数字の例で まとめて造るとサプライヤーに何が起きるか 標準化との違い 現場でよくある誤解を トヨタの子会社のコンサル会社で20年以上改善をしてきた人が説明します。',
         '平準化とは？ わかりやすく解説（標準化との違いとトヨタの例）', JA_BODY, JA_FAQ,
         [("Mendomi Lab", "https://mendomilab.com/ja/"), ("平準化とは", "https://mendomilab.com/ja/learn/heijunka/")],
         'learn/heijunka-examples/')
    page('en', 'learn/heijunka-examples/', '../../',
         'Heijunka Examples with Numbers | Mendomi Lab',
         "Heijunka (production leveling) examples with numbers: a leveled weekly schedule, a supplier's view, and a heijunka box. Try it in a free browser game.",
         'Heijunka examples: production leveling in real life, with numbers', EN_BODY, EN_FAQ,
         [("Mendomi Lab", "https://mendomilab.com/"), ("Heijunka examples", "https://mendomilab.com/learn/heijunka-examples/")],
         'ja/learn/heijunka/')


# ---------- 日本語：造りすぎのムダ ----------
JA2_BODY = '''  <p class="lead"><b>造りすぎのムダとは お客様が必要とする量より多く または必要なときより早く造ることです。</b>トヨタ生産方式の「7つのムダ」の1つで その中でもいちばん悪いムダと言われます。ほかのムダを生み しかもかくしてしまうからです。</p>

<h2>7つのムダ</h2>
<table><thead><tr><th>ムダ</th><th>どんなことか</th></tr></thead><tbody>
<tr><td><b>造りすぎのムダ</b></td><td>必要より多く 早く造る</td></tr>
<tr><td>手待ちのムダ</td><td>材料や前の工程を待って 手が止まる</td></tr>
<tr><td>運搬のムダ</td><td>必要以上に運ぶ 置きかえる</td></tr>
<tr><td>加工そのもののムダ</td><td>お客様の価値にならない加工や手間</td></tr>
<tr><td>在庫のムダ</td><td>材料 仕掛品 完成品が必要以上にある</td></tr>
<tr><td>動作のムダ</td><td>探す かがむ 歩くなど 価値を生まない動き</td></tr>
<tr><td>不良をつくるムダ</td><td>不良品と その手直し</td></tr>
</tbody></table>

<h2>なぜ造りすぎがいちばん悪いのか</h2>
<p>造りすぎると ほかのムダが次々に出てきます。</p>
<ul>
<li><b>在庫のムダ</b>：造った分は置いておくしかありません。</li>
<li><b>運搬のムダ</b>：置き場に運び また取りに行きます。</li>
<li><b>動作のムダ</b>：山の中から必要なものを探します。</li>
<li><b>不良が見つかるのが遅れる</b>：工程のあいだに在庫があると 前の工程で出た不良が後の工程で見つかるまで時間がかかります。そのあいだに同じ不良を造り続けることがあります。</li>
</ul>
<p>そしていちばんこわいのは <b>手待ちのムダがかくれる</b>ことです。本当は人や機械が余っていても 造り続けているので 全員が忙しく見えます。どこに余力があるのか だれにも見えなくなります。</p>

<h2>数字で見る造りすぎ</h2>
<p>1日の注文が480台 稼働時間が480分の工場では タクトタイム（お客様の注文で決まる速さ）は1台1分です。</p>
<p>ここで「工程は止めるな 造れるだけ造れ」というルールで 1日600台造ったとします。</p>
<ul>
<li>注文は480台。毎日120台が余ります。</li>
<li>仮に1台に材料費などが1,000円かかるとすると 120台分で毎日12万円です。</li>
<li>余った分があとで使われないとすると 1か月（20日）で2,400台 240万円。その置き場と運ぶ人も必要になります。</li>
</ul>
<p>帳簿では在庫は資産として数えられるので 利益が出ているように見えることもあります。でもトヨタ生産方式では 必要以上の在庫をムダと考えます。材料のお金が先に出ていき 置き場や運搬の手間もかかるからです。造りすぎ工場でも 売れると決まっていない在庫は価値ゼロとして数えます。</p>

<h2>職場で造りすぎを見つけるチェック</h2>
<ul>
<li>工程と工程のあいだに 決まった数より多い仕掛品が置いてある</li>
<li>「手があいたから とりあえず次の分を造っておく」が当たり前になっている</li>
<li>人や機械の稼働率（どれだけ動いているか）を上げることが目標になっている</li>
<li>まとめて造ったほうが効率がいい と思われている</li>
<li>置き場が足りなくなって 通路や空いた場所に物が置かれている</li>
</ul>

<h2>造りすぎをなくすには</h2>
<ol>
<li><b>タクトタイムで造る</b>：造る速さを 機械の速さではなく お客様の注文で決めます。</li>
<li><b>後工程引取り</b>：後の工程が 必要なものを 必要なときに 必要な数だけ引き取り 前の工程は引き取られた分だけを造って補充します。かんばんはそのための道具です。</li>
<li><b>工程のあいだに置く数を決める</b>：ラインを止めずに流すのに必要な最低限の仕掛品（標準手持ち）を決め それ以上は造りません。</li>
<li><b>止まってよいと決める</b>：やることがなければ止まる。止まった時間は 改善できる余力が見えたしるしです。</li>
</ol>

<h2>現場でよくある誤解</h2>
<ul>
<li><b>「人や機械を止めるのはもったいない」</b>：止めずに造った分は 在庫と置き場と運搬のコストになります。もったいないのは止まることではなく 売れないものを造ることです。</li>
<li><b>「在庫があれば安心」</b>：在庫は 不良や設備の問題 段取りの長さなどを見えなくします。問題がかくれたままになります。</li>
<li><b>「稼働率が高いほどよい」</b>：トヨタ生産方式で大事にするのは 必要なときに設備が動ける状態にある割合（可動率）です。どれだけ動かすかは注文に合わせて決めます。稼働率を上げるために必要以上に造ると 造りすぎになります。</li>
</ul>

<h2>造りすぎのムダを体験してみる</h2>
<p><a href="../../games/factory/">造りすぎ工場</a>は 4つの工程と1日480台の注文がある架空の工場で「工程は止めるな 造れるだけ造れ」のルールのまま動かすと 注文は全部出せるのに利益がマイナスになるのを体験する無料のブラウザゲームです。人数と仕掛品の数を変えて 本当に利益が出る形を自分で見つけます。研修では「注文は全部出せた。ではお金はどこに消えた？」という問いから話が深まります。</p>
<p><a class="btn primary" href="../../play/factory/">無料で遊ぶ</a><a class="btn ghost" href="../../games/factory/">ゲームの説明を見る</a></p>
<p>平準化については <a href="../heijunka/">平準化とは？ わかりやすく解説</a> にまとめています。</p>
<p>研修での使い方は <a href="../kenshu-game/">製造業の研修に使えるゲーム</a> にまとめています。</p>
<p>タクトタイムの出し方は <a href="../takt-time/">タクトタイムとサイクルタイムの違い</a> にまとめています。</p>

<h2>書いた人</h2>
<p>高木 務（Mendomi Lab）。トヨタの子会社のコンサル会社で20年以上 トヨタの現場で長く働いた人たちと組んで 30社以上の工場の改善をしてきました。研修や職場への導入の相談は <a href="../../consult/">相談する</a> からどうぞ。</p>
'''
JA2_FAQ = [
    ("造りすぎのムダとは何ですか？", "お客様が必要とする量より多く または必要なときより早く造ることです。トヨタ生産方式の7つのムダの1つです。"),
    ("7つのムダで一番悪いのはどれですか？", "造りすぎのムダです。在庫 運搬 動作などほかのムダを生み 手待ちや不良などの問題をかくしてしまうからです。"),
    ("7つのムダの順番は決まっていますか？", "決まった順番で覚える必要はありません。ただし造りすぎのムダを最初に挙げることが多く いちばん悪いムダとして扱われます。"),
    ("造りすぎのムダをなくすには何から始めればいいですか？", "まず休けいなどをのぞいた稼働時間を注文数で割って タクトタイムを出し いまの造る速さとくらべます。次に 工程のあいだにたまっている仕掛品を見て 置く数を決めます。"),
]

# ---------- 英語：lean simulation games ----------
EN2_BODY = '''  <p class="lead"><b>These are free, browser-based lean simulation games for training.</b> Each one takes 10–20 minutes to play and 30–90 minutes as a workshop. Nothing to install and no sign-up — open the link, share your screen or put groups in front of a laptop, and run the session. They were built by a consultant with more than 20 years at a Toyota subsidiary consulting company, from the way lean is actually taught on the shop floor.</p>

<h2>The games</h2>
<table><thead><tr><th>Game</th><th>Lean topic</th><th>Play time</th><th>Workshop</th><th>Price</th></tr></thead><tbody>
<tr><td><a href="../../games/overproduction-factory/">Overproduction Factory</a></td><td>Overproduction waste, takt time, people per process, standard WIP</td><td>10–20 min</td><td>30–90 min</td><td>Free / Pro $29, team $99</td></tr>
<tr><td><a href="../../games/suppliers-puzzle/">The Supplier's Puzzle</a></td><td>Heijunka (production leveling), supplier capacity and inventory cost</td><td>10–20 min</td><td>30–90 min</td><td>Free / Pro $49, team $149</td></tr>
</tbody></table>

<h3>Overproduction Factory</h3>
<p>Four processes and a daily order of 480 units. The old rule on the floor is "never let a process stop, build as much as you can." Follow it and every ordered unit ships — yet the day ends in a loss. Players change the crew and the work-in-process between processes until the line actually makes money. Best for a first lean session, supervisors and improvement teams.</p>
<p><a class="btn primary" href="https://ttmtkg.itch.io/overproduction-factory">Play free</a><a class="btn ghost" href="../../games/overproduction-factory/">How it works</a></p>

<h3>The Supplier's Puzzle</h3>
<p>Set in a fictional scenario inspired by Toyota production, the customer needs 8,000 cars this month and players run two suppliers. They change the build order, people and machines and explore how a leveled sequence can lower the supplier's cost. Best for purchasing, planning and supplier development teams, and for teaching heijunka.</p>
<p><a class="btn primary" href="https://ttmtkg.itch.io/the-suppliers-puzzle">Play free</a><a class="btn ghost" href="../../games/suppliers-puzzle/">How it works</a></p>

<h2>How to choose</h2>
<ul>
<li><b>New to lean, or one session only:</b> start with Overproduction Factory. It opens the most basic question — are we building what the customer needs? See <a href="../overproduction-waste/">overproduction waste examples</a>.</li>
<li><b>Teaching heijunka or working with suppliers:</b> use The Supplier's Puzzle. Read <a href="../heijunka-examples/">heijunka examples with numbers</a> first if you need a refresher.</li>
<li><b>A half-day workshop:</b> run both. Overproduction first, then the supplier view of the same problem.</li>
</ul>

<h2>How to run a lean simulation session</h2>
<ol>
<li><b>Run it as it starts.</b> Let groups play without changing anything, so they see the problem with their own eyes.</li>
<li><b>Ask before you explain.</b> One good question does more than a slide: "Every unit shipped. So where did the money go?"</li>
<li><b>Let them try and fail.</b> The games never show the answer first. Wrong attempts are where the learning happens.</li>
<li><b>Compare runs.</b> Write each group's settings and results on a board and compare.</li>
<li><b>Bring it home.</b> End with one thing each person will look for in their own workplace tomorrow.</li>
</ol>

<h2>Browser games vs. hands-on kits</h2>
<p>Classic hands-on simulations — building with blocks or folding paper products on a mini line — are great in a room. Browser games add three things: they run in remote and hybrid classes, they replay a full day or month in minutes so groups can test several ideas, and they show cost and profit numbers that are hard to track by hand. The two work well together.</p>

<h2>Free version and Pro</h2>
<p>The free versions are enough to play and to run a basic session. Pro is for trainers. It lets you change the settings to match your own workplace — orders, work times, prices and wages in Overproduction Factory; models, volumes, machines and costs in The Supplier's Puzzle — and adds a 6-page facilitator guide with the session plan, questions and common answers, offline use and one year of bug fixes.</p>
<p><a class="btn ghost" href="https://mendomilab.gumroad.com/l/overproduction-factory-pro">Overproduction Factory Pro</a><a class="btn ghost" href="https://mendomilab.gumroad.com/l/supplier-puzzle-pro">Supplier's Puzzle Pro</a></p>

<h2>About the author</h2>
<p>Tsutomu Takagi (Mendomi Lab). For more than 20 years I worked at a consulting company that is a Toyota subsidiary, teaming up with people who spent long careers on Toyota's shop floors and improving more than 30 factories. If you want help fitting these games to your course or workplace, <a href="../../consult/">get in touch</a>.</p>
'''
EN2_FAQ = [
    ("Are these lean simulation games free?", "Yes. The free versions run in a browser with no sign-up. Pro versions for trainers add customization, a facilitator guide and offline use."),
    ("Can I use them in an online or university class?", "Yes. They run in a modern web browser, so they work with screen sharing and in classrooms. They fit operations management and lean courses."),
    ("Do I need to be a lean expert to run them?", "No. The games are designed so the problem shows itself. The Pro facilitator guide gives the session plan, the questions to ask and the answers people usually give."),
    ("How long does a session take?", "Each game takes 10–20 minutes to play alone, and 30, 60 or 90 minutes as a facilitated workshop."),
]

if __name__ == '__main__':
    page('ja', 'ja/learn/tsukurisugi-no-muda/', '../../../',
         '造りすぎのムダとは？7つのムダで一番悪い理由と見つけ方｜Mendomi Lab',
         '造りすぎのムダとは 必要より多く早く造ること。7つのムダの中でなぜ一番悪いのか 数字の例 職場で見つけるチェック なくす方法を トヨタの子会社のコンサル会社で20年以上改善をしてきた人が説明します。',
         '造りすぎのムダとは？ 7つのムダで一番悪いと言われる理由', JA2_BODY, JA2_FAQ,
         [("Mendomi Lab", "https://mendomilab.com/ja/"), ("造りすぎのムダとは", "https://mendomilab.com/ja/learn/tsukurisugi-no-muda/")],
         'learn/overproduction-waste/', og='og_ja_of')
    page('en', 'learn/lean-simulation-games/', '../../',
         'Lean Simulation Games Online (Free) | Mendomi Lab',
         'Free browser-based lean simulation games for training: overproduction, heijunka and bottlenecks. How to run each one as a 30–90 minute workshop.',
         'Lean simulation games online: free browser games for lean training', EN2_BODY, EN2_FAQ,
         [("Mendomi Lab", "https://mendomilab.com/"), ("Lean simulation games", "https://mendomilab.com/learn/lean-simulation-games/")],
         None, og='og')


# ---------- 日本語：製造業の研修ゲーム ----------
JA3_BODY = '''  <p class="lead"><b>製造業の研修で使える トヨタ生産方式（TPS）を体験するゲームです。</b>どれもブラウザで無料で遊べて 登録もいりません。研修なら30〜90分で使えます（時間は下の一覧）。新人研修 監督者研修 改善チームの勉強会 大学の授業に向いています。トヨタの子会社のコンサル会社で20年以上 工場の改善をしてきた人が 現場での教え方をもとに作りました。</p>

<h2>ゲームの一覧</h2>
<table><thead><tr><th>ゲーム</th><th>学べること</th><th>向いている研修</th><th>研修の時間</th></tr></thead><tbody>
<tr><td><a href="../../games/factory/">造りすぎ工場</a></td><td>造りすぎのムダ タクトタイム 必要人数 標準手持ち</td><td>新人研修 監督者研修 リーンの入り口</td><td>30〜90分</td></tr>
<tr><td><a href="../../games/supplier/">サプライヤーのパズル</a></td><td>平準化 サプライヤーの人 設備 在庫のコスト</td><td>購買 生産計画 調達 管理職研修</td><td>30〜90分</td></tr>
<tr><td><a href="../../games/pasta/">回らないパスタ屋</a></td><td>ネック（いちばん先にいっぱいになる場所） 人数の配置</td><td>研修の入り口 製造業以外のチーム</td><td>30〜60分</td></tr>
</tbody></table>

<h2>研修の目的からえらぶ</h2>
<ul>
<li><b>新人研修で「ムダ」と「お客様が必要な量」を体で覚えてほしい</b>：<a href="../../games/factory/">造りすぎ工場</a>。「工程は止めるな 造れるだけ造れ」のまま動かすと 注文は全部出せても1日の利益がマイナスになるのを体験します。</li>
<li><b>監督者や改善チームに 人数と仕掛品の決め方を学んでほしい</b>：造りすぎ工場で タクトタイムと標準手持ちを自分で出します。</li>
<li><b>購買や生産計画の担当に サプライヤーとの関係を考えてほしい</b>：<a href="../../games/supplier/">サプライヤーのパズル</a>。組み立ての順番が サプライヤーの人 設備 在庫のコストにどう影響するかを見ます。</li>
<li><b>まず楽しく入りたい 事務やサービスの人もいる</b>：<a href="../../games/pasta/">回らないパスタ屋</a>。飲食店が題材なので だれでも入りやすいです。</li>
<li><b>半日の研修</b>：パスタ屋 → 造りすぎ工場 → サプライヤーのパズル の順に 身近な題材からつなげます。</li>
</ul>

<h2>製造業の新入社員研修での使い方（60分の例）</h2>
<table><thead><tr><th>時間</th><th>やること</th></tr></thead><tbody>
<tr><td>5分</td><td>工場の説明と「工程は止めるな 造れるだけ造れ」というルールを伝える</td></tr>
<tr><td>10分</td><td>造りすぎ工場を そのまま1日動かす（2〜3人で1画面）</td></tr>
<tr><td>10分</td><td>ふり返り「注文は全部出せた。ではお金はどこに消えた？」</td></tr>
<tr><td>20分</td><td>人数と工程のあいだの数を変えて もう一度動かし グループの結果をくらべる</td></tr>
<tr><td>10分</td><td>タクトタイムと造りすぎのムダを 体験とつなげて説明する</td></tr>
<tr><td>5分</td><td>明日から職場で見るところを 1人1つ書く</td></tr>
</tbody></table>

<h2>ゲーム形式の研修の進め方</h2>
<ol>
<li><b>まずそのまま動かす</b>：何も変えずに動かして 問題を自分の目で見てもらいます。</li>
<li><b>説明の前に問いかける</b>：「注文は全部出せた。ではお金はどこに消えた？」のような問いを1つだけ出します。</li>
<li><b>試してまちがえてもらう</b>：答えは先に言いません。まちがえた理由を話し合うところに学びがあります。</li>
<li><b>結果をくらべる</b>：グループごとの設定と結果をホワイトボードに書いてくらべます。</li>
<li><b>職場に持ち帰る</b>：明日から自分の職場で見るところを 1人1つ書いてもらいます。</li>
</ol>
<p>人数は何人でもできます。2〜3人で1つの画面を見ながら進めると 話し合いが生まれます。オンラインの研修でも 画面を共有すれば使えます。</p>

<h2>講義だけの研修とのちがい</h2>
<table><thead><tr><th></th><th>講義</th><th>ゲーム形式</th></tr></thead><tbody>
<tr><td>覚え方</td><td>言葉と考え方を聞く</td><td>自分で動かして 結果から気づく</td></tr>
<tr><td>試せる回数</td><td>考え方を聞くだけ</td><td>1日や1か月の動きを数分で何度もためせる</td></tr>
<tr><td>数字</td><td>例の数字を見る</td><td>自分が変えた人数や順番で 利益とコストが変わる</td></tr>
<tr><td>よいところ</td><td>考え方を短い時間で整理できる</td><td>試した結果をもとに話し合える</td></tr>
</tbody></table>
<p>講義とゲームはどちらかではなく 組み合わせると効きます。ゲームのあとに考え方を説明すると 言葉が体験とつながります。</p>

<h2>無料版とPro版</h2>
<p>無料版で遊ぶことも 研修で使うこともできます。造りすぎ工場とサプライヤーのパズルには 研修をする人向けのPro版があり 注文や工数 コストなどを自分の職場に合わせて変えられ 進行役の手引きもつきます（回らないパスタ屋は無料版だけです）。日本語のPro版も購入できます。研修に合わせた作り直しや 進め方の相談は <a href="../../consult/">相談する</a> からどうぞ（最初の1往復は無料）。</p>

<h2>書いた人</h2>
<p>高木 務（Mendomi Lab）。トヨタの子会社のコンサル会社で20年以上 トヨタの現場で長く働いた人たちと組んで 30社以上の工場の改善をしてきました。</p>
<p>あわせて読む：<a href="../tsukurisugi-no-muda/">造りすぎのムダとは？</a> ／ <a href="../heijunka/">平準化とは？</a> ／ <a href="../kanban/">かんばん方式とは？</a> ／ <a href="../lean-tps-chigai/">リーンとトヨタ生産方式の違い</a></p>
'''
JA3_FAQ = [
    ("無料で研修に使えますか？", "使えます。無料版はブラウザでそのまま遊べて 登録もいりません。研修をする人向けのPro版は 設定を自分の職場に合わせて変えられ 進行役の手引きがつきます（日本語版も購入できます）。"),
    ("リーンやトヨタ生産方式にくわしくなくても進行できますか？", "はじめてでも このページの手順で進められます。まずそのまま動かして 結果を見てから 何が起きたかを問いかけてください。"),
    ("オンライン研修でも使えますか？", "使えます。ブラウザで動くので 画面を共有すれば オンラインでも教室でも使えます。"),
    ("新人研修に向いているのはどれですか？", "造りすぎ工場です。必要な量を超えて造ると 在庫やコストがどう増えるのかを 短い時間で体験できます。"),
]

# ---------- 英語：overproduction waste examples ----------
EN3_BODY = '''  <p class="lead"><b>Overproduction waste means making more than the customer needs, or making it earlier than needed.</b> It is one of the <a href="../7-wastes-of-lean/">seven wastes</a> of the Toyota Production System, and it is often called the worst one, because it creates the other wastes and hides problems. Below are concrete overproduction waste examples — in a factory, in an office and in services — with numbers.</p>

<h2>Example 1: a line that "never stops"</h2>
<p>A plant receives an order of 480 units a day and has 480 minutes of working time, so the takt time is one minute per unit. The rule on the floor is "never let a process stop, build as much as you can," and the line builds 600 units a day.</p>
<ul>
<li>120 extra units are made every day.</li>
<li>If each unit ties up, say, $10 of material, that is $1,200 a day sitting on the floor.</li>
<li>If the extra units are not used later, after 20 working days that is 2,400 units and $24,000 — plus the space to store them and the people to move them.</li>
</ul>
<p>On the books, inventory is an asset, so the plant can look profitable. On the floor, money is tied up in material and inventory, and the extra units need space, handling and checking.</p>

<h2>Example 2: piles between processes</h2>
<p>Process A runs faster than process B. Nobody has set how many parts may wait between them, so A keeps going. By the afternoon there are hundreds of parts in front of B. If B finds a defect that started in A, many of the parts waiting in the pile may have the same problem — and A may have been making it for hours.</p>

<h2>Example 3: batch printing in an office</h2>
<p>A team prints and assembles 500 information packs at the start of the month "to be efficient." Halfway through, the form changes. The remaining packs go in the recycling bin. The waste came from printing more packs than were needed, before they were needed.</p>

<h2>Example 4: food prepared ahead in a restaurant</h2>
<p>A kitchen preps 80 portions of a dish before lunch because "it was busy last Friday." Only 50 sell. The rest is thrown out at closing, and the cooks spent the morning on food nobody ordered instead of on what customers wanted.</p>

<h2>Why overproduction is often called the worst waste</h2>
<table><thead><tr><th>Overproduction leads to…</th><th>How</th></tr></thead><tbody>
<tr><td>Inventory</td><td>What is made early usually has to be stored.</td></tr>
<tr><td>Transportation</td><td>It is often moved to storage and back again.</td></tr>
<tr><td>Motion</td><td>People search through piles for the right item.</td></tr>
<tr><td>Defects found late</td><td>Problems hide in the pile until the next process uses it.</td></tr>
<tr><td>Hidden waiting</td><td>Spare people and machines look busy, so nobody sees the extra capacity.</td></tr>
</tbody></table>

<h2>How to spot overproduction</h2>
<ul>
<li>Work-in-process regularly exceeds its agreed limit, or piles up between steps with no limit at all.</li>
<li>"We had time, so we made the next batch" is normal.</li>
<li>Machine or labor utilization is a target in itself.</li>
<li>Aisles and spare corners fill up with material.</li>
</ul>

<h2>How to reduce it</h2>
<ol>
<li><b>Work to takt time.</b> Set the pace from customer demand (available time ÷ demand), not from machine speed.</li>
<li><b>Pull, don't push.</b> Let the next process take what it needs, when it needs it, and make only what was taken. Kanban is a common tool for this.</li>
<li><b>Set a WIP limit.</b> Decide how much work-in-process may wait between steps — enough to keep the line flowing — and stop producing when the limit is reached. Review it as conditions change.</li>
<li><b>Allow stopping.</b> If there is nothing needed, stop. The idle time makes spare capacity visible, so it can be used for improvement or moved where it is needed.</li>
</ol>

<h2>See it in a game</h2>
<p><a href="../../games/overproduction-factory/">Overproduction Factory</a> is a free browser game about a factory with four processes and a daily order of 480 units, like Example 1. Follow the old "never stop" rule and every ordered unit ships — yet the day ends in a loss. Players change the crew and the work-in-process until the line actually makes money. In a workshop, one question opens the discussion: <em>"Every unit shipped. So where did the money go?"</em></p>
<p><a class="btn primary" href="https://ttmtkg.itch.io/overproduction-factory">Play free</a><a class="btn ghost" href="https://mendomilab.gumroad.com/l/overproduction-factory-pro">Pro for trainers ($29)</a></p>
<p>More games: <a href="../lean-simulation-games/">lean simulation games for training</a>. Related: <a href="../heijunka-examples/">heijunka examples</a> / <a href="../takt-time-vs-cycle-time/">takt time vs cycle time</a> / <a href="../mura-muri-muda/">mura, muri, muda examples</a>.</p>

<h2>How to run it in a 30-minute session</h2>
<ol>
<li><b>Round 1:</b> follow the "never stop" rule. Note the units shipped, the work-in-process left at the end of the day and the profit.</li>
<li><b>Round 2:</b> change the crew so each process runs at the pace of the order, not at full speed.</li>
<li><b>Round 3:</b> limit the work-in-process between processes, and compare the three results.</li>
</ol>
<h2>What to look for on a real floor</h2>
<ul>
<li>Piles of parts between processes, especially in front of a slower process.</li>
<li>People "keeping busy" while the next process is stopped.</li>
<li>Targets that reward output or machine utilization rather than what was actually shipped.</li>
<li>Finished goods waiting for an order that has not come yet.</li>
</ul>

<h2>About the author</h2>
<p>Tsutomu Takagi (Mendomi Lab). For more than 20 years I worked at a consulting company that is a Toyota subsidiary, teaming up with people who spent long careers on Toyota's shop floors and improving more than 30 factories. If you want help bringing these ideas into your training or workplace, <a href="../../consult/">get in touch</a>.</p>
'''
EN3_FAQ = [
    ("What is overproduction waste in lean?", "Making more than the customer needs, or making it earlier than needed. It is one of the seven wastes of the Toyota Production System."),
    ("What is a simple example of overproduction waste?", "A line that has an order of 480 units a day but builds 600 because no process is allowed to stop. The 120 extra units become inventory that needs space, handling and money."),
    ("Why is overproduction considered the worst of the seven wastes?", "Because it creates other wastes such as inventory, transportation and motion, and it hides problems such as defects and idle capacity."),
    ("Does overproduction happen outside manufacturing?", "Yes. Printing documents before they are needed, preparing more food than is likely to sell and processing batches before the next step needs them can all be overproduction."),
]

if __name__ == '__main__':
    page('ja', 'ja/learn/kenshu-game/', '../../../',
         '製造業の研修に使えるゲーム｜トヨタ生産方式を体験する無料の研修ゲーム｜Mendomi Lab',
         '製造業の新人研修 監督者研修 改善チームの勉強会に使える トヨタ生産方式を体験する無料のブラウザゲーム。造りすぎのムダ 平準化 ネックを30〜90分で学べます。ゲーム形式の研修の進め方つき。',
         '製造業の研修に使えるゲーム：トヨタ生産方式を体験する無料の研修ゲーム', JA3_BODY, JA3_FAQ,
         [("Mendomi Lab", "https://mendomilab.com/ja/"), ("製造業の研修ゲーム", "https://mendomilab.com/ja/learn/kenshu-game/")],
         None, og='og_ja_of')
    page('en', 'learn/overproduction-waste/', '../../',
         'Overproduction Waste Examples | Mendomi Lab',
         'Overproduction waste examples with numbers in a factory, an office and a restaurant. Why it is called the worst of the 7 wastes and how to reduce it.',
         'Overproduction waste examples: factory, office and service, with numbers', EN3_BODY, EN3_FAQ,
         [("Mendomi Lab", "https://mendomilab.com/"), ("Overproduction waste examples", "https://mendomilab.com/learn/overproduction-waste/")],
         'ja/learn/tsukurisugi-no-muda/', og='og_of')


# ---------- 日本語：タクトタイムとサイクルタイム ----------
JA4_BODY = '''  <p class="lead"><b>タクトタイムは お客様の注文で決まる「1個あたり何秒で造ればよいか」です。サイクルタイムは 工程や作業者が「実際に1個造るのに何秒かかっているか」です。</b>タクトタイムは目標の速さ サイクルタイムは今の速さ。この2つをくらべると 注文に間に合うか 人の配置が合っているか 造りすぎていないかを見直す手がかりになります。</p>

<h2>タクトタイムの計算方法</h2>
<p><b>タクトタイム ＝ 1日の稼働時間 ÷ 1日に必要な数</b></p>
<p>稼働時間は 休けいや朝礼などをのぞいた 実際に造れる時間です。</p>
<table><thead><tr><th>例</th><th>計算</th><th>タクトタイム</th></tr></thead><tbody>
<tr><td>稼働8時間（480分）で 1日480台</td><td>28,800秒 ÷ 480台</td><td>60秒</td></tr>
<tr><td>稼働7.5時間（450分）で 1日300台</td><td>27,000秒 ÷ 300台</td><td>90秒</td></tr>
<tr><td>月20日稼働 1日8時間（休けいなどをのぞく）で 月9,600台</td><td>1日480台 → 28,800秒 ÷ 480台</td><td>60秒</td></tr>
</tbody></table>
<p>注文や造れる時間が変わればタクトタイムも変わります。機械の速さや人数は 計算式に入りません。</p>

<h2>サイクルタイムとは</h2>
<p>サイクルタイムは 工程から製品が1個ずつ送り出される間隔です。1人の作業者を測るときは その人が決まった作業を1回くり返す時間を見ます。ストップウォッチで何回か測り ばらつきも見ます。</p>

<h2>タクトタイムとサイクルタイムの違い</h2>
<table><thead><tr><th></th><th>タクトタイム</th><th>サイクルタイム</th></tr></thead><tbody>
<tr><td>何の時間か</td><td>お客様が求める速さ（目標）</td><td>工程が実際に造っている速さ（実力）</td></tr>
<tr><td>決めるもの</td><td>注文の数と稼働時間</td><td>作業のやり方 設備 人</td></tr>
<tr><td>出し方</td><td>計算する</td><td>現場で測る</td></tr>
<tr><td>変えたいとき</td><td>注文や稼働時間が変わったときに見直す</td><td>改善で縮める</td></tr>
</tbody></table>

<h2>2つをくらべると何がわかるか</h2>
<table><thead><tr><th>状態</th><th>起きていること</th><th>やること</th></tr></thead><tbody>
<tr><td>サイクルタイム ＜ タクトタイム</td><td>必要な速さより速く造れる。必要な数をこえて造れば<b>造りすぎ</b>になり 必要な数で止めれば手待ちが出る</td><td>タクトタイムに合わせて造る。余った力は人の配置を見直して改善に回す</td></tr>
<tr><td>サイクルタイム ＞ タクトタイム</td><td>その工程が注文に間に合わないおそれがある。残業や欠品につながる</td><td>ネックの原因を調べ 作業の改善や 設備・人の配置を見直す</td></tr>
<tr><td>サイクルタイム ≒ タクトタイム</td><td>お客様の速さで流れている</td><td>ばらつきを小さくする</td></tr>
</tbody></table>

<h2>必要な人数の出し方</h2>
<p><b>必要人数の目安 ＝ 1個を造る人の作業時間の合計 ÷ タクトタイム</b></p>
<p>たとえば4つの工程の作業時間の合計が240秒で タクトタイムが60秒なら 240 ÷ 60 ＝ 計算上は4人です。ただし 1人ひとりの作業を60秒以内に分けられるかも確かめます。合計が250秒なら4.17人。すぐ5人にするのではなく まず作業のムダを取って240秒以内にできないかを考え できなければ5人や稼働時間の見直しを考えます。</p>

<h2>リードタイムとの違い</h2>
<p>リードタイムは 注文を受けてから（または材料が入ってから）お客様に届くまでの時間です。タクトタイムとサイクルタイムが「1個あたりの速さ」なのに対して リードタイムは「全体でどれだけ待たせるか」です。工程のあいだに在庫が多いほど リードタイムは長くなります。</p>

<h2>現場でよくある誤解</h2>
<ul>
<li><b>「機械の速さがタクトタイム」</b>：それはサイクルタイムです。タクトタイムはお客様の注文から計算します。</li>
<li><b>「稼働時間に休けいも入れる」</b>：休けいや会議の時間は造れません。入れるとタクトタイムが長く出て 間に合わなくなります。</li>
<li><b>「速く造れるなら速く造ったほうがいい」</b>：タクトタイムより速く造り続けると 造りすぎになります。速く造れる力は 人を減らしたり別の仕事に回したりして使います。</li>
</ul>

<h2>タクトタイムを体験してみる</h2>
<p><a href="../../games/factory/">造りすぎ工場</a>は 1日480台の注文がある架空の工場で タクトタイムと工程ごとの必要人数を自分で出して 利益が出る形を見つける無料のブラウザゲームです。「工程は止めるな 造れるだけ造れ」のまま動かすと どうなるかから始まります。</p>
<p><a class="btn primary" href="../../play/factory/">無料で遊ぶ</a><a class="btn ghost" href="../../games/factory/">ゲームの説明を見る</a></p>
<p>あわせて読む：<a href="../tsukurisugi-no-muda/">造りすぎのムダとは？</a> ／ <a href="../heijunka/">平準化とは？</a> ／ <a href="../kenshu-game/">製造業の研修に使えるゲーム</a> ／ <a href="../bottleneck/">ボトルネック工程とは？</a></p>

<h2>書いた人</h2>
<p>高木 務（Mendomi Lab）。トヨタの子会社のコンサル会社で20年以上 トヨタの現場で長く働いた人たちと組んで 30社以上の工場の改善をしてきました。研修や職場への導入の相談は <a href="../../consult/">相談する</a> からどうぞ。</p>
'''
JA4_FAQ = [
    ("タクトタイムとサイクルタイムの違いは何ですか？", "タクトタイムはお客様の注文で決まる目標の速さ（稼働時間÷必要数）で 計算して出します。サイクルタイムは工程が実際に1個造るのにかかる時間で 現場で測ります。"),
    ("タクトタイムの計算方法は？", "1日の稼働時間（休けいなどをのぞく）を1日に必要な数で割ります。稼働480分で480台なら 28,800秒÷480台＝60秒です。"),
    ("サイクルタイムがタクトタイムより短いとどうなりますか？", "必要な数をこえて造れば造りすぎになり 必要な数で止めれば手待ちが出ます。タクトタイムに合わせて造り 余った力は人の配置を見直して改善に回します。"),
    ("必要な人数はどう出しますか？", "1個を造る人の作業時間の合計をタクトタイムで割ると目安が出ます。合計240秒でタクトタイム60秒なら計算上は4人です。1人ひとりの作業をタクトタイム以内に分けられるかも確かめます。"),
]

# ---------- 英語：takt time vs cycle time ----------
EN4_BODY = '''  <p class="lead"><b>Takt time is the pace the customer requires — how many seconds you have per unit. Cycle time is how long a process or operator actually takes to complete one unit.</b> Takt time is the target; cycle time is your current speed. Comparing the two helps you check whether you can meet demand, whether staffing fits, and whether you are overproducing.</p>

<h2>Takt time formula</h2>
<p><b>Takt time = available working time per day ÷ units required per day</b></p>
<p>Available time excludes breaks, meetings and other planned stops.</p>
<table><thead><tr><th>Example</th><th>Calculation</th><th>Takt time</th></tr></thead><tbody>
<tr><td>480 min available, 480 units a day</td><td>28,800 s ÷ 480</td><td>60 s</td></tr>
<tr><td>450 min available, 300 units a day</td><td>27,000 s ÷ 300</td><td>90 s</td></tr>
<tr><td>20 days × 480 min available (after breaks), 9,600 units a month</td><td>480 a day → 28,800 s ÷ 480</td><td>60 s</td></tr>
</tbody></table>
<p>When demand or available time changes, takt time changes. Machine speed and headcount are not part of the formula.</p>

<h2>What cycle time is</h2>
<p>Cycle time is the interval at which a process releases one unit. For a single operator, it is the time to complete their work sequence once. Measure it several times with a stopwatch and look at the variation, not just the average.</p>

<h2>Takt time vs cycle time</h2>
<table><thead><tr><th></th><th>Takt time</th><th>Cycle time</th></tr></thead><tbody>
<tr><td>What it is</td><td>The pace the customer needs (target)</td><td>The pace the process achieves (actual)</td></tr>
<tr><td>Set by</td><td>Demand and available time</td><td>Method, equipment and people</td></tr>
<tr><td>How you get it</td><td>Calculate it</td><td>Measure it on the floor</td></tr>
<tr><td>How it changes</td><td>Review when demand or available time changes</td><td>Reduce through improvement</td></tr>
</tbody></table>

<h2>What the comparison tells you</h2>
<table><thead><tr><th>Situation</th><th>What happens</th><th>What to do</th></tr></thead><tbody>
<tr><td>Cycle time &lt; takt time</td><td>You can build faster than needed. Produce beyond the quantity needed and you <b>overproduce</b>; stop at the quantity needed and there is waiting time</td><td>Build to takt. Use the spare capacity by rebalancing people and improving</td></tr>
<tr><td>Cycle time &gt; takt time</td><td>The process risks missing demand: overtime or shortages</td><td>Find the cause at the bottleneck; improve the work or rebalance people and equipment</td></tr>
<tr><td>Cycle time ≈ takt time</td><td>Work flows at the customer's pace</td><td>Reduce variation</td></tr>
</tbody></table>

<h2>How many people you need</h2>
<p><b>People needed (estimate) = total manual work time per unit ÷ takt time</b></p>
<p>If the work across four processes adds up to 240 seconds and takt time is 60 seconds, the calculation gives 240 ÷ 60 = 4 people — provided the work can be split so each person stays within 60 seconds. If it adds up to 250 seconds, that is 4.17. Before adding a fifth person, look for waste and try to bring the total within 240 seconds; if you cannot, consider a fifth person or a change in working time.</p>

<h2>Takt time vs cycle time vs lead time</h2>
<p>Lead time is the time from receiving an order (or material) until the customer receives the product. Takt and cycle time are about pace per unit; lead time is about how long the customer waits overall. The more inventory sits between processes, the longer the lead time.</p>

<h2>Common mistakes</h2>
<ul>
<li><b>Calling machine speed "takt time."</b> That is cycle time. Takt time comes from customer demand.</li>
<li><b>Including breaks in available time.</b> Nobody produces during breaks. Including them makes takt look longer than it is, and you fall behind.</li>
<li><b>"If we can go faster, we should."</b> Producing beyond what is needed is overproduction. Build to takt and use the extra capacity by freeing people for other work or improvement.</li>
</ul>

<h2>Practice it in a game</h2>
<p><a href="../../games/overproduction-factory/">Overproduction Factory</a> is a free browser game: a fictional factory with a daily order of 480 units. Players work out the takt time and the people needed per process, and find the setup that actually makes a profit — starting from the old rule "never let a process stop, build as much as you can."</p>
<p><a class="btn primary" href="https://ttmtkg.itch.io/overproduction-factory">Play free</a><a class="btn ghost" href="https://mendomilab.gumroad.com/l/overproduction-factory-pro">Pro for trainers ($29)</a></p>
<p>Related: <a href="../overproduction-waste/">overproduction waste examples</a> / <a href="../heijunka-examples/">heijunka examples</a> / <a href="../lean-simulation-games/">lean simulation games</a> / <a href="../bottleneck-analysis/">bottleneck analysis</a></p>

<h2>How to run it in a 30-minute session</h2>
<ol>
<li>Players first calculate the takt time from the daily order and the available working time.</li>
<li>They compare it with the cycle time of each process and find which processes are faster or slower than takt.</li>
<li>They set the number of people per process and check the profit. Then they discuss what changed.</li>
</ol>
<h2>What to look for on a real floor</h2>
<ul>
<li>Measure cycle time with a stopwatch over about 10 cycles, not from a standard sheet. Look at the spread as well as the average.</li>
<li>Check whether takt time is recalculated when demand changes, or stays the same for months.</li>
<li>A process far faster than takt usually builds piles in front of the next one.</li>
<li>A process slower than takt is often covered by overtime that nobody counts as a problem.</li>
</ul>

<h2>About the author</h2>
<p>Tsutomu Takagi (Mendomi Lab). For more than 20 years I worked at a consulting company that is a Toyota subsidiary, teaming up with people who spent long careers on Toyota's shop floors and improving more than 30 factories. If you want help bringing these ideas into your training or workplace, <a href="../../consult/">get in touch</a>.</p>
'''
EN4_FAQ = [
    ("What is the difference between takt time and cycle time?", "Takt time is the pace the customer requires (available time ÷ demand); you calculate it. Cycle time is how long a process actually takes to complete one unit; you measure it."),
    ("What is the takt time formula?", "Takt time = available working time ÷ units required. With 480 minutes available and 480 units a day, takt time is 28,800 s ÷ 480 = 60 seconds."),
    ("What happens if cycle time is shorter than takt time?", "Produce beyond the quantity needed and you overproduce; stop at the quantity needed and there is waiting time. Build to takt and use the spare capacity by rebalancing people and improving."),
    ("How do you calculate the number of operators needed?", "Divide the total manual work time per unit by takt time for an estimate. 240 seconds of work at a 60-second takt gives 4 people, if the work can be split so each person stays within takt."),
]

if __name__ == '__main__':
    page('ja', 'ja/learn/takt-time/', '../../../',
         'タクトタイムとサイクルタイムの違い｜計算方法と例・必要人数の出し方｜Mendomi Lab',
         'タクトタイムはお客様の注文で決まる目標の速さ サイクルタイムは今の速さ。計算方法と例 2つをくらべてわかること 必要人数の出し方 リードタイムとの違いを トヨタの子会社のコンサル会社で20年以上改善をしてきた人が説明します。',
         'タクトタイムとサイクルタイムの違い（計算方法と例）', JA4_BODY, JA4_FAQ,
         [("Mendomi Lab", "https://mendomilab.com/ja/"), ("タクトタイムとサイクルタイム", "https://mendomilab.com/ja/learn/takt-time/")],
         'learn/takt-time-vs-cycle-time/', og='og_ja_of')
    page('en', 'learn/takt-time-vs-cycle-time/', '../../',
         'Takt Time vs Cycle Time: Formula & Examples | Mendomi',
         'Takt time vs cycle time: the formulas, worked examples, and how to use the gap to decide staffing and spot overproduction.',
         'Takt time vs cycle time: formula, examples and staffing', EN4_BODY, EN4_FAQ,
         [("Mendomi Lab", "https://mendomilab.com/"), ("Takt time vs cycle time", "https://mendomilab.com/learn/takt-time-vs-cycle-time/")],
         'ja/learn/takt-time/', og='og_of')


# ---------- 日本語：ボトルネック工程 ----------
JA5_BODY = '''  <p class="lead"><b>ボトルネック（ネック）工程とは 工程の中でいちばん能力が低く 全体でつくれる量の上限を決めてしまう工程です。</b>ほかの工程がどれだけ速くても 全体の生産量はネックの速さをこえられません。だから改善はまずネックを見つけることから始めます。</p>

<h2>数字で見るボトルネック</h2>
<p>4つの工程が順番につながったラインで 1時間につくれる量が次のようだったとします。</p>
<table><thead><tr><th>工程</th><th>A</th><th>B</th><th>C</th><th>D</th></tr></thead><tbody>
<tr><td>1時間につくれる量</td><td>60個</td><td><b>40個</b></td><td>50個</td><td>70個</td></tr>
</tbody></table>
<p>注文が十分にあっても このラインでつくれるのは <b>1時間40個まで</b>です。Bがネックだからです。Aに人を足して80個つくれるようにしても 生産量は40個のまま。Bの前に仕掛品がたまるだけです。</p>
<p>Bを改善して60個にすると 上限は50個になります。今度はCがネックになりました。<b>ネックを1つ直すと 別の工程（または注文の量）が次の制約になります。</b></p>

<h2>工程の能力の計算方法</h2>
<p><b>1日につくれる量 ＝ 1日の稼働時間 ÷ その工程のサイクルタイム</b></p>
<p>稼働480分（28,800秒）で サイクルタイム72秒の工程なら 28,800 ÷ 72 ＝ 400個です。1日の注文が480個（タクトタイム60秒）なら この工程は足りません。サイクルタイムがタクトタイムより長い工程は 注文に対して能力が足りない工程です。いくつもあるときは その中でいちばん能力の低い工程がネックの候補です。なお この計算は止まる時間や不良を入れていない目安です。タクトタイムの出し方は <a href="../takt-time/">タクトタイムとサイクルタイムの違い</a> にまとめています。</p>

<h2>現場でネックを見つける4つのしるし</h2>
<ul>
<li><b>前に仕掛品がたまっている</b>：前の工程から来たものが 待たされて山になっている</li>
<li><b>後ろが待っている</b>：次の工程の人が手を止めて 物が来るのを待っている</li>
<li><b>いつも止まらずに動いている</b>：ほかの工程に手待ちがあるのに そこだけは休みなく動いている</li>
<li><b>サイクルタイムがタクトタイムより長い</b>：測ってくらべると数字でわかる</li>
</ul>
<p>見かけの忙しさにだまされないことも大事です。いちばんバタバタしている場所が ネックとはかぎりません。行列の原因が 別の場所にあることもあります。</p>

<h2>ボトルネックの改善の順番</h2>
<ol>
<li><b>ネックを見つける</b>：上の4つのしるしと数字で確かめます。</li>
<li><b>ネックを止めない</b>：休けいをずらす 段取り替えを短くする ネックの前に少しだけ仕掛品を置くなどして ネックの時間をむだにしません。</li>
<li><b>ほかの工程をネックに合わせる</b>：ネックより速い工程が造り続けると 在庫がふえるだけです。造る量をネックに合わせます。</li>
<li><b>ネックの能力を上げる</b>：作業のムダを取る 人や設備を足すなどで ネックそのものを速くします。</li>
<li><b>次のネックを探す</b>：ネックは移るので 1にもどります。</li>
</ol>

<h2>よくある誤解</h2>
<ul>
<li><b>「人を足せば生産量が上がる」</b>：ネック以外に人を足しても 生産量は増えません。人件費だけが増えます。</li>
<li><b>「全部の工程をフルに動かすのがいい」</b>：ネックより速い工程をフルに動かすと 造りすぎになります（<a href="../tsukurisugi-no-muda/">造りすぎのムダとは？</a>）。</li>
<li><b>「ネックは機械のこと」</b>：人の作業 検査 運搬 事務の承認など どこでもネックになります。</li>
</ul>

<h2>飲食店のボトルネック</h2>
<p>ボトルネックは工場だけの話ではありません。飲食店なら 席 厨房 ホール レジ 皿洗いのどれかがネックになります。席が空いているのに料理が出ないなら厨房 料理はできているのに運べないならホール 食べ終わったお客さんがレジに並んでいるならレジ。忙しいからといって全部の持ち場に人を足すと 売上は変わらず人件費だけが増えることもあります。飲食店の回転率を上げたいときも 考える順番は同じです。</p>

<h2>ボトルネックを体験してみる</h2>
<p><a href="../../games/pasta/">回らないパスタ屋</a>は 14席の小さなパスタ屋のランチ（11時〜14時）で 厨房 ホール レジの人数を変えて ネックを見つける無料のブラウザゲームです。「忙しいなら人を増やせ」で7人で回してきた店を どこがネックかを探して見直します。工場の題材なら <a href="../../games/factory/">造りすぎ工場</a> で 工程ごとの人数を考えられます。</p>
<p><a class="btn primary" href="../../play/pasta/">無料で遊ぶ</a><a class="btn ghost" href="../../games/pasta/">ゲームの説明を見る</a></p>
<p>あわせて読む：<a href="../takt-time/">タクトタイムとサイクルタイムの違い</a> ／ <a href="../kenshu-game/">製造業の研修に使えるゲーム</a> ／ <a href="../kaitenritsu/">飲食店の回転率とは？</a></p>

<h2>書いた人</h2>
<p>高木 務（Mendomi Lab）。トヨタの子会社のコンサル会社で20年以上 トヨタの現場で長く働いた人たちと組んで 30社以上の工場の改善をしてきました。研修や職場への導入の相談は <a href="../../consult/">相談する</a> からどうぞ。</p>
'''
JA5_FAQ = [
    ("ボトルネック工程とは何ですか？", "工程の中でいちばん能力が低く 全体でつくれる量を決めてしまう工程です。ネック工程ともいいます。"),
    ("ボトルネックの計算方法は？", "工程ごとに 稼働時間をサイクルタイムで割って 1日につくれる量を出します。いちばん少ない工程がネックです。稼働480分（28,800秒）でサイクルタイム72秒なら 28,800÷72＝400個です。止まる時間や不良を入れていない目安です。"),
    ("ボトルネックはどうやって見つけますか？", "前に仕掛品がたまっている 後ろの工程が待っている いつも止まらずに動いている サイクルタイムがタクトタイムより長い の4つが目安です。"),
    ("ボトルネックを解消すると終わりですか？", "終わりません。1つ直すと 次に能力の低い工程や 注文の量が新しい制約になります。見つけて直すことをくり返します。"),
]

# ---------- 英語：bottleneck analysis ----------
EN5_BODY = '''  <p class="lead"><b>A bottleneck is the step with the lowest capacity in a process. It sets the maximum output of the whole line.</b> However fast the other steps are, the system cannot produce more than the bottleneck. That is why improvement starts with finding it. Below is a simple bottleneck analysis with numbers.</p>

<h2>A bottleneck example with numbers</h2>
<p>Four steps run in sequence. Their hourly capacity is:</p>
<table><thead><tr><th>Step</th><th>A</th><th>B</th><th>C</th><th>D</th></tr></thead><tbody>
<tr><td>Units per hour</td><td>60</td><td><b>40</b></td><td>50</td><td>70</td></tr>
</tbody></table>
<p>Even with plenty of orders, the line can produce at most <b>40 units an hour</b>, because B is the bottleneck. Adding people to A so it makes 80 an hour changes nothing — the parts simply pile up in front of B.</p>
<p>Improve B to 60 an hour and the limit rises to 50. Now C is the bottleneck. <b>Fix one bottleneck and another step — or demand itself — becomes the next constraint.</b></p>

<h2>How to calculate capacity</h2>
<p><b>Daily capacity of a step = available time per day ÷ cycle time of that step</b></p>
<p>With 480 minutes (28,800 seconds) available and a 72-second cycle time, a step can make 28,800 ÷ 72 = 400 units a day. If demand is 480 a day (a 60-second takt time), that step cannot keep up. Steps whose cycle time is longer than takt time lack capacity for demand; if there are several, the slowest is the bottleneck candidate. This is an estimate that ignores downtime and defects. See <a href="../takt-time-vs-cycle-time/">takt time vs cycle time</a>.</p>

<h2>Four signs of a bottleneck on the floor</h2>
<ul>
<li><b>Work piles up in front of it.</b></li>
<li><b>The next step is waiting for it.</b></li>
<li><b>It never stops,</b> while other steps have idle time.</li>
<li><b>Its cycle time is longer than takt time</b> when you measure it.</li>
</ul>
<p>Don't be fooled by how busy a place looks. The most hectic spot is not always the bottleneck, and a queue can be caused somewhere else.</p>

<h2>How to fix a bottleneck, step by step</h2>
<ol>
<li><b>Find it</b> with the signs above and the numbers.</li>
<li><b>Never let it stop.</b> Stagger breaks, shorten changeovers, and keep a small buffer in front of it so no bottleneck time is wasted.</li>
<li><b>Pace everything else to it.</b> Steps faster than the bottleneck only build inventory if they keep running.</li>
<li><b>Raise its capacity.</b> Remove waste from the work, or add people or equipment there.</li>
<li><b>Look for the next one.</b> The bottleneck moves, so go back to step 1.</li>
</ol>
<p>This sequence follows the same logic as the five focusing steps of the theory of constraints.</p>

<h2>Common mistakes</h2>
<ul>
<li><b>"More people means more output."</b> Adding people anywhere other than the bottleneck adds cost, not output.</li>
<li><b>"Every step should run at full speed."</b> Running non-bottlenecks flat out is overproduction (<a href="../overproduction-waste/">overproduction waste examples</a>).</li>
<li><b>"Bottlenecks are machines."</b> Manual work, inspection, transport and office approvals can all be bottlenecks.</li>
</ul>

<h2>Bottlenecks outside the factory</h2>
<p>In a restaurant, the bottleneck can be the seats, the kitchen, the servers, the cashier or the dishwashing. Empty tables but slow food: the kitchen. Food ready but not served: the floor staff. Finished guests queuing to pay: the cashier. Adding staff everywhere because it is busy can raise cost without raising sales.</p>

<h2>Practice it in a game</h2>
<p><a href="../../games/overproduction-factory/">Overproduction Factory</a> is a free browser game with four processes and a daily order of 480 units. Players set the people per process, watch where work piles up, and find the setup that makes a profit. More games: <a href="../lean-simulation-games/">lean simulation games</a>.</p>
<p><a class="btn primary" href="https://ttmtkg.itch.io/overproduction-factory">Play free</a><a class="btn ghost" href="https://mendomilab.gumroad.com/l/overproduction-factory-pro">Pro for trainers ($29)</a></p>

<h2>About the author</h2>
<p>Tsutomu Takagi (Mendomi Lab). For more than 20 years I worked at a consulting company that is a Toyota subsidiary, teaming up with people who spent long careers on Toyota's shop floors and improving more than 30 factories. If you want help bringing these ideas into your training or workplace, <a href="../../consult/">get in touch</a>.</p>
'''
EN5_FAQ = [
    ("What is a bottleneck in lean?", "The step with the lowest capacity in a process. It limits the output of the whole system."),
    ("How do you calculate a bottleneck?", "Divide available time by each step's cycle time to get its capacity. The step with the lowest capacity is the bottleneck. 480 minutes (28,800 seconds) at a 72-second cycle time gives 28,800 ÷ 72 = 400 units a day, before downtime and defects."),
    ("How do you identify a bottleneck on the floor?", "Work piles up in front of it, the next step waits for it, it never stops while others have idle time, and its cycle time is longer than takt time."),
    ("What happens after you fix a bottleneck?", "Another step, or demand itself, becomes the new constraint. Bottleneck analysis is a cycle: find it, fix it, and look for the next one."),
]

if __name__ == '__main__':
    page('ja', 'ja/learn/bottleneck/', '../../../',
         'ボトルネック工程とは？見つけ方と計算方法・改善の順番｜Mendomi Lab',
         'ボトルネック（ネック）工程とは 全体の生産量を決めるいちばん能力の低い工程。数字の例 計算方法 現場で見つける4つのしるし 改善の順番 飲食店の例を トヨタの子会社のコンサル会社で20年以上改善をしてきた人が説明します。',
         'ボトルネック工程とは？ 見つけ方と計算方法', JA5_BODY, JA5_FAQ,
         [("Mendomi Lab", "https://mendomilab.com/ja/"), ("ボトルネック工程とは", "https://mendomilab.com/ja/learn/bottleneck/")],
         'learn/bottleneck-analysis/', og='og_ja_pasta')
    page('en', 'learn/bottleneck-analysis/', '../../',
         'Bottleneck Analysis in Lean (with Numbers) | Mendomi',
         'How to find a bottleneck with simple numbers, why adding people elsewhere does not help, and the order to fix it. With a free game to practice.',
         'Bottleneck analysis in lean: how to find and fix a bottleneck', EN5_BODY, EN5_FAQ,
         [("Mendomi Lab", "https://mendomilab.com/"), ("Bottleneck analysis", "https://mendomilab.com/learn/bottleneck-analysis/")],
         'ja/learn/bottleneck/', og='og_of')


# ---------- 日本語：かんばん方式 ----------
JA6_BODY = '''  <p class="lead"><b>かんばん方式とは 後の工程が使った分だけを 前の工程に「運んで」「つくって」と知らせる札（かんばん）を使うしくみです。</b>トヨタ生産方式の柱の1つ「ジャストインタイム」（必要なものを 必要なときに 必要な量だけ）を実現するための道具です。</p>

<h2>ジャストインタイムとかんばんの関係</h2>
<p>ジャストインタイムは目的で かんばんはその手段です。前の工程が計画どおりにつくって後ろへ送る（押し出す）のではなく 後の工程が必要な分を取りに行く（引き取る）ことで つくりすぎと在庫を防ぎます。</p>

<h2>かんばんは2種類</h2>
<table><thead><tr><th>かんばん</th><th>何を知らせるか</th></tr></thead><tbody>
<tr><td>引き取りかんばん</td><td>後の工程が 前の工程から「何を いくつ 引き取るか」</td></tr>
<tr><td>生産指示かんばん</td><td>前の工程に「何を いくつ つくるか」</td></tr>
</tbody></table>

<h2>数字で見る かんばんの流れ</h2>
<p>部品が1箱20個入り 1箱にかんばんが1枚ついているとします。</p>
<ol>
<li>組立ラインで箱を使い始めたら 箱についている<b>引き取りかんばん</b>を外して ポストに入れます。</li>
<li>運ぶ人が決まった時間に引き取りかんばんを集め 前の工程へ行き 同じ部品を1箱（20個）引き取ります。</li>
<li>引き取るとき 箱についていた<b>生産指示かんばん</b>を外して 引き取りかんばんにつけかえます。外した生産指示かんばんが「20個つくって」の合図になり 前の工程はその分だけをつくります。</li>
</ol>
<p>つまり 箱単位で 使った分を補充する形でしかつくらず 運ばない。かんばんで管理している範囲（工程のあいだの棚 運んでいる途中 つくっている途中の箱）では かんばんの枚数 × 1箱の入り数 が 部品の量の上限になります。</p>
<p>枚数の考え方の一例：1日400個使い 補充に半日かかり（かんばんを集める 運ぶ つくるまでの合計） 1割の余裕を見て 1箱20個なら 400 × 0.5 × 1.1 ÷ 20 ＝ 11枚です。端数が出たら切り上げます。現場では 集める間かくや運ぶ回数なども入れて 引き取りかんばんと生産指示かんばんそれぞれの枚数を決めます。</p>

<h2>かんばんのルール</h2>
<ul>
<li>後の工程が 前の工程へ取りに行く</li>
<li>前の工程は 引き取られた分だけをつくる</li>
<li>かんばんのないものは つくらない・運ばない</li>
<li>不良品を後の工程に送らない</li>
<li>かんばんの枚数を少しずつ減らして 隠れていた問題を見つけていく</li>
</ul>
<p>そして大前提が <a href="../heijunka/">平準化</a> です。後の工程の使い方に大きな波があると かんばんは前の工程に波をそのまま伝えてしまいます。</p>

<h2>ジャストインタイムのデメリットと注意点</h2>
<ul>
<li><b>止まりやすく見える</b>：在庫が少ないので 部品が1つ来ないとラインが止まります。災害や物流の止まりへの備え（どこにどれだけ置くか）は別に考える必要があります。</li>
<li><b>平準化なしで入れると 前の工程にしわ寄せがいく</b>：つくる量や種類に波があるままかんばんだけ入れると サプライヤーがいちばん忙しい日に合わせた人や在庫を持つことになります。「下請けに在庫を押しつける」と言われるのは この形のときです。</li>
<li><b>段取り替えを短くする必要がある</b>：小さいロットで何度もつくるので 切りかえの時間が長いと回りません。</li>
<li><b>運ぶ回数がふえる</b>：少しずつ何度も運ぶので 運び方（決まった順に回る運搬など）の工夫がいります。</li>
</ul>
<p>どれも「かんばんを入れれば在庫が減る」のではなく 波をならし 段取りを短くし 問題を1つずつ直した結果として在庫が減る ということです。</p>

<h2>タスク管理のカンバンとのちがい</h2>
<p>仕事の進み具合を「やること・やっている・終わった」の列で見せるタスク管理のカンバン（カンバンボード）は トヨタのかんばんの「進めている途中のものの数に上限をつける」考え方を借りたものです。列を並べるだけでは足りず 「やっている」の列に入れる数の上限を決めて はじめてカンバンらしくなります。工場のかんばんは 物と情報をいっしょに動かして つくる量そのものを決めるところがちがいます。</p>

<h2>かんばん・ジャストインタイムを体験してみる</h2>
<p><a href="../../games/supplier/">サプライヤーのパズル</a> では 組み立ての順番（平準化しているかどうか）で 前の工程にあたるサプライヤーの人 設備 在庫のコストがどう変わるかを見られます。<a href="../../games/factory/">造りすぎ工場</a> では 工程のあいだに置く数を決めないと 在庫がふえていく様子を体験できます。どちらも無料のブラウザゲームです。</p>
<p><a class="btn primary" href="../../play/supplier/">サプライヤーのパズルで遊ぶ</a><a class="btn ghost" href="../../play/factory/">造りすぎ工場で遊ぶ</a></p>
<p>あわせて読む：<a href="../heijunka/">平準化とは？</a> ／ <a href="../tsukurisugi-no-muda/">造りすぎのムダとは？</a> ／ <a href="../takt-time/">タクトタイムとサイクルタイムの違い</a> ／ <a href="../lean-tps-chigai/">リーンとトヨタ生産方式の違い</a></p>

<h2>書いた人</h2>
<p>高木 務（Mendomi Lab）。トヨタの子会社のコンサル会社で20年以上 トヨタの現場で長く働いた人たちと組んで 30社以上の工場の改善をしてきました。研修や職場への導入の相談は <a href="../../consult/">相談する</a> からどうぞ。</p>
'''
JA6_FAQ = [
    ("かんばん方式とは何ですか？", "後の工程が使った分だけを 前の工程に運ぶ・つくるよう知らせる札（かんばん）を使うしくみです。ジャストインタイムを実現する道具です。"),
    ("ジャストインタイムとかんばん方式の違いは？", "ジャストインタイムは 必要なものを必要なときに必要な量だけつくり運ぶという考え方（目的）です。かんばん方式は それを実現するための道具（手段）です。"),
    ("ジャストインタイムのデメリットは？", "在庫が少ないので部品が届かないと止まりやすいこと 平準化をせずに入れると前の工程やサプライヤーに負担がかかること 段取り替えの短縮や運搬の工夫が必要なことです。"),
    ("かんばんの枚数はどう決めますか？", "1日の使用量 補充にかかる時間 余裕分 1箱の入り数から決めます。例として 1日400個 補充に半日 1割の余裕 1箱20個なら 400×0.5×1.1÷20＝11枚です。"),
]

# ---------- 英語：mura muri muda ----------
EN6_BODY = '''  <p class="lead"><b>Mura, muri and muda are three related ideas in the Toyota Production System, often called the "3 Ms": mura is unevenness, muri is overburden, and muda is waste — work that adds no value.</b> They are connected — unevenness tends to create overburden, and overburden leads to waste. Below are concrete examples, and why improvement usually starts with mura.</p>

<p>On Japanese shop floors the trio is often remembered as <b>"darari"</b> — the last sounds of mu<b>da</b>, mu<b>ra</b> and mu<b>ri</b> — or simply as the 3 Mu. Either way, people check all three together.</p>
<h2>The three Ms at a glance</h2>
<table><thead><tr><th></th><th>Meaning</th><th>Typical sign</th></tr></thead><tbody>
<tr><td><b>Mura</b> (斑)</td><td>Unevenness in volume, mix or timing</td><td>Busy days and quiet days; end-of-month rush</td></tr>
<tr><td><b>Muri</b> (無理)</td><td>Overburden on people or machines</td><td>Overtime, rushing, skipped checks, breakdowns</td></tr>
<tr><td><b>Muda</b> (無駄)</td><td>Activity that adds no value for the customer</td><td>Inventory, waiting, extra transport, rework</td></tr>
</tbody></table>

<h2>Example 1: a factory with a batched schedule</h2>
<p>A plant builds 100 units a week: model A Monday to Wednesday, B on Thursday, C on Friday. A supplier that makes a part only for B sees zero demand four days a week and 20 sets on Thursday (<b>mura</b>). Assume the people and machine on this part have little other work. On Thursday they work overtime and the machine runs flat out (<b>muri</b>). The rest of the week, the same people and machines sit idle — or keep building stock ahead (<b>muda</b>). If the plant builds 4 B units every day and the supplier ships to match, the day-to-day mura in this example disappears, and the muri and much of the muda go with it. See <a href="../heijunka-examples/">heijunka examples</a>.</p>

<h2>Example 2: an office at month end</h2>
<p>Invoices arrive all month but are processed in the last three days (<b>mura</b>). The team works late and makes mistakes under pressure (<b>muri</b>). Mistakes are reworked and customers wait (<b>muda</b>). Processing a few invoices every day evens out the load.</p>

<h2>Example 3: a restaurant at lunch</h2>
<p>Everyone arrives between 12:00 and 12:30 (<b>mura</b>). The kitchen is overloaded and orders back up (<b>muri</b>). Guests leave without eating, and staff stand idle at 14:00 (<b>muda</b>). Taking reservations at staggered times or preparing some items before the peak spreads the load.</p>

<h2>Why start with mura?</h2>
<p>Many teams attack muda first — cutting inventory, chasing idle time. But if the unevenness stays, the waste comes back: the inventory was there to absorb the waves. Leveling the work (heijunka) and setting standard work so no one is overloaded make the remaining waste easier to see and remove. This is a priority, not a strict order: obvious overburden that risks safety or quality should be fixed right away.</p>

<h2>Common mistakes</h2>
<ul>
<li><b>Treating muda as the only target.</b> Removing buffers without removing the unevenness usually creates muri.</li>
<li><b>Calling everything "waste."</b> Some buffer is a deliberate choice while the unevenness still exists. Decide it on purpose and shrink it as you improve.</li>
<li><b>Ignoring muri.</b> Overburdened people and machines lead to errors, injuries and breakdowns — which become more muda.</li>
</ul>

<h2>See it in a game</h2>
<p><a href="../../games/suppliers-puzzle/">The Supplier's Puzzle</a> is a free browser game set in a fictional scenario inspired by Toyota production. Change the build order and watch how unevenness at the customer turns into capacity and inventory cost at two suppliers — mura, muri and muda in one screen.</p>
<p><a class="btn primary" href="https://ttmtkg.itch.io/the-suppliers-puzzle">Play free</a><a class="btn ghost" href="https://mendomilab.gumroad.com/l/supplier-puzzle-pro">Pro for trainers ($49)</a></p>
<p>Related: <a href="../heijunka-examples/">heijunka examples</a> / <a href="../overproduction-waste/">overproduction waste examples</a> / <a href="../7-wastes-of-lean/">7 wastes of lean</a> / <a href="../lean-simulation-games/">lean simulation games</a> / <a href="../lean-vs-toyota-production-system/">lean vs TPS</a></p>

<h2>About the author</h2>
<p>Tsutomu Takagi (Mendomi Lab). For more than 20 years I worked at a consulting company that is a Toyota subsidiary, teaming up with people who spent long careers on Toyota's shop floors and improving more than 30 factories. If you want help bringing these ideas into your training or workplace, <a href="../../consult/">get in touch</a>.</p>
'''
EN6_FAQ = [
    ("What do mura, muri and muda mean?", "Mura is unevenness, muri is overburden, and muda is activity that adds no value for the customer. Together they are the three Ms of the Toyota Production System."),
    ("What is an example of mura, muri and muda?", "A batched schedule gives a supplier 20 sets of demand on one day and none on the others (mura). That day its people work overtime (muri). On the other days they sit idle or build stock ahead (muda)."),
    ("Which should you eliminate first?", "Usually mura. Leveling the work removes the cause of much of the overburden and waste. Removing waste while the unevenness remains tends to bring the waste back or create overburden."),
    ("How is heijunka related to mura?", "Heijunka (production leveling) is the main way to reduce mura in the production plan, by smoothing volume and mix over time."),
]

if __name__ == '__main__':
    page('ja', 'ja/learn/kanban/', '../../../',
         'かんばん方式とは？わかりやすく解説｜ジャストインタイムとの関係とデメリット｜Mendomi Lab',
         'かんばん方式とは 後の工程が使った分だけを前の工程に知らせるしくみ。ジャストインタイムとの関係 2種類のかんばん 数字で見る流れと枚数の考え方 ルール デメリットと注意点を トヨタの子会社のコンサル会社で20年以上改善をしてきた人が説明します。',
         'かんばん方式とは？ わかりやすく解説（ジャストインタイムとの関係とデメリット）', JA6_BODY, JA6_FAQ,
         [("Mendomi Lab", "https://mendomilab.com/ja/"), ("かんばん方式とは", "https://mendomilab.com/ja/learn/kanban/")],
         None, og='og_ja_sp')
    page('en', 'learn/mura-muri-muda/', '../../',
         'Mura, Muri, Muda: Meaning & Examples | Mendomi Lab',
         'Mura, muri and muda explained with examples from a factory, an office and a restaurant, and why improvement usually starts with mura.',
         'Mura, muri, muda: meaning and examples', EN6_BODY, EN6_FAQ,
         [("Mendomi Lab", "https://mendomilab.com/"), ("Mura, muri, muda", "https://mendomilab.com/learn/mura-muri-muda/")],
         None, og='og_sp')


# ---------- 日本語：飲食店の回転率 ----------
JA7_BODY = '''  <p class="lead"><b>飲食店の回転率は 一定の時間に 1つの席を何人のお客さんが使ったかを表す数字です。計算は「その時間に席に案内したお客さんの数 ÷ 席の数」です。</b>回転率を上げるには お客さんを急がせるより 料理や会計で詰まっている場所（ネック）を見つけて そこを直すほうが効きます。</p>

<h2>回転率の計算方法</h2>
<p><b>回転率 ＝ その時間に席に案内したお客さんの数 ÷ 席の数</b></p>
<p>待ちきれずに帰った人は入れません。時間の終わりをまたいで残った人をどう数えるかは 毎回同じ数え方にそろえます。</p>
<p>例：14席の店で ランチ（11時〜14時）に42人が来たら 42 ÷ 14 ＝ <b>3回転</b>です。</p>
<table><thead><tr><th>席の数</th><th>ランチの客数</th><th>回転率</th></tr></thead><tbody>
<tr><td>14席</td><td>28人</td><td>2回転</td></tr>
<tr><td>14席</td><td>42人</td><td>3回転</td></tr>
<tr><td>14席</td><td>56人</td><td>4回転</td></tr>
</tbody></table>

<h2>回転率の上限はどう決まる？</h2>
<p>1人が席にいる時間（来てから帰るまで）が平均40分なら ランチの3時間＝180分で 1つの席は 180 ÷ 40 ＝ <b>4.5回転</b>が計算上の目安になります（席がずっと埋まっていて 時間の前後にまたがる人を数えない場合）。実際はお客さんが来ない時間や 2人のお客さんが4人席に座ることがあるので これより下がります。</p>
<p>席にいる時間の中身は だいたい次の4つです。</p>
<ul>
<li>注文を聞くまで待つ時間</li>
<li>料理が出るまで待つ時間</li>
<li>食べている時間</li>
<li>会計を待つ時間</li>
</ul>
<p>食べている時間をけずるのは お客さんの満足を下げます。けずるなら <b>待つ時間</b>です。</p>

<h2>回転率を上げる方法：まず「ネック」を見つける</h2>
<p>待つ時間が長いのは どこかがいっぱいになっているからです。時間帯ごとに どこで待ちや仕事がたまっているかを見て いちばん流れを止めている場所から直します。直すと ネックが別の場所に移ることもあります。それが <b>ネック</b>（ボトルネック）です。</p>
<ul>
<li><b>厨房がネック</b>：料理が出るまでが長い。ピークの前に仕込みを進める メニューをしぼる 調理の順番をそろえる。</li>
<li><b>ホールがネック</b>：注文を聞く 片づけるのが追いつかず 空いた席にお客さんを案内できない。</li>
<li><b>レジがネック</b>：食べ終わったお客さんが席で待つ 列ができる。先に会計する 支払い方法をふやす。</li>
</ul>
<p>大事なのは <b>ネックでない場所に人を足しても 回転率は上がらない</b>ことです。厨房がネックのときにホールの人をふやしても 料理が出る速さは変わりません。効果の少ない場所への増員は 人件費に見合わないことが多いです。くわしくは <a href="../bottleneck/">ボトルネック工程とは？</a> にまとめています。</p>

<h2>やってはいけないこと</h2>
<ul>
<li><b>お客さんを急がせる</b>：食べている時間を短くすると リピートが減り 長い目で見た売上が下がるおそれがあります。</li>
<li><b>「忙しいなら人をふやせ」</b>：ネックでない持ち場に人を足すと 人件費がふえて利益は下がります。</li>
<li><b>回転率だけを見る</b>：回転率が上がっても 客単価や人件費しだいで利益は変わります。回転率と人件費を いっしょに見てください。</li>
</ul>

<h2>ゲームで試す：回らないパスタ屋</h2>
<p><a href="../../games/pasta/">回らないパスタ屋</a> は 14席・ランチ11時〜14時の店で 厨房 ホール レジの人数を変えて ランチの利益がいちばん大きくなる人数を見つける無料のブラウザゲームです。いまは「忙しいなら人をふやせ」で7人で回しています。どこがネックかを見つけて 人数を合わせると 帰ってしまうお客さんと利益がどう変わるかを試せます。</p>
<p><a class="btn primary" href="../../play/pasta/">回らないパスタ屋で遊ぶ</a></p>
<p>あわせて読む：<a href="../bottleneck/">ボトルネック工程とは？</a> ／ <a href="../takt-time/">タクトタイムとサイクルタイムの違い</a> ／ <a href="../kenshu-game/">研修に使えるゲーム</a></p>

<h2>書いた人</h2>
<p>高木 務（Mendomi Lab）。トヨタの子会社のコンサル会社で20年以上 トヨタの現場で長く働いた人たちと組んで 30社以上の工場の改善をしてきました。工場で使う「ネックを見つけて合わせる」考え方は 飲食店にもそのまま使えます。お店に合わせた相談は <a href="../../consult/">相談する</a> からどうぞ。</p>
'''
JA7_FAQ = [
    ("飲食店の回転率の計算方法は？", "その時間に来たお客さんの数 ÷ 席の数 です。14席の店にランチで42人来たら 3回転です。"),
    ("ランチの回転率の目安は？", "どの店にも当てはまる目標の数字はありません。業態 席にいる時間 席の組み合わせで変わります。平均40分ならランチ3時間で計算上は4.5回転が目安です。同じ曜日・時間帯の自分の店の回転率を 客単価や利益といっしょにくらべてください。"),
    ("回転率を上げるにはどうすればいい？", "お客さんを急がせるのではなく 待つ時間をへらします。厨房 ホール レジのどこがいっぱいになっているか（ネック）を見つけて そこを直すのが近道です。"),
    ("人をふやせば回転率は上がりますか？", "ネックの持ち場に足せば上がることがあります。ネックでない持ち場に足しても回転率はほとんど変わらず 人件費に見合わないことが多いです。"),
]

# ---------- 英語：7 wastes ----------
EN7_BODY = '''  <p class="lead"><b>The 7 wastes of lean (muda) are overproduction, waiting, transportation, over-processing, inventory, motion and defects.</b> They come from the Toyota Production System. Each is an activity or a condition that uses time or money but creates no value for the customer. Some non-value-adding work is still necessary (safety checks, legal requirements), so the goal is to remove the unnecessary part while protecting safety and quality. Below is a simple example of each, in a factory and outside one.</p>

<h2>The 7 wastes with examples</h2>
<table><thead><tr><th>Waste</th><th>Factory example</th><th>Office / service example</th></tr></thead><tbody>
<tr><td><b>Overproduction</b></td><td>Building 120 parts when the next step needs 100 today</td><td>Printing 50 reports when 10 people read them</td></tr>
<tr><td><b>Waiting</b></td><td>An operator watching a machine that could run on its own</td><td>A form waiting three days for a signature</td></tr>
<tr><td><b>Transportation</b></td><td>Moving parts to a warehouse and back to the line</td><td>Emailing a file through four people before it reaches the person who acts on it</td></tr>
<tr><td><b>Over-processing</b></td><td>Polishing a hidden surface beyond what function or quality requires</td><td>Re-typing data already in another system</td></tr>
<tr><td><b>Inventory</b></td><td>A pile of work in progress between two processes</td><td>A backlog of tickets nobody is working on</td></tr>
<tr><td><b>Motion</b></td><td>Walking ten steps to fetch a tool for every unit</td><td>Searching shared drives for the latest version</td></tr>
<tr><td><b>Defects</b></td><td>Scrap and rework</td><td>An invoice sent with the wrong amount</td></tr>
</tbody></table>
<p>An easy way to remember them is <b>TIMWOOD</b>: Transportation, Inventory, Motion, Waiting, Over-processing, Overproduction, Defects. Some lists add an eighth — unused skills of people.</p>

<h2>Why overproduction is called the worst</h2>
<p>Overproduction creates the others. Extra parts need to be moved (transportation), stored (inventory) and searched for (motion), and defects in them are found late. It also hides problems: when there is always stock, nobody notices that a machine is slow or a step is unstable. See <a href="../overproduction-waste/">overproduction waste examples</a>.</p>

<h2>How to find the 7 wastes in your own work</h2>
<ol>
<li>Follow one item (a part, a document, an order) from start to finish.</li>
<li>Write down every step and sort it into: value-adding, necessary but not value-adding, and pure waste.</li>
<li>For each pure-waste step, ask which of the seven wastes it is, and remove those first.</li>
<li>Use overproduction and waiting as starting points, then trace the cause on the floor. Check for unevenness and overburden (<a href="../mura-muri-muda/">mura and muri</a>) as well as breakdowns and long changeovers.</li>
</ol>

<h2>See waste in a game</h2>
<p><a href="../../games/overproduction-factory/">Overproduction Factory</a> is a free browser game where you run a small line and watch what happens when every process builds as much as it can — inventory piles up and lead time stretches. <a href="../../games/suppliers-puzzle/">The Supplier's Puzzle</a> shows how an uneven build order turns into waiting and inventory at suppliers.</p>
<p><a class="btn primary" href="../../games/overproduction-factory/">Overproduction Factory</a><a class="btn ghost" href="../lean-simulation-games/">All lean games</a></p>
<p>Related: <a href="../overproduction-waste/">overproduction waste examples</a> / <a href="../mura-muri-muda/">mura, muri, muda</a> / <a href="../takt-time-vs-cycle-time/">takt time vs cycle time</a> / <a href="../lean-vs-toyota-production-system/">lean vs TPS</a></p>

<h2>About the author</h2>
<p>Tsutomu Takagi (Mendomi Lab). For more than 20 years I worked at a consulting company that is a Toyota subsidiary, teaming up with people who spent long careers on Toyota's shop floors and improving more than 30 factories. If you want help bringing these ideas into your training or workplace, <a href="../../consult/">get in touch</a>.</p>
'''
EN7_FAQ = [
    ("What are the 7 wastes of lean?", "Overproduction, waiting, transportation, over-processing, inventory, motion and defects. They come from the Toyota Production System and are often remembered as TIMWOOD."),
    ("Which of the 7 wastes is the worst?", "Overproduction is usually called the worst, because it creates the other wastes (inventory, transportation, motion) and hides problems."),
    ("Do the 7 wastes apply outside manufacturing?", "Yes. Offices, hospitals and restaurants have the same wastes: waiting for approvals, re-typing data, backlogs, searching for files and errors that need rework."),
    ("What is the 8th waste?", "Some lists add unused skills or talent of people. It is not in the original seven from Toyota, but it is widely used."),
]

if __name__ == '__main__':
    page('ja', 'ja/learn/kaitenritsu/', '../../../',
         '飲食店の回転率とは？計算方法と上げる方法（ネックの見つけ方）｜Mendomi Lab',
         '飲食店の回転率の計算方法（来店客数÷席数）と上限の考え方 回転率を上げる方法を 厨房・ホール・レジのネック（ボトルネック）の見つけ方から説明します。無料ゲーム「回らないパスタ屋」で試せます。',
         '飲食店の回転率とは？ 計算方法と上げる方法', JA7_BODY, JA7_FAQ,
         [("Mendomi Lab", "https://mendomilab.com/ja/"), ("飲食店の回転率とは", "https://mendomilab.com/ja/learn/kaitenritsu/")],
         None, og='og_ja_pasta')
    page('en', 'learn/7-wastes-of-lean/', '../../',
         'The 7 Wastes of Lean with Examples | Mendomi Lab',
         'The 7 wastes of lean (TIMWOOD) with a factory and an office example for each, why overproduction is the worst, and how to find waste in your work.',
         'The 7 wastes of lean, with examples', EN7_BODY, EN7_FAQ,
         [("Mendomi Lab", "https://mendomilab.com/"), ("7 wastes of lean", "https://mendomilab.com/learn/7-wastes-of-lean/")],
         None, og='og_of')

# ---------- 日本語：リーン生産方式とトヨタ生産方式の違い ----------
JA8_BODY = '''  <p class="lead"><b>トヨタ生産方式（TPS）は トヨタが自分の工場で長い時間をかけて作り上げたやり方です。リーン生産方式は それをアメリカの研究者が調べて ほかの会社でも使えるように言葉にまとめたものです。</b>中身の多くは同じですが 生まれ方と 何を大事にするかに ちがいがあります。</p>

<h2>ひと目でわかる違い</h2>
<table><thead><tr><th></th><th>トヨタ生産方式（TPS）</th><th>リーン生産方式</th></tr></thead><tbody>
<tr><th>生まれたところ</th><td>トヨタの工場（大野耐一さんたちが中心）</td><td>アメリカの研究（MITの自動車産業の調査）</td></tr>
<tr><th>名前ができた時期</th><td>戦後から1970年代にかけて形になった</td><td>1988年の論文で「lean production」という言葉が使われ 1990年の本『The Machine That Changed the World』で広まった</td></tr>
<tr><th>柱</th><td>ジャスト・イン・タイムと自働化（ニンベンのついた自働化）</td><td>価値・価値の流れ・流れ・引っぱり・完ぺきの5原則（1996年の本『Lean Thinking』）</td></tr>
<tr><th>大事にすること</th><td>現場で問題を見えるようにして 人が考えて改善を続けること</td><td>ムダを減らして 顧客にとっての価値の流れをつくること</td></tr>
<tr><th>使われる場所</th><td>トヨタとそのグループ・取引先が中心</td><td>製造業のほか 病院・ソフトウェア・事務などにも広がった</td></tr>
</tbody></table>

<h2>同じところ</h2>
<ul>
<li>つくりすぎ・在庫・待ちなどの <a href="../tsukurisugi-no-muda/">ムダ</a> を減らす</li>
<li>後工程が使った分だけ前工程がつくる（引っぱり）。<a href="../kanban/">かんばん</a> はその道具</li>
<li>注文の量と種類をならす（<a href="../heijunka/">平準化</a>）</li>
<li>客が求める速さ（<a href="../takt-time/">タクトタイム</a>）に合わせてつくる</li>
</ul>

<h2>ちがいが出やすいところ</h2>
<p><b>1. 道具から入るか 考え方から入るか</b><br>リーンとして入ってくると かんばん・5S・見える化などの <b>道具</b> から始まることが多いです。トヨタ生産方式では 道具は 問題を見えるようにして改善するための手段です。道具だけまねても 問題を見て直す人がいないと続きません。</p>
<p><b>2. 自働化の扱い</b><br>トヨタ生産方式のもう1本の柱「自働化」は 異常があったら機械や人が止めて 不良を後に流さない考え方です。リーンの説明では ジャスト・イン・タイムやムダ取りにくらべて 小さく扱われることがあります。</p>
<p><b>3. 人を育てることの重さ</b><br>トヨタ生産方式は 改善を続ける人を育てることと一体です。トヨタの現場で長く働いた人たちと仕事をして わたしが強く感じたのは トヨタの強さの源は 上司や先輩が部下を気にかけて育てる「めんどう見」にあるということでした。</p>

<h2>どちらの言葉を使えばいい？</h2>
<p>社内で話すときは どちらでもかまいません。大事なのは 名前より <b>何を目指すか</b> をそろえることです。「在庫を減らす」だけを目標にすると 欠品や残業がふえることがあります。顧客が求める量とタイミングに合わせてつくる という目的をはっきりさせてから 道具を選んでください。</p>

<h2>ゲームで試す</h2>
<p>どちらの考え方も 体を動かすとわかりやすくなります。</p>
<ul>
<li><a href="../../games/factory/">造りすぎ工場</a>：「止めるな・つくれ」で流すと 全部出荷しても赤字になる。ジャスト・イン・タイムの意味を体験できます</li>
<li><a href="../../games/supplier/">サプライヤーのパズル</a>：組み立ての順番を変えると 部品会社のコストが変わる。平準化の意味を体験できます</li>
</ul>
<p>あわせて読む：<a href="../tsukurisugi-no-muda/">造りすぎのムダとは？</a> ／ <a href="../kanban/">かんばん方式とは？</a> ／ <a href="../kenshu-game/">研修に使えるゲーム</a></p>

<h2>書いた人</h2>
<p>高木 務（Mendomi Lab）。トヨタの子会社のコンサル会社で20年以上 トヨタの現場で長く働いた人たちと組んで 30社以上の工場の改善をしてきました。研修や職場への取り入れ方の相談は <a href="../../consult/">相談する</a> からどうぞ。</p>
'''
JA8_FAQ = [
    ("リーン生産方式とトヨタ生産方式は同じものですか？", "中身の多くは同じです。トヨタ生産方式はトヨタが作り上げたやり方で リーン生産方式はそれをアメリカの研究者が調べて ほかの会社でも使えるようにまとめたものです。"),
    ("リーンという言葉はいつできましたか？", "1988年の論文で「lean production」という言葉が使われ 1990年の本『The Machine That Changed the World』で広まりました。"),
    ("トヨタ生産方式の2本の柱は何ですか？", "ジャスト・イン・タイムと自働化です。自働化は 異常があったら止めて 不良を後に流さない考え方です。"),
    ("リーンを入れてもうまくいかないのはなぜですか？", "道具だけをまねて 問題を見て直す人が育っていないことが多いです。目的をそろえ 改善を続ける人を育てることが先です。"),
]

# ---------- 英語：Lean vs TPS ----------
EN8_BODY = '''  <p class="lead"><b>The Toyota Production System (TPS) is the way Toyota built up in its own plants over decades. Lean is the name researchers in the United States gave to it when they studied it and described it so other companies could use it.</b> Most of the content is the same. The differences are in where each came from and what each tends to emphasize.</p>

<h2>The difference at a glance</h2>
<table><thead><tr><th></th><th>Toyota Production System (TPS)</th><th>Lean</th></tr></thead><tbody>
<tr><th>Origin</th><td>Toyota's plants (Taiichi Ohno and colleagues)</td><td>US research (the MIT study of the world auto industry)</td></tr>
<tr><th>When the name appeared</th><td>Took shape from the post-war years to the 1970s</td><td>"Lean production" was used in a 1988 paper and popularized by the 1990 book <em>The Machine That Changed the World</em></td></tr>
<tr><th>Pillars</th><td>Just-in-time and jidoka (automation with a human touch)</td><td>Five principles: value, value stream, flow, pull, perfection (<em>Lean Thinking</em>, 1996)</td></tr>
<tr><th>Emphasis</th><td>Making problems visible on the floor and developing people who keep improving</td><td>Removing waste and creating a flow of value for the customer</td></tr>
<tr><th>Where it is used</th><td>Mainly Toyota, its group companies and suppliers</td><td>Manufacturing, and also hospitals, software, offices and services</td></tr>
</tbody></table>

<h2>What they share</h2>
<ul>
<li>Reducing waste such as <a href="../overproduction-waste/">overproduction</a>, inventory and waiting (see <a href="../7-wastes-of-lean/">the 7 wastes</a>)</li>
<li>Pull: an earlier process makes only what the next process used</li>
<li>Leveling volume and mix (<a href="../heijunka-examples/">heijunka</a>)</li>
<li>Producing at the customer's pace (<a href="../takt-time-vs-cycle-time/">takt time</a>)</li>
</ul>

<h2>Where they tend to differ</h2>
<p><b>1. Tools first or thinking first</b><br>When lean is introduced, it often starts with <b>tools</b>: kanban, 5S, visual management. In TPS the tools are means to make problems visible so people can fix them. Copying the tools without people who see and solve problems rarely lasts.</p>
<p><b>2. Jidoka</b><br>The second pillar of TPS, jidoka, means stopping a machine or a line when something is abnormal so defects do not flow downstream. Lean summaries sometimes give it less weight than just-in-time and waste removal.</p>
<p><b>3. Developing people</b><br>TPS cannot be separated from developing people who keep improving. Working with people who spent long careers on Toyota's shop floors, I came to see that much of Toyota's strength comes from what they call <em>mendomi</em>: leaders and seniors who genuinely look after and develop the people around them.</p>

<h2>Which word should you use?</h2>
<p>Either is fine. What matters is agreeing on the goal. If the only goal is "less inventory", you may get stock-outs and overtime. Make the purpose clear first, producing what the customer needs when they need it, and then choose the tools.</p>

<h2>Try it in a game</h2>
<ul>
<li><a href="../../games/overproduction-factory/">Overproduction Factory</a>: follow "never stop, keep building", ship every unit, and still lose money. A hands-on way to feel just-in-time.</li>
<li><a href="../../games/suppliers-puzzle/">The Supplier's Puzzle</a>: change the build order and watch the supplier's costs change. A hands-on way to feel heijunka.</li>
</ul>
<p>Related: <a href="../7-wastes-of-lean/">7 wastes of lean</a> / <a href="../mura-muri-muda/">mura, muri, muda</a> / <a href="../lean-simulation-games/">lean simulation games</a></p>

<h2>About the author</h2>
<p>Tsutomu Takagi (Mendomi Lab). For more than 20 years I worked at a consulting company that is a Toyota subsidiary, teaming up with people who spent long careers on Toyota's shop floors and improving more than 30 factories. If you want help bringing these ideas into your training or workplace, <a href="../../consult/">get in touch</a>.</p>
'''
EN8_FAQ = [
    ("Is lean the same as the Toyota Production System?", "Mostly, yes. TPS is the system Toyota developed. Lean is the name US researchers gave it when they studied TPS and described it for other companies."),
    ("Who coined the term lean production?", "It was used in a 1988 paper from the MIT auto industry research program and popularized by the 1990 book The Machine That Changed the World."),
    ("What are the two pillars of TPS?", "Just-in-time and jidoka. Jidoka means stopping when something is abnormal so defects do not flow to the next process."),
    ("Why do lean programs fail?", "Often because tools are copied without developing people who see and solve problems. Agree on the purpose first and develop people who keep improving."),
]

if __name__ == '__main__':
    page('ja', 'ja/learn/lean-tps-chigai/', '../../../',
         'リーン生産方式とトヨタ生産方式の違いは？｜Mendomi Lab',
         'リーン生産方式とトヨタ生産方式（TPS）の違いを 生まれたところ・柱・大事にすることの表で説明します。同じところ・ちがいが出やすいところ・言葉の選び方も。無料ゲームで体験できます。',
         'リーン生産方式とトヨタ生産方式の違い', JA8_BODY, JA8_FAQ,
         [("Mendomi Lab", "https://mendomilab.com/ja/"), ("リーンとトヨタ生産方式の違い", "https://mendomilab.com/ja/learn/lean-tps-chigai/")],
         None, og='og_ja_of')
    page('en', 'learn/lean-vs-toyota-production-system/', '../../',
         'Lean vs Toyota Production System: Differences | Mendomi Lab',
         'Lean vs the Toyota Production System (TPS): origin, pillars and emphasis compared in one table, what they share, where they differ, and which word to use.',
         'Lean vs Toyota Production System: what is the difference?', EN8_BODY, EN8_FAQ,
         [("Mendomi Lab", "https://mendomilab.com/"), ("Lean vs TPS", "https://mendomilab.com/learn/lean-vs-toyota-production-system/")],
         None, og='og_of')
    page('en', 'learn/what-is-mendomi/', '../../',
         'What Does Mendomi (面倒見) Mean? Looking After People at Toyota | Mendomi Lab',
         'Mendomi (面倒見) is a Japanese word for looking after people. What it means, how to pronounce it, how it shows up in the Toyota Production System, and how leaders can practice it.',
         'What does mendomi (面倒見) mean?', EN9_BODY, EN9_FAQ,
         [("Mendomi Lab", "https://mendomilab.com/"), ("What is mendomi", "https://mendomilab.com/learn/what-is-mendomi/")],
         None)
