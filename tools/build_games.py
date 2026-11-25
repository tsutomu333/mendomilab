import json, os, html
ROOT='/home/claude/mendomilab'
GTAG=next(l for l in open(f'{ROOT}/about/index.html').read().split('\n') if 'G-SGX5EJT1CN' in l)  # the analytics <script> line
SHIP={"@type":"OfferShippingDetails","shippingRate":{"@type":"MonetaryAmount","value":"0","currency":"JPY"},"shippingDestination":{"@type":"DefinedRegion","addressCountry":"JP"},"deliveryTime":{"@type":"ShippingDeliveryTime","handlingTime":{"@type":"QuantitativeValue","minValue":0,"maxValue":0,"unitCode":"DAY"},"transitTime":{"@type":"QuantitativeValue","minValue":0,"maxValue":0,"unitCode":"DAY"}}}
RET={"@type":"MerchantReturnPolicy","applicableCountry":"JP","returnPolicyCategory":"https://schema.org/MerchantReturnNotPermitted","merchantReturnLink":"https://mendomilab.com/ja/tokushoho/"}

OG={'games/overproduction-factory/':'og_of.png','games/suppliers-puzzle/':'og_sp.png','ja/games/factory/':'og_ja_of.png','ja/games/supplier/':'og_ja_sp.png','ja/games/pasta/':'og_ja_pasta.png','ja/games/kadou/':'og.png','games/availability-vs-utilization/':'og.png'}
PRODUCTS={
 'games/availability-vs-utilization/':('Stalled Factory, Paused Factory Pro','Pro edition with settings for your own plant and a facilitator guide (PDF). A browser game on availability vs. utilization in the Toyota Production System.',[('Personal',29,'https://buy.stripe.com/4gMeV523M0AD5Xgb0jcV208'),('Team',99,'https://buy.stripe.com/9B68wHcIq4QTclEd8rcV209')],'USD'),
 'ja/games/kadou/':('止まる工場・止める工場 Pro 日本語版','稼働時間 能力 故障 注文 価格を自分の工場に合わせて変えられるPro版と進行役の手引き（PDF）。可動率と稼働率のちがいを体験するブラウザのゲーム。',[('1人用',4500,'https://buy.stripe.com/7sY8wH23M83571k7O7cV206'),('チーム用',15000,'https://buy.stripe.com/28E9ALfUC2ILclE6K3cV207')]),
 'ja/games/factory/':('造りすぎ工場 Pro 日本語版','数字を変えられる設定パネルつきのPro版と進行役の手引き（PDF）。研修や授業で使えるブラウザのゲーム。',[('1人用',4500,'https://buy.stripe.com/5kQ00b8sa979gBU8SbcV202'),('チーム用',15000,'https://buy.stripe.com/9B6aEPbEm835fxQ9WfcV203')]),
 'ja/games/supplier/':('サプライヤーのパズル Pro 日本語版','計算式が見えるPro版と進行役の手引き（PDF）。平準化を部品会社の側から体験するブラウザのゲーム。',[('1人用',7500,'https://buy.stripe.com/eVq7sD6k23MPclEd8rcV204'),('チーム用',23000,'https://buy.stripe.com/6oU4greQy5UXetM1pJcV205')]),
}
def page(lang, path, title, desc, h1, lead, sections, faqs, buttons, alt_en, alt_ja, crumb_name):
    depth=path.strip('/').count('/')+1
    up='../'*depth
    canon=f'https://mendomilab.com/{path}'
    if lang=='en':
        nav=f'<nav><a href="{up}#games">Games</a><a href="{up}consult/">Work with me</a><a href="{up}about/">About</a><a class="lang" href="{up}{alt_ja}" hreflang="ja">日本語</a></nav>'
        home=up; foot=f'''<footer class="site"><div class="wrap">
  <div><a href="{up}about/">About</a><a href="{up}consult/">Work with me</a><a href="{up}privacy/">Privacy</a></div>
  <div>Mendomi Lab is a project of A&amp;T Works.</div>
  <div>© 2026 Mendomi Lab. Not affiliated with Toyota Motor Corporation or OJT Solutions.</div>
</div></footer>'''
        crumb_home='Mendomi Lab'; games_lbl='Games'; faq_h='Questions'
    else:
        nav=f'<nav><a href="{up}ja/#games">ゲーム</a><a href="{up}ja/consult/">相談する</a><a href="{up}ja/about/">Mendomi Labについて</a><a class="lang" href="{up}{alt_en or ''}" hreflang="en">English</a></nav>'
        home=up+'ja/'; foot=f'''<footer class="site"><div class="wrap">
  <div><a href="{up}ja/about/">Mendomi Labについて</a><a href="{up}ja/consult/">相談する</a><a href="{up}ja/privacy/">プライバシー</a><a href="{up}ja/tokushoho/">特定商取引法にもとづく表記</a></div>
  <div>Mendomi Lab は A&amp;T Works のプロジェクトです</div>
  <div>© 2026 Mendomi Lab. トヨタ自動車株式会社・株式会社OJTソリューションズとは関係ありません。</div>
</div></footer>'''
        crumb_home='Mendomi Lab'; games_lbl='ゲーム'; faq_h='よくある質問'
    alts=(f'<link rel="alternate" hreflang="en" href="https://mendomilab.com/{alt_en}">\n<link rel="alternate" hreflang="ja" href="https://mendomilab.com/{alt_ja}">') if alt_en else ''
    body=''.join(f'<h2>{h}</h2>\n{c}\n' for h,c in sections)
    faq_html=''.join(f'<h3>{q}</h3>\n<p>{a}</p>\n' for q,a in faqs)
    btn=''.join(f'<a class="btn {cls}" href="{href}">{t}</a>' for t,href,cls in buttons)
    ld=[{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":html.unescape(a.replace('<b>','').replace('</b>',''))}} for q,a in faqs]},
        {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
          {"@type":"ListItem","position":1,"name":crumb_home,"item":'https://mendomilab.com/'+('' if lang=='en' else 'ja/')},
          {"@type":"ListItem","position":2,"name":games_lbl,"item":'https://mendomilab.com/'+('' if lang=='en' else 'ja/')+'#games'},
          {"@type":"ListItem","position":3,"name":crumb_name,"item":canon}]}]
    if path in PRODUCTS:
        n,d,offs=PRODUCTS[path][:3]; cur=PRODUCTS[path][3] if len(PRODUCTS[path])>3 else "JPY"
        ld.append({"@context":"https://schema.org","@type":"Product","name":n,"description":d,"image":f"https://mendomilab.com/assets/social/{OG[path]}","brand":{"@type":"Brand","name":"Mendomi Lab"},
          "offers":[{"@type":"Offer","name":on,"price":str(pr),"priceCurrency":cur,"availability":"https://schema.org/InStock","url":u,"seller":{"@type":"Organization","name":"A&T Works"},**({"shippingDetails":SHIP,"hasMerchantReturnPolicy":RET} if cur=="JPY" else {})} for on,pr,u in offs]})
    out=f'''<!DOCTYPE html>
<html lang="{lang}">
<head>
{GTAG}
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<link rel="icon" href="{up}favicon.svg" type="image/svg+xml">
<meta name="description" content="{desc}">
<link rel="canonical" href="{canon}">
{alts}
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{canon}">
<meta property="og:type" content="article">
<meta property="og:image" content="https://mendomilab.com/assets/social/{OG[path]}">
<meta name="twitter:card" content="summary_large_image">
<link rel="stylesheet" href="{up}assets/site.css">
<script type="application/ld+json">{json.dumps(ld,ensure_ascii=False)}</script>
</head>
<body>
<header class="site"><div class="wrap">
  <a class="logo" href="{home}"><span class="mark">面</span><span class="name">Mendomi<small>Lab</small></span></a>
  {nav}
</div></header>

<main class="wrap prose">
  <p class="crumb" style="font-size:.85em;opacity:.7"><a href="{home}">{crumb_home}</a> › <a href="{home}#games">{games_lbl}</a> › {crumb_name}</p>
  <h1>{h1}</h1>
  <p class="lead">{lead}</p>
  <p>{btn}</p>
{body}
<h2>{faq_h}</h2>
{faq_html}
  <p>{btn}</p>
</main>

{foot}
</body>
</html>
'''
    os.makedirs(f'{ROOT}/{path}',exist_ok=True)
    open(f'{ROOT}/{path}index.html','w').write(out)

