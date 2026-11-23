#!/usr/bin/env python3
"""解説ページ（learn）を作る。python3 tools/learn_pages.py"""
import json, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

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
JA_BODY = '''  <p class="lead"><b>平準化とは 造る量と種類を 日ごと・時間ごとにならして造ることです。</b>同じものを何日もまとめて造るのではなく 毎日 少しずついろいろな種類を造ります。トヨタ生産方式（TPS）の土台の1つで ジャストインタイムとかんばんは 平準化ができていることが前提になっています。</p>

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
<p>トヨタではこれを ムラ（ばらつき）がムリ（無理な負荷）につながり ムリがムダ（使わない人と設備・在庫）につながる と説明します。平準化は 生産計画のムラを小さくする手段です。</p>

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

<h2>About the author</h2>
<p>Tsutomu Takagi (Mendomi Lab). For more than 20 years I worked at a consulting company that is a Toyota subsidiary, teaming up with people who spent long careers on Toyota's shop floors and improving more than 30 factories. If you want help bringing these ideas into your training or workplace, <a href="../../consult/">get in touch</a>.</p>
'''
EN_FAQ = [
    ("What is a simple heijunka example?", "A plant that builds 60 A, 20 B and 20 C in a week can run A for three days, then B, then C — or build 12 A, 4 B and 4 C every day in the sequence A B A C A. The second plan is heijunka."),
    ("What is the difference between heijunka and leveling?", "They are the same idea. Heijunka is the Japanese term used in the Toyota Production System for leveling production volume and mix."),
    ("What does a heijunka box do?", "It holds kanban cards in slots by time interval and model, in the leveled order, so work is released to the line at a steady pace."),
    ("How is heijunka related to mura, muri and muda?", "Uneven schedules (mura) overburden people and machines (muri), which leads to waste such as idle capacity and inventory (muda). Heijunka reduces that unevenness in the plan itself."),
]

if __name__ == '__main__':
    page('ja', 'ja/learn/heijunka/', '../../../',
         '平準化とは？わかりやすく解説｜標準化との違いとトヨタの例｜Mendomi Lab',
         '平準化とは 造る量と種類を日ごとにならして造ること。数字の例で まとめて造るとサプライヤーに何が起きるか 標準化との違い 現場でよくある誤解を トヨタの子会社のコンサル会社で20年以上改善をしてきた人が説明します。',
         '平準化とは？ わかりやすく解説（標準化との違いとトヨタの例）', JA_BODY, JA_FAQ,
         [("Mendomi Lab", "https://mendomilab.com/ja/"), ("平準化とは", "https://mendomilab.com/ja/learn/heijunka/")],
         'learn/heijunka-examples/')
    page('en', 'learn/heijunka-examples/', '../../',
         'Heijunka Examples: Production Leveling in Real Life (with Numbers) | Mendomi Lab',
         'Concrete heijunka examples with numbers: a batched vs. leveled week, what the supplier sees, how a heijunka box works, and examples outside the factory. Written by a consultant with 20+ years at a Toyota subsidiary consulting company.',
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
         'Lean Simulation Games Online: Free Browser Games for Lean Training | Mendomi Lab',
         'Free browser-based lean simulation games for training and classes: overproduction, takt time and heijunka. No install, 30–90 minute workshops, Pro versions for trainers. Built by a 20+ year consultant at a Toyota subsidiary.',
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
<p>無料版で遊ぶことも 研修で使うこともできます。造りすぎ工場とサプライヤーのパズルには 研修をする人向けのPro版があり 注文や工数 コストなどを自分の職場に合わせて変えられ 進行役の手引きもつきます（回らないパスタ屋は無料版だけです）。日本語のPro版は準備中です。研修に合わせた作り直しや 進め方の相談は <a href="../../consult/">相談する</a> からどうぞ（最初の1往復は無料）。</p>

<h2>書いた人</h2>
<p>高木 務（Mendomi Lab）。トヨタの子会社のコンサル会社で20年以上 トヨタの現場で長く働いた人たちと組んで 30社以上の工場の改善をしてきました。</p>
<p>あわせて読む：<a href="../tsukurisugi-no-muda/">造りすぎのムダとは？</a> ／ <a href="../heijunka/">平準化とは？</a></p>
'''
JA3_FAQ = [
    ("無料で研修に使えますか？", "使えます。無料版はブラウザでそのまま遊べて 登録もいりません。研修をする人向けのPro版は 設定を自分の職場に合わせて変えられ 進行役の手引きがつきます（日本語版は準備中）。"),
    ("リーンやトヨタ生産方式にくわしくなくても進行できますか？", "はじめてでも このページの手順で進められます。まずそのまま動かして 結果を見てから 何が起きたかを問いかけてください。"),
    ("オンライン研修でも使えますか？", "使えます。ブラウザで動くので 画面を共有すれば オンラインでも教室でも使えます。"),
    ("新人研修に向いているのはどれですか？", "造りすぎ工場です。必要な量を超えて造ると 在庫やコストがどう増えるのかを 短い時間で体験できます。"),
]

# ---------- 英語：overproduction waste examples ----------
EN3_BODY = '''  <p class="lead"><b>Overproduction waste means making more than the customer needs, or making it earlier than needed.</b> It is one of the seven wastes of the Toyota Production System, and it is often called the worst one, because it creates the other wastes and hides problems. Below are concrete overproduction waste examples — in a factory, in an office and in services — with numbers.</p>

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
<p>More games: <a href="../lean-simulation-games/">lean simulation games for training</a>. Related: <a href="../heijunka-examples/">heijunka examples</a> / <a href="../takt-time-vs-cycle-time/">takt time vs cycle time</a>.</p>

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
         'Overproduction Waste Examples: Factory, Office and Service (with Numbers) | Mendomi Lab',
         'Overproduction waste examples with numbers: a line that never stops, piles between processes, office batch printing and restaurant prep. Why it is called the worst of the seven wastes, how to spot it and how to reduce it.',
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
<p>あわせて読む：<a href="../tsukurisugi-no-muda/">造りすぎのムダとは？</a> ／ <a href="../heijunka/">平準化とは？</a> ／ <a href="../kenshu-game/">製造業の研修に使えるゲーム</a></p>

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
<p>Related: <a href="../overproduction-waste/">overproduction waste examples</a> / <a href="../heijunka-examples/">heijunka examples</a> / <a href="../lean-simulation-games/">lean simulation games</a></p>

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
         'Takt Time vs Cycle Time: Formula, Examples and Staffing | Mendomi Lab',
         'Takt time vs cycle time explained with numbers: the takt time formula, what the comparison tells you, how to calculate people needed, and how lead time differs. Written by a consultant with 20+ years at a Toyota subsidiary consulting company.',
         'Takt time vs cycle time: formula, examples and staffing', EN4_BODY, EN4_FAQ,
         [("Mendomi Lab", "https://mendomilab.com/"), ("Takt time vs cycle time", "https://mendomilab.com/learn/takt-time-vs-cycle-time/")],
         'ja/learn/takt-time/', og='og_of')
