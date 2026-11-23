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
<li><b>New to lean, or one session only:</b> start with Overproduction Factory. It opens the most basic question — are we building what the customer needs?</li>
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
         None, og='og_ja_of')
    page('en', 'learn/lean-simulation-games/', '../../',
         'Lean Simulation Games Online: Free Browser Games for Lean Training | Mendomi Lab',
         'Free browser-based lean simulation games for training and classes: overproduction, takt time and heijunka. No install, 30–90 minute workshops, Pro versions for trainers. Built by a 20+ year consultant at a Toyota subsidiary.',
         'Lean simulation games online: free browser games for lean training', EN2_BODY, EN2_FAQ,
         [("Mendomi Lab", "https://mendomilab.com/"), ("Lean simulation games", "https://mendomilab.com/learn/lean-simulation-games/")],
         None, og='og')