# ---------- EN: Overproduction Factory ----------
page('en','games/overproduction-factory/',
 'Overproduction Factory | Lean Training Game on Overproduction and Takt Time | Mendomi Lab',
 'A free lean training game about overproduction, takt time and standard WIP. Run a factory simulation, then talk about what really drives profit.',
 'Overproduction Factory: a lean game about overproduction',
 'Four processes, one daily order of 480 units. The old rule on the floor is "never let a process stop, build as much as you can." Follow it and every ordered unit ships — yet the day ends in a loss. Players find the crew and work-in-process that actually make a profit.',
 [('What participants learn','<ul><li>Why building more than the customer needs lowers profit, even when every process looks busy.</li><li><b>Takt time</b>: the pace set by customer demand (available time ÷ demand).</li><li>How to set <b>people per process</b> from work time ÷ takt time.</li><li><b>Standard WIP</b>: the minimum stock that keeps the line flowing, and why piles grow when nobody defines it.</li><li>Why the game, following the Toyota Production System, counts stock with no buyer as worth nothing — and how book profit can hide the problem.</li></ul>'),
  ('Who it is for and how long it takes','<table><thead><tr><th>Format</th><th>Time</th><th>Best for</th></tr></thead><tbody><tr><td>Quick demo</td><td>30 min</td><td>Team meetings, a first look at lean</td></tr><tr><td>Standard workshop</td><td>60 min</td><td>Most groups</td></tr><tr><td>Deep dive</td><td>90 min</td><td>Supervisors and improvement teams, using your own line in Pro</td></tr></tbody></table><p>Any group size. Pairs or groups of three sharing one screen work best. One person can also play alone in 10–20 minutes.</p>'),
  ('How a session runs','<ol><li><b>Run the default line.</b> Nobody changes anything. Every order ships, and the profit is negative.</li><li><b>Debrief.</b> The facilitator asks: <em>"Every unit the customer ordered was shipped. So where did the money go?"</em></li><li><b>Find the takt.</b> Groups set people per process and run the day again.</li><li><b>Standard WIP.</b> Groups compare how many parts to keep between processes.</li><li><b>Back to the workplace.</b> Each person writes one thing to look for tomorrow.</li></ol><p>The game never gives the answer first. People have to try, get it wrong, and talk about why — that is where the learning happens.</p>'),
  ('Free version and Pro','<table><thead><tr><th></th><th>Free</th><th>Pro ($29 / Team $99)</th></tr></thead><tbody><tr><td>Play the default factory</td><td>Yes</td><td>Yes</td></tr><tr><td>Change the order, cycle times, prices and wages to match your workplace</td><td>—</td><td>Yes</td></tr><tr><td>6-page facilitator guide (session plan, questions, common answers)</td><td>—</td><td>Yes</td></tr><tr><td>Works offline after download</td><td>—</td><td>Yes</td></tr><tr><td>Bug fixes</td><td>—</td><td>Free for one year</td></tr></tbody></table><p>The Team license covers one organization and one facilitator, with unlimited participants and sessions.</p>')],
 [('Do I need to be a lean expert to run it?','No. The Pro facilitator guide gives you the session plan, the questions to ask at each step and the answers people usually give.'),
  ('Does it need installation or sign-up?','No. The free version runs in a browser on itch.io. The Pro version is a single file that runs in Chrome, Edge, Safari or Firefox, even without an internet connection.'),
  ('Is it only for factories?','The setting is a factory line, but the question it raises — is our work matched to what the customer really needs? — is just as useful in offices, hospitals and service work. The facilitator guide ends with questions about your own workplace.'),
  ('Can I use it in a university class?','Yes. It works well for operations management and lean courses. Contact me if you want to adapt it for a class.')],
 [('Play free','https://ttmtkg.itch.io/overproduction-factory','primary'),('Buy Pro','https://mendomilab.gumroad.com/l/overproduction-factory-pro','ghost')],
 'games/overproduction-factory/','ja/games/factory/','Overproduction Factory')

# ---------- EN: Supplier's Puzzle ----------
page('en','games/suppliers-puzzle/',
 "The Supplier's Puzzle | Heijunka Simulation Game | Mendomi Lab",
 "A free browser game about heijunka. Toyota needs 8,000 cars this month. Change the build order and see why leveled orders let suppliers cut costs together.",
 "The Supplier's Puzzle: a heijunka simulation game",
 "Toyota needs 8,000 cars this month and you run two suppliers. Change the build order, the people and the machines, and find the cheapest way for the supplier — not just for Toyota. An animated one-month simulation shows where the cost really comes from.",
 [('What participants learn','<ul><li>Why a customer\'s build order decides how much capacity and stock its suppliers must carry.</li><li><b>Heijunka</b>: leveling both the volume and the mix of models over time.</li><li>Why large batches force suppliers to choose between capacity for the peak and stock built ahead — and why both cost money.</li><li>How suppliers should size people and machines when the order changes.</li><li>Why lowering supplier cost is a shared job, not just a price demand.</li></ul>'),
  ('Who it is for and how long it takes','<table><thead><tr><th>Format</th><th>Time</th><th>Best for</th></tr></thead><tbody><tr><td>Quick demo</td><td>30 min</td><td>Team meetings, a first look at heijunka</td></tr><tr><td>Standard workshop</td><td>60 min</td><td>Most groups</td></tr><tr><td>Deep dive</td><td>90 min</td><td>Purchasing, planning and supplier development teams, using your own products in Pro</td></tr></tbody></table><p>Groups of three work well: one plays Toyota (the build order), one plays Supplier A and one plays Supplier B.</p>'),
  ('How a session runs','<ol><li><b>Run the month as it starts.</b> Toyota\'s line never stops. Nothing seems wrong.</li><li><b>Debrief.</b> The facilitator asks: <em>"Who chose this cost — the supplier or Toyota?"</em></li><li><b>Suppliers cut cost alone.</b> They remove people and machines and watch the warehouse fill up.</li><li><b>Toyota changes the build order.</b> Suppliers resize their people and machines each time and compare the cost.</li><li><b>Back to your supply chain.</b> Where do uneven orders reach your own suppliers or your own floor?</li></ol>'),
  ('Free version and Pro','<table><thead><tr><th></th><th>Free</th><th>Pro ($49 / Team $149)</th></tr></thead><tbody><tr><td>Play the default month</td><td>Yes</td><td>Yes</td></tr><tr><td>Change models, volumes, machines and costs to match your supply chain</td><td>—</td><td>Yes</td></tr><tr><td>6-page facilitator guide</td><td>—</td><td>Yes</td></tr><tr><td>Works offline after download</td><td>—</td><td>Yes</td></tr><tr><td>Bug fixes</td><td>—</td><td>Free for one year</td></tr></tbody></table>')],
 [('What is heijunka?','Heijunka means leveling production: both the volume and the mix of products are spread evenly over time, instead of building one model in a long run and then switching. It is one of the foundations of the Toyota Production System.'),
  ('Why does the customer\'s order matter to the supplier?','A supplier has to be ready for the busiest day its customer creates. With large batches, that peak forces the supplier to carry either idle capacity or stock built ahead. The game lets players see that cost move.'),
  ('Do I need to be a lean expert to run it?','No. The Pro facilitator guide gives you the session plan, the questions to ask and the answers people usually give.'),
  ('Does it need installation or sign-up?','No. The free version runs in a browser on itch.io. The Pro version is a single file that runs offline in any modern browser.')],
 [('Play free','https://ttmtkg.itch.io/the-suppliers-puzzle','primary'),('Buy Pro','https://mendomilab.gumroad.com/l/supplier-puzzle-pro','ghost')],
 'games/suppliers-puzzle/','ja/games/supplier/',"The Supplier's Puzzle")

# ---------- JA: 造りすぎ工場 ----------
page('ja','ja/games/factory/',
 '造りすぎ工場｜造りすぎのムダを学ぶリーン研修ゲーム｜Mendomi Lab',
 'ブラウザで無料で遊べる トヨタ生産方式の体験ゲーム。全工程を忙しくするとお金を失う。タクトタイム 必要人数 標準手持ちを 30〜90分の研修で体験しながら学べます。',
 '造りすぎ工場：造りすぎのムダを体験するリーン研修ゲーム',
 '4つの工程と 1日480台の注文。現場のこれまでのルールは「工程は止めるな 造れるだけ造れ」。そのとおりにすると 注文は全部出荷できるのに 1日の利益はマイナスになります。本当に利益が出る人数と仕掛品の数を 自分で見つけるゲームです。',
 [('このゲームで学べること','<ul><li>全工程が忙しく見えても お客様が求める以上に造ると 利益が減る理由</li><li><b>タクトタイム</b>：お客様の注文で決まる速さ（稼働時間 ÷ 注文数）</li><li><b>必要人数</b>の出し方（工数 ÷ タクトタイム）</li><li><b>標準手持ち</b>：ラインを止めずに流すための最低限の仕掛品と 決めないと在庫がふえていくしくみ</li><li>トヨタ生産方式にならって このゲームが 売れると決まっていない在庫を価値ゼロとして数える理由</li></ul>'),
  ('だれ向けか・何分かかるか','<table><thead><tr><th>やり方</th><th>時間</th><th>向いている場</th></tr></thead><tbody><tr><td>短い紹介</td><td>30分</td><td>チームの会議 リーンの入り口</td></tr><tr><td>ふつうの研修</td><td>60分</td><td>たいていのグループ</td></tr><tr><td>じっくり</td><td>90分</td><td>監督者や改善チーム（Pro版で自分のラインに合わせる）</td></tr></tbody></table><p>人数は何人でもできます。2〜3人で1つの画面を見ながら進めるのがおすすめです。1人で遊ぶなら10〜20分です。</p>'),
  ('研修での進め方','<ol><li><b>そのまま動かす</b>：何も変えずに1日を動かします。注文は全部出荷できて 利益はマイナスです</li><li><b>ふり返り</b>：進行役が聞きます。「注文は全部出せた。ではお金はどこに消えた？」</li><li><b>タクトを見つける</b>：工程ごとの人数を決めて もう一度動かします</li><li><b>標準手持ち</b>：工程のあいだに置く数を変えてくらべます</li><li><b>職場に持ち帰る</b>：明日から自分の職場で見るところを 1人1つ書きます</li></ol><p>答えを先に見せないのがこのゲームのしくみです。まず試して まちがえて なぜかを話し合う。そこに学びがあります。</p>'),
  ('無料版とPro版','<table><thead><tr><th></th><th>無料版</th><th>Pro版</th></tr></thead><tbody><tr><td>決まった工場で遊ぶ</td><td>○</td><td>○</td></tr><tr><td>注文 工数 価格 賃金を自分の職場に合わせて変える</td><td>－</td><td>○</td></tr><tr><td>6ページの進行役の手引き</td><td>－</td><td>○</td></tr><tr><td>ダウンロードしてネットなしで使える</td><td>－</td><td>○</td></tr><tr><td>不具合の修正</td><td>－</td><td>購入から1年間無料</td></tr></tbody></table><p id="pro">日本語のPro版を購入できます。<a href="https://buy.stripe.com/5kQ00b8sa979gBU8SbcV202">1人用 4,500円</a>／<a href="https://buy.stripe.com/9B6aEPbEm835fxQ9WfcV203">チーム用 15,000円</a>（クレジットカード・お支払いのあとすぐダウンロード）。くわしくは<a href="../../tokushoho/#pro">特定商取引法にもとづく表記</a>をご覧ください。</p>')],
 [('リーンにくわしくなくても進行できますか？','できます。Pro版の手引きに 進め方 各場面で聞くこと よく出る答えと そのあとの導き方が書いてあります。'),
  ('インストールや登録はいりますか？','いりません。無料版はブラウザでそのまま遊べます。'),
  ('工場以外の職場でも使えますか？','使えます。題材は工場ですが「自分たちの仕事は お客様が本当に求める量に合っているか」という問いは 事務 病院 サービスの仕事でも話し合えます。製造業でないチームには 回らないパスタ屋 も入りやすいゲームです。'),
  ('大学の授業でも使えますか？','使えます。生産管理やリーンの授業に合います。授業に合わせたいときは 相談してください（最初の1往復は無料）。')],
 [('無料で遊ぶ','../../play/factory/','primary'),('作った人に相談する','../../consult/','ghost')],
 'games/overproduction-factory/','ja/games/factory/','造りすぎ工場')

# ---------- JA: サプライヤーのパズル ----------
page('ja','ja/games/supplier/',
 'サプライヤーのパズル｜平準化を体験する研修ゲーム｜Mendomi Lab',
 'ブラウザで無料で遊べる 平準化の体験ゲーム。トヨタは今月8,000台が必要。組み立ての順番を変えると なぜサプライヤーがいっしょにコストを下げられるのかがわかります。',
 'サプライヤーのパズル：平準化を体験するシミュレーションゲーム',
 'トヨタは今月8,000台が必要です。あなたは2つのサプライヤーを動かします。組み立ての順番と 自社の人と設備を変えて トヨタにとってだけでなく サプライヤーにとっていちばん安い方法を見つけてください。1か月を動かすアニメーションで コストがどこから来るのかが見えます。',
 [('このゲームで学べること','<ul><li>お客様の組み立ての順番が サプライヤーの持つべき人 設備 在庫を決めること</li><li><b>平準化</b>：量と車種の組み合わせを 日ごとにならすこと</li><li>まとめて造る注文だと サプライヤーは「いちばん忙しい日に合わせた人と設備」か「先に造ってためる在庫」のどちらかを持つしかなく どちらもお金がかかること</li><li>注文が変わったとき サプライヤーの人と設備をどう決めるか</li><li>サプライヤーのコストを下げるのは 値下げのお願いではなく いっしょにやる仕事だということ</li></ul>'),
  ('だれ向けか・何分かかるか','<table><thead><tr><th>やり方</th><th>時間</th><th>向いている場</th></tr></thead><tbody><tr><td>短い紹介</td><td>30分</td><td>会議 平準化の入り口</td></tr><tr><td>ふつうの研修</td><td>60分</td><td>たいていのグループ</td></tr><tr><td>じっくり</td><td>90分</td><td>購買 生産計画 調達の担当（Pro版で自社の製品に合わせる）</td></tr></tbody></table><p>3人1組なら トヨタ役（組み立ての順番）とサプライヤーA役 B役に分かれると話が深まります。</p>'),
  ('研修での進め方','<ol><li><b>そのまま動かす</b>：トヨタのラインは止まりません。何も問題がないように見えます</li><li><b>ふり返り</b>：進行役が聞きます。「このコストを決めたのは サプライヤー？ それともトヨタ？」</li><li><b>サプライヤーだけで下げる</b>：人と設備を減らすと 倉庫に在庫がたまっていきます</li><li><b>トヨタが順番を変える</b>：順番を変えるたびに サプライヤーの人と設備を合わせ直して コストをくらべます</li><li><b>自分の職場に持ち帰る</b>：ばらつきのある注文が 自社や仕入れ先のどこに届いているかを話します</li></ol>'),
  ('無料版とPro版','<table><thead><tr><th></th><th>無料版</th><th>Pro版</th></tr></thead><tbody><tr><td>決まった1か月で遊ぶ</td><td>○</td><td>○</td></tr><tr><td>車種 台数 設備 コストを自社に合わせて変える</td><td>－</td><td>○</td></tr><tr><td>6ページの進行役の手引き</td><td>－</td><td>○</td></tr><tr><td>ダウンロードしてネットなしで使える</td><td>－</td><td>○</td></tr><tr><td>不具合の修正</td><td>－</td><td>購入から1年間無料</td></tr></tbody></table><p id="pro">日本語のPro版を購入できます。<a href="https://buy.stripe.com/eVq7sD6k23MPclEd8rcV204">1人用 7,500円</a>／<a href="https://buy.stripe.com/6oU4greQy5UXetM1pJcV205">チーム用 23,000円</a>（クレジットカード・お支払いのあとすぐダウンロード）。くわしくは<a href="../../tokushoho/#pro">特定商取引法にもとづく表記</a>をご覧ください。</p>')],
 [('平準化（ヘイジュンカ）とは何ですか？','造る量と車種の組み合わせを 日ごとにならすことです。何日も同じ車種を造ってから切りかえるやり方とは反対の考え方です。トヨタ生産方式の土台の1つです。'),
  ('お客様の注文の順番が なぜサプライヤーに関係するのですか？','サプライヤーは お客様がつくるいちばん忙しい日に間に合うように準備しなければなりません。まとめて造る注文だと その山のために 使わない日の多い人と設備か 先に造った在庫を持つことになります。ゲームでは そのコストの動きが見えます。'),
  ('リーンにくわしくなくても進行できますか？','できます。Pro版の手引きに 進め方 聞くこと よく出る答えが書いてあります。'),
  ('インストールや登録はいりますか？','いりません。無料版はブラウザでそのまま遊べます。')],
 [('無料で遊ぶ','../../play/supplier/','primary'),('作った人に相談する','../../consult/','ghost')],
 'games/suppliers-puzzle/','ja/games/supplier/','サプライヤーのパズル')

# ---------- JA: 回らないパスタ屋 ----------
page('ja','ja/games/pasta/',
 '回らないパスタ屋｜人数とネックを考える無料の研修ゲーム｜Mendomi Lab',
 '小さなパスタ屋のランチのピーク。ピークに合わせた人数がいちばん儲かるのか。厨房 ホール レジの人数を変えて ネック（いちばん先にいっぱいになる場所）を見つける無料ゲームです。',
 '回らないパスタ屋：飲食店の人数とネックを考えるゲーム',
 '席は14席 ランチは11時から14時まで。これまでは「忙しいなら人を増やせ」で7人で回してきました。厨房 ホール レジの人数を変えて ランチの利益がいちばん大きくなる人数を見つけるゲームです。製造業でないチームにも入りやすい題材です。',
 [('このゲームで学べること','<ul><li><b>ネック</b>：いちばん先にいっぱいになる場所。ネックより速い場所に人を足しても売上は増えないこと</li><li><b>見えにくいネック</b>：行列の原因が 見かけとは別の場所にあることもあること</li><li>考える順番：まずネックを見つけ ほかの持ち場の人数をネックの速さに合わせること</li><li>ピークに合わせて人を置くことが いつもいちばん儲かるとはかぎらないこと</li></ul>'),
  ('だれ向けか・何分かかるか','<p>飲食 小売 サービスの店長やリーダー 研修の入り口として。1人で遊ぶなら10〜20分。研修なら30〜60分で 造りすぎ工場の前後に入れると 製造業とサービス業の両方の目で考えられます。</p>'),
  ('研修での進め方','<ol><li><b>7人のまま動かす</b>：ランチを動かして 持ち場の忙しさと 帰ってしまったお客さんを見ます</li><li><b>ふり返り</b>：進行役が聞きます。「いちばん先にいっぱいになったのはどこ？」</li><li><b>ネックに合わせる</b>：人数を変えてもう一度動かし 利益と逃したお客さんをくらべます</li><li><b>自分の店に持ち帰る</b>：自分の職場のネックはどこかを話します</li></ol>'),
  ('料金','<p>無料です。登録もいりません。</p><p>このゲームは 工場以外の職場でも同じ考え方で作れることを見せる見本です。お店 病院 窓口など 自分の職場に合わせた版がほしいときは <a href="../../consult/">相談してください</a>（最初の1往復は無料）。</p>')],
 [('飲食店でなくても使えますか？','使えます。受付 窓口 コールセンターなど 人がお客さんを順番にさばく職場なら同じ考え方が使えます。'),
  ('インストールや登録はいりますか？','いりません。ブラウザでそのまま遊べます。'),
  ('自分の店に合わせて作り直せますか？','相談してください。席の数 料理の時間 お客さんの来かたを変えた版を作ることができます（最初の1往復は無料）。')],
 [('無料で遊ぶ','../../play/pasta/','primary'),('作った人に相談する','../../consult/','ghost')],
 None,'ja/games/pasta/','回らないパスタ屋')

# ---------- JA: 止まる工場・止める工場 ----------
page('ja','ja/games/kadou/',
 '止まる工場・止める工場｜可動率と稼働率のちがいがわかる無料の研修ゲーム｜Mendomi Lab',
 '設備が止まっている時間には 故障で止まってしまう時間と 注文の分をつくり終えて止めている時間の2種類がある。トヨタ生産方式の可動率（べきどうりつ）と稼働率（かせどうりつ）のちがいを 設備の台数を変えて体験する無料ゲームです。',
 '止まる工場・止める工場：トヨタ生産方式の可動率と稼働率を体験するゲーム',
 '設備が動いていない時間を ひとつの数字だけで見ると 故障で止まった時間も 注文がなくて止めた時間も 同じ「停止」になってしまいます。トヨタ生産方式では 動かすべきときに動けたかを見る可動率と 注文に対してどれだけ動かしたかを見る稼働率を分けて考えます。このゲームでは 設備の台数を変えて1日を動かし 2つのちがいを数字とお金で確かめます。',
 [('このゲームで学べること','<ul><li><b>可動率（べきどうりつ）</b>：動かしたいときに動けた割合。故障で止まる時間（赤）は直すもので 100%をめざすこと</li><li><b>稼働率（かせどうりつ）</b>：設備の能力に対してどれだけ動かしたか。注文で決まるので 低くてもいいこと</li><li>赤があると 取り返すために設備を多く持つことになること</li><li>注文の分をつくり終えて止めている時間（黄）を埋めようとして動かすと 造りすぎになること</li><li>黄が多いときは 設備を持ちすぎていないかを考えること</li></ul>'),
  ('だれ向けか・何分かかるか','<p>製造業の新人研修 設備や生産管理の担当者 大学の生産管理の授業に。1人で遊ぶなら15〜20分。研修なら30〜45分で 造りすぎ工場の前後に入れると 造りすぎのムダとのつながりが見えます。</p>'),
  ('研修での進め方','<ol><li><b>ステージ1（赤）</b>：故障のある工場で 注文に間に合う台数を探します。計算では3台で足りるはずなのに 足りないのはなぜか</li><li><b>ふり返り</b>：進行役が聞きます。「赤の時間はなくせる？ なくなったら何台ですむ？」</li><li><b>ステージ2（黄）</b>：故障のない工場で 注文が少ない日に「稼働率を上げろ」と言われたらどうするかをためします</li><li><b>自分の職場に持ち帰る</b>：自分の職場の数字は 赤と黄を分けて見ているかを話します</li></ol>'),
  ('稼働率の定義は会社によってちがう','<p id="bunbo">同じ「稼働率」という言葉でも 分母のとり方が会社や分野でちがいます。このゲームは<b>TPSの定義</b>で計算しています。</p><table><thead><tr><th>考え方</th><th>分母</th><th>故障の扱い</th></tr></thead><tbody><tr><td><b>TPSの稼働率</b></td><td>定時（決められた時間）の能力</td><td>分母から引かない。可動率のほうで見る</td></tr><tr><td>故障の時間を分母から引く稼働率</td><td>動かせた時間（定時 − 故障など）</td><td>分母から消える</td></tr><tr><td>設備保全・信頼性の「稼働率」</td><td>動かしたい時間</td><td>故障で下がる（中身はTPSの可動率とほぼ同じ）</td></tr><tr><td>OEE（設備総合効率）の時間稼働率</td><td>負荷時間</td><td>故障や段取りで下がる（これも可動率に近い）</td></tr></tbody></table><h3>TPSで故障の時間を分母から引かない理由</h3><p>分母から故障の時間を引くと <b>故障しても数字が悪くならない</b>からです。定時8時間 1時間に50個つくれる設備で 注文は300個。故障が3時間あって250個しかつくれなかった日で比べます。</p><table><thead><tr><th>分母</th><th>計算</th><th>結果</th></tr></thead><tbody><tr><td>定時（TPS）</td><td>250 ÷ 400</td><td>62.5%</td></tr><tr><td>故障を引いた時間</td><td>250 ÷（5時間 × 50）</td><td><b>100%</b></td></tr></tbody></table><p>故障を引いた分母だと 50個足りないのに100%になります。問題が数字から見えなくなるので TPSでは 稼働率は定時を分母にして必要数に合っているかを見て 可動率で故障や段取りで止まった分をはっきり出します。2つに分けて 故障がかくれないようにしているのです。</p><p>相談の場で「稼働率」という言葉が出たら 最初に<b>「分母は何ですか？」</b>と確かめると 話のくいちがいを防げます。</p>'),
  ('無料版とPro版','<table><thead><tr><th></th><th>無料版</th><th>Pro版</th></tr></thead><tbody><tr><td>決まった工場で遊ぶ</td><td>○</td><td>○</td></tr><tr><td>稼働時間 能力 故障の時刻と長さ 注文 価格を自分の工場に合わせて変える</td><td>－</td><td>○</td></tr><tr><td>6ページの進行役の手引き（進め方 聞くこと 答えの一覧）</td><td>－</td><td>○</td></tr><tr><td>ダウンロードしてネットなしで使える</td><td>－</td><td>○</td></tr><tr><td>不具合の修正</td><td>－</td><td>購入から1年間無料</td></tr></tbody></table><p id="pro">日本語のPro版を購入できます。<a href="https://buy.stripe.com/7sY8wH23M83571k7O7cV206">1人用 4,500円</a>／<a href="https://buy.stripe.com/28E9ALfUC2ILclE6K3cV207">チーム用 15,000円</a>（クレジットカード・お支払いのあとすぐダウンロード）。くわしくは<a href="../../tokushoho/#pro">特定商取引法にもとづく表記</a>をご覧ください。</p>')],
 [('可動率と稼働率のちがいは何ですか？','可動率は 動かしたいときにちゃんと動けた割合で 故障などで止まってしまった時間だけを見ます。稼働率は 設備の能力に対してどれだけ動かしたかで 注文がなくて止めている時間も含めて見ます。可動率は100%をめざし 稼働率は注文しだいです。'),
  ('読み方を変えるのはなぜですか？','どちらも「かどうりつ」と読めてしまうので トヨタ生産方式では可動率を「べきどうりつ」 稼働率を「かせどうりつ」と読んで 耳で聞いても区別できるようにしています。'),
  ('稼働率の分母は会社によってちがうのですか？','ちがいます。TPSでは定時の能力を分母にしますが 故障の時間を分母から引く会社もあります。設備保全やOEE（設備総合効率）でいう稼働率は 中身がTPSの可動率に近いこともあります。話をするときは最初に分母を確かめるのが安全です。'),
  ('なぜTPSでは故障の時間を分母から引かないのですか？','引くと 故障しても稼働率が下がらないからです。たとえば注文300個に対して故障で250個しかつくれなくても 故障を引いた分母だと100%になってしまいます。TPSでは稼働率と可動率を分けて 故障が数字からかくれないようにしています。'),
  ('インストールや登録はいりますか？','いりません。ブラウザでそのまま遊べます。'),
  ('自分の工場の数字に合わせられますか？','相談してください。設備の能力 故障の時間 注文の数を変えた版を作ることができます（最初の1往復は無料）。')],
 [('無料で遊ぶ','../../play/kadou/','primary'),('作った人に相談する','../../consult/','ghost')],
 'games/availability-vs-utilization/','ja/games/kadou/','止まる工場・止める工場')

# ---------- EN: Stalled Factory, Paused Factory ----------
page('en','games/availability-vs-utilization/',
 "Stalled Factory, Paused Factory | Availability vs. Utilization Game | Mendomi Lab",
 "A free browser game on the two kinds of machine downtime. See why the Toyota Production System separates availability (bekido-ritsu) from utilization (kasedo-ritsu).",
 "Stalled Factory, Paused Factory: a game on availability vs. utilization",
 "If you track machine time with one number, a breakdown and a planned stop both look like \"not running.\" The Toyota Production System keeps them apart: availability asks whether the machine could run when it was needed, and utilization asks how much it ran against the order. In this game you choose how many machines to own, run the day, and see the difference in numbers and in money.",
 [('What participants learn','<ul><li><b>Availability</b> (bekidō-ritsu, 可動率): the share of the needed time a machine could actually run. Breakdown time (red) is something to fix. The target is 100%.</li><li><b>Utilization</b> (kasedō-ritsu, 稼働率): how much a machine ran against its capacity. The order decides it, so a low number can be fine.</li><li>Why red makes you own extra machines to win back the lost time.</li><li>Why running machines to fill idle time (yellow) is overproduction.</li><li>When there is a lot of yellow, the real question is whether you own too many machines.</li></ul>'),
  ('Who it is for and how long it takes','<p>New hires in manufacturing, maintenance and production planning teams, and operations management classes. 15–20 minutes alone. In a workshop, 30–45 minutes; it pairs well with <a href="../overproduction-factory/">Overproduction Factory</a>.</p>'),
  ('How a session runs','<ol><li><b>Stage 1 (red)</b>: in a plant with breakdowns, find how many machines meet the order. On paper 3 should be enough — why are they not?</li><li><b>Debrief</b>: the facilitator asks: <em>"Can the red time be removed? If it were, how many machines would you need?"</em></li><li><b>Stage 2 (yellow)</b>: in a plant with no breakdowns, head office says "raise utilization" on a slow day. What do you do?</li><li><b>Back to your floor</b>: do your own numbers keep red and yellow apart?</li></ol>'),
  ('The same word, different denominators','<p id="denominator">"Utilization" and "availability" are defined differently from company to company and field to field. In English the confusion is worse, because OEE uses "availability" for something close to what Toyota calls bekidō-ritsu. This game uses the <b>TPS definitions</b>.</p><table><thead><tr><th>Definition</th><th>Denominator</th><th>Breakdown time</th></tr></thead><tbody><tr><td><b>TPS utilization</b> (kasedō-ritsu)</td><td>Capacity in the planned shift</td><td>Not removed. It shows up in availability instead</td></tr><tr><td>Utilization with downtime removed</td><td>Time the machine could run (shift − breakdowns etc.)</td><td>Disappears from the number</td></tr><tr><td>Maintenance / reliability "availability" or "uptime"</td><td>Time the machine was needed</td><td>Lowers it (close to TPS bekidō-ritsu)</td></tr><tr><td>OEE availability</td><td>Planned production time</td><td>Breakdowns and changeovers lower it (also close to bekidō-ritsu)</td></tr></tbody></table><h3>Why TPS does not remove breakdown time from utilization</h3><p>If breakdown time is taken out of the denominator, <b>a breakdown no longer makes the number worse</b>. Take an 8-hour shift, a machine that makes 50 parts an hour, and an order of 300. Breakdowns take 3 hours and only 250 parts are made.</p><table><thead><tr><th>Denominator</th><th>Calculation</th><th>Result</th></tr></thead><tbody><tr><td>Planned shift (TPS)</td><td>250 ÷ 400</td><td>62.5%</td></tr><tr><td>Shift minus breakdowns</td><td>250 ÷ (5 h × 50)</td><td><b>100%</b></td></tr></tbody></table><p>With breakdowns removed, the day reads 100% even though the order is 50 parts short. The problem disappears from the numbers. So TPS keeps two numbers: utilization uses the planned shift and asks whether output matches demand, and availability shows the time lost to breakdowns and changeovers. Neither can hide the other.</p><p>When someone quotes a utilization figure, ask first: <b>"What is the denominator?"</b> It saves a lot of talking past each other.</p>'),
  ('Free version and Pro','<table><thead><tr><th></th><th>Free</th><th>Pro ($29 / Team $99)</th></tr></thead><tbody><tr><td>Play the default factory</td><td>Yes</td><td>Yes</td></tr><tr><td>Change working time, capacity, breakdown times, orders and prices to match your plant</td><td>—</td><td>Yes</td></tr><tr><td>6-page facilitator guide (session plan, questions, answer key)</td><td>—</td><td>Yes</td></tr><tr><td>Works offline after download</td><td>—</td><td>Yes</td></tr><tr><td>Bug fixes</td><td>—</td><td>Free for one year</td></tr></tbody></table><p id="pro">Buy the Pro edition: <a href="https://buy.stripe.com/4gMeV523M0AD5Xgb0jcV208">Personal $29</a> / <a href="https://buy.stripe.com/9B68wHcIq4QTclEd8rcV209">Team $99</a> (card, Apple Pay or Google Pay; download right after payment). Personal: for your own classes and training. Team: share within your organization.</p>')],
 [('What is the difference between availability and utilization?','Availability looks only at time lost to breakdowns and similar problems: of the time the machine was needed, how much could it run? Utilization compares running time with full capacity, so it also counts time stopped because there was no order. Availability aims for 100%; utilization depends on demand.'),
  ('Why does Toyota read the two words differently?','In Japanese both 可動率 and 稼働率 can be read "kadō-ritsu." Toyota reads the first as "bekidō-ritsu" and the second as "kasedō-ritsu" so people can tell them apart by ear.'),
  ('Is this the same as OEE?','No. OEE multiplies availability, performance and quality into one number. This game is about a different point: keeping breakdown stops and planned stops apart, because one should be fixed and the other is fine.'),
  ('Why doesn\'t TPS take breakdown time out of the utilization denominator?','Because then breakdowns would stop lowering the number. A day that is 50 parts short of a 300-part order can still read 100% if the lost hours are removed from the denominator. TPS keeps utilization and availability apart so breakdowns cannot hide.'),
  ('Does it need installation or sign-up?','No. The free version runs in any modern browser. The Pro edition is a single file that runs offline in Chrome, Edge, Safari or Firefox.'),
  ('Can it be adapted to my plant?','Yes. Machine capacity, breakdown time and order sizes can be changed. Get in touch — the first reply is free.')],
 [('Play free','../../play/availability-vs-utilization/','primary'),('Talk to the maker','../../consult/','ghost')],
 'games/availability-vs-utilization/','ja/games/kadou/','Stalled Factory, Paused Factory')
print('built')
