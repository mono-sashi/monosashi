#!/usr/bin/env python3
"""
モノサシ SEO構造 生成スクリプト

data/shops.json を正のデータとして、以下を機械生成する:
  - /nishiazabu/sushi/index.html            エリア×ジャンルのメインページ(絞り込み+比較+条件ページ導線)
  - /nishiazabu/sushi/{slug}/index.html      店舗詳細ページ(11店舗)
  - /nishiazabu/sushi/{condition}/index.html 条件別比較ページ(9種)
  - /sitemap.xml
  - /robots.txt
  - 旧URL(/shops/*.html, /areas/nishiazabu.html)を新URLへの案内ページに置換

再実行すれば同じ入力から同じ出力が再生成される(冪等)。店舗データを更新する場合は
data/shops.json を編集してこのスクリプトを再実行すること。手でnishiazabu/配下のHTMLを
直接編集しないこと(次回実行時に上書きされる)。
"""
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE_URL = "https://sushi-monosashi.com"
BRAND = "モノサシ"

with open(os.path.join(ROOT, "data", "shops.json"), encoding="utf-8") as f:
    DATA = json.load(f)

SHOPS = DATA["shops"]
AREA = DATA["area"]  # nishiazabu / sushi

# ---------------------------------------------------------------------------
# 条件別ページの定義
# filter: shop(dict) -> bool
# ---------------------------------------------------------------------------
CONDITIONS = [
    {
        "slug": "osusume",
        "label": "おすすめ",
        "navLabel": "おすすめの鮨を見る",
        "title": "西麻布の鮨おすすめ11選｜価格・個室・開始時間から比較｜モノサシ",
        "h1": "西麻布の鮨、おすすめ11店",
        "description": "西麻布エリアで「ここなら安心して連れていける」と判断できる基準で選んだ、掲載11店舗すべてを比較できるページです。価格・個室・特徴で絞り込めます。",
        "lead": "モノサシが掲載している西麻布エリアの鮨店は、オンライン予約が可能で、価格・個室・特徴を同じ基準で比較できる店だけに厳選しています。まずはこの11店舗から、目的に合う店を絞り込んでください。",
        "body": [
            "西麻布は高価格帯の鮨店が集中するエリアで、店ごとに個室の有無・コース開始時間・サービス料の扱いが異なります。同じ「おまかせコース」でも、サービス料が加算される店とされない店では2名利用時の実質負担額が数千円単位で変わるため、コース料金だけで比較すると想定より高くなることがあります。",
            "初めて絞り込む場合は、まず「予算(2名・料理利用額)」で候補を絞り、そのうえで個室の有無・コース開始時間・特徴タグを見て目的に合う店を選ぶ順番がおすすめです。",
        ],
        "filter": lambda s: True,
    },
    {
        "slug": "date",
        "label": "デート向き",
        "navLabel": "デート向きの鮨を見る",
        "title": "西麻布でデートに使える鮨を比較｜モノサシ",
        "h1": "西麻布でデートに使える鮨",
        "description": "西麻布エリアの鮨店から、カウンターや個室でデート利用がしやすいと確認できた店舗を比較。価格・個室の有無・特徴もあわせて確認できます。",
        "lead": "「利用シーン」欄でデート利用について◎・○の情報が確認できた店舗のみを掲載しています。情報が確認できなかった店舗は含まれていません。",
        "body": [
            "デート利用では、カウンター席か個室かで過ごし方が変わります。大将との会話も含めて楽しみたい場合はカウンター、周りを気にせず会話に集中したい場合は個室・半個室が向いています。個室の有無は各店舗ページの「基本情報」で確認できます。",
            "コースの開始時間も重要な要素です。仕事帰りに立ち寄るなら18時台スタートの店、ゆっくり夜を過ごすなら20時30分前後の遅い回がある店が候補になります。西麻布の鮨店は当日・直前の予約が取りづらい店が多いため、日程が決まり次第の早めの予約をおすすめします。",
        ],
        "filter": lambda s: s.get("dateOk"),
    },
    {
        "slug": "entertain",
        "label": "接待・会食向き",
        "navLabel": "接待向きの鮨を見る",
        "title": "西麻布で接待に使える鮨を比較｜モノサシ",
        "h1": "西麻布で接待に使える鮨",
        "description": "西麻布エリアの鮨店から、個室や落ち着いた環境で接待・会食利用がしやすいと確認できた店舗を比較。価格・個室の有無・特徴もあわせて確認できます。",
        "lead": "「利用シーン」欄で接待・会食利用について◎・○の情報が確認できた店舗のみを掲載しています。情報が確認できなかった店舗は含まれていません。",
        "body": [
            "接待・会食では、取引先や上司との会話を周りに気にせず進められるかどうかが重要になります。個室・半個室を備えた店舗であれば、込み入った話や商談も安心して進められます。西麻布の鮨店は個室ありでも収容人数(2名〜／4名〜など)が店舗ごとに異なるため、参加人数が確定したら予約時に伝えておくと確実です。",
            "接待は店選びの失敗が許されない利用シーンのため、コース料金だけでなくサービス料の有無や「2名・料理利用額」まで含めた予算感を事前に把握しておくことをおすすめします。コース開始時間が接待相手のスケジュールに合うかもあわせて確認してください。",
        ],
        "filter": lambda s: s.get("entertainOk"),
    },
    {
        "slug": "anniversary",
        "label": "記念日向き",
        "navLabel": "記念日向きの鮨を見る",
        "title": "西麻布で記念日に使える鮨を比較｜モノサシ",
        "h1": "西麻布で記念日に使える鮨",
        "description": "西麻布エリアの鮨店から、誕生日や結婚記念日など特別な日の利用がしやすいと確認できた店舗を比較。価格・個室の有無・特徴もあわせて確認できます。",
        "lead": "「利用シーン」欄で記念日利用について◎・○の情報が確認できた店舗のみを掲載しています。情報が確認できなかった店舗は含まれていません。",
        "body": [
            "記念日利用では、誕生日や結婚記念日など特別な日を落ち着いて過ごせるかどうかが重要になります。個室・半個室のある店舗であれば周りを気にせずゆっくり過ごせますが、カウンターのみの店でも「落ち着いた雰囲気」の特徴タグが付いている店舗は記念日利用の候補になります。",
            "サプライズや特別な演出への対応可否は店舗によって異なるため、記念日利用である旨を予約時に伝えておくとスムーズです。3万円台の店舗は個室を備える比率も高いため、あわせて価格帯別ページも参考にしてください。",
        ],
        "filter": lambda s: s.get("anniversaryOk"),
    },
    {
        "slug": "private-room",
        "label": "個室あり",
        "navLabel": "個室ありの鮨を見る",
        "title": "西麻布で個室ありの鮨を比較｜モノサシ",
        "h1": "西麻布で個室ありの鮨",
        "description": "西麻布エリアの鮨店から、個室・半個室を備えた店舗だけを比較。接待や会食、周りを気にせず過ごしたいデートにも使いやすい店舗です。",
        "lead": "個室・半個室のいずれかを備えていると公開情報で確認できた店舗を掲載しています。個室の広さ・人数の目安は店舗詳細ページでご確認ください。",
        "body": [
            "個室は、接待や会食で周りの会話を気にしたくない場合、記念日など特別な用途で個室・半個室が向いています。ただし個室のある鮨店でも、席数が少なく個室利用に人数条件(最少利用人数など)を設けている場合があるため、予約時に個室希望である旨と人数をあわせて伝えておくと確実です。",
            "個室の収容人数は店舗ごとに幅があります。2名から利用できる鮨 波残や江戸前鮓 すし通(2〜6名用の個室3室)など少人数向けの店がある一方、成 西麻布は最大15名までの貸切に対応しており、大人数の会食にも使えます。接待・記念日での個室利用を具体的に検討している場合は、それぞれの目的別ページもあわせてご確認ください。",
        ],
        "filter": lambda s: s.get("room") == "yes",
    },
    {
        "slug": "20000",
        "label": "2万円台",
        "navLabel": "2万円台の鮨を見る",
        "title": "西麻布で2万円台の鮨を比較｜モノサシ",
        "h1": "西麻布で2万円台の鮨",
        "description": "西麻布エリアの鮨店から、メインのディナーコースが2万円台(税込20,000〜29,999円)の店舗だけを比較できます。",
        "lead": "コース料金は税込表示です。同じ2万円台でもサービス料の有無で実際の支払額(2名・料理利用額)は変わるため、あわせてご確認ください。",
        "body": [
            "2万円台は、西麻布エリアの鮨店の中では比較的手が届きやすい価格帯で、初めての利用や普段使いに近い形での利用に向いています。ただしサービス料が10%前後加算される店では、コース料金が同じ2万円台でも2名の実質負担額に差が出るため、「2名・料理利用額」欄であわせて確認することをおすすめします。",
            "この価格帯に該当する店舗のうち、鮨利﨑 西麻布・鮨 波残は個室ありでデートや接待にも対応しやすい構成です。カウンターのみの寿司玄・鮓 有無・西麻布 鮨いちは、大将との距離が近いカウンター越しの体験を重視する方に向いています。",
        ],
        "filter": lambda s: 20000 <= s["priceMin"] <= 29999,
    },
    {
        "slug": "30000",
        "label": "3万円台",
        "navLabel": "3万円台の鮨を見る",
        "title": "西麻布で3万円台の鮨を比較｜モノサシ",
        "h1": "西麻布で3万円台の鮨",
        "description": "西麻布エリアの鮨店から、メインのディナーコースが3万円台(税込30,000〜39,999円)の店舗だけを比較できます。",
        "lead": "コース料金は税込表示です。特別な記念日や接待など、腰を据えて楽しみたいシーンに向いた価格帯の店舗です。",
        "body": [
            "3万円台は、大切な記念日や重要な接待など「失敗したくない」利用シーンで選ばれることが多い価格帯です。この価格帯になると個室を備えた店舗の比率も高くなる傾向があるため、目的に応じて個室の有無もあわせて確認することをおすすめします。",
            "実際にこの価格帯に該当する店舗はいずれも個室ありです。成 西麻布は最大15名までの貸切に対応し、江戸前鮓 すし通は2〜6名用の個室を3室備えるなど、少人数から大人数まで幅広い会食に対応できる構成が揃っています。",
        ],
        "filter": lambda s: 30000 <= s["priceMin"] <= 39999,
    },
    {
        "slug": "cospa",
        "label": "コスパがいい",
        "navLabel": "コスパがいい鮨を見る",
        "title": "西麻布でコスパがいい鮨を比較｜モノサシ",
        "h1": "西麻布でコスパがいい鮨",
        "description": "西麻布エリアの鮨店から、口コミの独立言及数をもとに「コスパがいい」という特徴タグが付与された店舗だけを比較できます。",
        "lead": "特徴タグは公式情報および口コミの定量基準(5人以上の独立言及)にもとづき機械的に付与しています。詳しい判定基準は各店舗ページをご覧ください。",
        "body": [
            "「コスパがいい」タグは、実際に閲覧できた口コミ(上限目安100件)のうち5人以上が価格に対する満足度を独立に言及している店舗にのみ付与しています。西麻布エリアは高価格帯の鮨店が中心のため、このタグは「安い」という意味ではなく、価格に見合った、あるいはそれ以上の満足度が口コミ上で確認できたことを示しています。",
            "該当店舗の2名・料理利用額は¥35,200〜¥44,000の範囲に収まっており、西麻布エリアの中では比較的予算を立てやすい価格帯にまとまっています。",
        ],
        "filter": lambda s: "コスパがいい" in s.get("features", []),
    },
    {
        "slug": "calm",
        "label": "落ち着いた雰囲気",
        "navLabel": "落ち着いた雰囲気の鮨を見る",
        "title": "西麻布で落ち着いた雰囲気の鮨を比較｜モノサシ",
        "h1": "西麻布で落ち着いた雰囲気の鮨",
        "description": "西麻布エリアの鮨店から、「落ち着いた雰囲気」という特徴タグが付与された店舗だけを比較できます。",
        "lead": "特徴タグは公式情報および口コミの定量基準(5人以上の独立言及)にもとづき機械的に付与しています。",
        "body": [
            "「落ち着いた雰囲気」タグは、店内の静けさや接客のトーンについて口コミで独立した言及が5人以上確認できた店舗に付与しています。会話を楽しみたい会食や、年配のゲストを連れていく接待など、賑やかさより落ち着きを優先したいシーンでの参考にしてください。",
            "該当するのは鮓 有無・西麻布 鮨いちの2店舗のみです。いずれも個室ではなくカウンター席が中心の店構えで、周りを気にせず過ごしたい場合は個室ありのページもあわせてご確認ください。",
        ],
        "filter": lambda s: "落ち着いた雰囲気" in s.get("features", []),
    },
    {
        "slug": "18",
        "label": "18時開始",
        "navLabel": "18時開始の鮨を見る",
        "title": "西麻布で18時から入れる鮨を比較｜モノサシ",
        "h1": "西麻布で18時から入れる鮨",
        "description": "西麻布エリアの鮨店から、コース開始時間が18時台の店舗だけを比較できます。仕事帰りに使いやすい時間帯です。",
        "lead": "「コース開始時間」は基本情報の営業時間から算出した目安です。実際の予約可能時間は店舗・予約先にご確認ください。",
        "body": [
            "18時台スタートは、仕事を早めに切り上げて向かう平日利用や、その後に別の予定を控えている日に使いやすい時間帯です。2部制を採る店では18時台が早い回にあたることが多く、遅い回(20時30分前後)より予約が取りやすい傾向があります。",
            "18時台に対応していないのは、17時開始の寿司玄・西麻布 鮨いちの2店舗のみです。この2店舗はさらに早い時間から利用できるため、18時よりも早めに会食を設定したい場合の候補になります。",
        ],
        "filter": lambda s: 18 in s.get("startHourTags", []),
    },
    {
        "slug": "2030",
        "label": "20時30分開始",
        "navLabel": "20時30分開始の鮨を見る",
        "title": "西麻布で20時30分から入れる鮨を比較｜モノサシ",
        "h1": "西麻布で20時30分から入れる鮨",
        "description": "西麻布エリアの鮨店から、20時30分スタートの回(2部制の遅い回など)がある店舗だけを比較できます。",
        "lead": "「コース開始時間」は基本情報の営業時間から算出した目安です。実際の予約可能時間は店舗・予約先にご確認ください。",
        "body": [
            "20時30分前後スタートは、仕事終わりに余裕を持って向かいたい場合や、2部制の遅い回でゆっくり過ごしたい場合に向いています。早い回に比べて予約が埋まりやすい店もあるため、候補が決まったら早めに空席状況を確認することをおすすめします。",
            "20時30分スタートに対応しているのは、鮨利﨑 西麻布・鮓 有無・鮨 きのしたの3店舗です。いずれも2部制を採用しており、早い回(18時台)より予約の融通が利きやすい場合があります。",
        ],
        "filter": lambda s: 2030 in s.get("startHourTags", []),
    },
]


def seo_url(path):
    """/foo/bar/index.html -> /foo/bar/ (GitHub Pagesは末尾スラッシュ形式で確実に配信されるため、
    canonical・OGP・sitemap・JSON-LDのURLはこちらに統一し、/index.html付きURLとの重複を避ける)"""
    if path.endswith("/index.html"):
        return path[: -len("index.html")]
    return path


def esc(s):
    if s is None:
        return ""
    return (
        str(s)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def head_common(title, description, canonical_path, depth):
    """depth: ルートまでの ../ の数"""
    up = "../" * depth
    og_url = f"{SITE_URL}{seo_url(canonical_path)}"
    return f"""<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{esc(title)}</title>
<meta name="description" content="{esc(description)}">
<link rel="canonical" href="{og_url}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Serif+JP:wght@400;500;600;700&family=Noto+Sans+JP:wght@300;400;500;700&display=swap" media="print" onload="this.media='all'">
<noscript><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Serif+JP:wght@400;500;600;700&family=Noto+Sans+JP:wght@300;400;500;700&display=swap"></noscript>
<link rel="stylesheet" href="{up}style.css">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{BRAND}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(description)}">
<meta property="og:url" content="{og_url}">
<meta property="og:image" content="{SITE_URL}/assets/ogp-default.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">"""


def header_nav(up):
    return f"""<header class="site-header">
  <div class="container">
    <div class="logo"><a href="{up}index.html">モノ<span>サシ</span></a></div>
    <nav class="nav-links">
      <a href="{up}nishiazabu/sushi/index.html">店舗を探す</a>
      <a href="{up}columns/index.html">鮨屋の選び方</a>
    </nav>
  </div>
</header>"""


def footer_common(up):
    return f"""<footer class="site-footer">
  <div class="container">
    <p>{BRAND} — 西麻布の鮨を、選びやすく。(プロトタイプ)</p>
    <p style="margin-top:8px;">鮨屋の選び方:<a href="{up}columns/index.html" style="color:#d4b483;text-decoration:underline;"> コラム一覧</a></p>
    <p style="margin-top:8px;">その他:<a href="{up}nishiazabu/sushi/index.html" style="color:#d4b483;text-decoration:underline;"> 西麻布エリアの鮨一覧</a> / <a href="{up}for-owners.html" style="color:#d4b483;text-decoration:underline;"> 掲載店舗様へ</a></p>
  </div>
</footer>"""


def breadcrumb_jsonld(items):
    """items: [(name, url_or_None)]"""
    entries = []
    for i, (name, url) in enumerate(items, start=1):
        entry = {"@type": "ListItem", "position": i, "name": name}
        if url:
            entry["item"] = url
        entries.append(entry)
    return json.dumps(
        {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": entries},
        ensure_ascii=False,
        indent=2,
    )


def condition_path_for_price(price_min):
    if 20000 <= price_min <= 29999:
        return "20000"
    if 30000 <= price_min <= 39999:
        return "30000"
    return None


# ---------------------------------------------------------------------------
# hikaku-card (絞り込み+比較UIで使う一覧カード) を組み立てる
# ---------------------------------------------------------------------------
def hikaku_card_html(shop, link_href):
    s = shop
    features_attr = "|".join(s["features"])
    features_pills = "".join(f'<span class="feature-pill">{esc(t)}</span>' for t in s["features"])
    return f"""      <article class="hikaku-card" data-id="{s['slug']}" data-name="{esc(s['name'])}" data-price="{s['priceMin']}" data-room="{s['room']}" data-service="{s['serviceFeeType']}" data-course-price="{esc(s['coursePriceDisplay'])}" data-service-label="{esc(s['serviceFeeLabel'])}" data-two-pax="{esc(s['twoPaxDisplay'])}" data-two-pax-num="{s['twoPaxNum']}" data-room-label="{esc(s['roomLabel'])}" data-start-label="{esc(s['startLabel'])}" data-start-hour="{s['startHourTags'][0] if s['startHourTags'] else ''}" data-reserve-url="{esc(s['tabelogUrl'])}" data-features="{esc(features_attr)}">
        <div class="hikaku-body">
          <h3 class="hikaku-name"><a href="{link_href}">{esc(s['name'])}</a></h3>
          <div class="hikaku-fields">
            <div class="field-row"><svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><text x="12" y="17" text-anchor="middle" font-size="15" font-family="sans-serif" fill="currentColor">¥</text></svg><span class="field-label">コース料金</span><span class="field-value">{esc(s['coursePriceDisplay'])}</span></div>
            <div class="field-row"><svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><text x="12" y="16" text-anchor="middle" font-size="13" font-family="sans-serif" fill="currentColor">%</text></svg><span class="field-label">サービス料</span><span class="field-value">{esc(s['serviceFeeLabel'])}</span></div>
            <div class="field-row"><svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><text x="12" y="17" text-anchor="middle" font-size="15" font-family="sans-serif" fill="currentColor">¥</text></svg><span class="field-label">2名・料理利用額</span><span class="field-value">{esc(s['twoPaxDisplay'])}</span></div>
            <div class="field-row"><svg viewBox="0 0 24 24" aria-hidden="true" focusable="false" fill="none" stroke="currentColor" stroke-width="1.8"><rect x="6" y="3" width="12" height="18" rx="1"/><circle cx="14.5" cy="12" r="1" fill="currentColor" stroke="none"/></svg><span class="field-label">個室</span><span class="field-value">{esc(s['roomLabel'])}</span></div>
            <div class="field-row"><svg viewBox="0 0 24 24" aria-hidden="true" focusable="false" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3.5 2"/></svg><span class="field-label">開始時間</span><span class="field-value">{esc(s['startLabel'])}</span></div>
          </div>
          <div class="hikaku-features">{features_pills}</div>
          <div class="hikaku-actions">
            <button type="button" class="btn-add-compare">比較に追加 ＋</button>
            <a class="btn-reserve" href="{esc(s['tabelogUrl'])}" target="_blank" rel="noopener">予約する(食べログ)</a>
          </div>
        </div>
      </article>"""


def filter_panel_html():
    return """    <div class="filter-panel">
      <div class="filter-group">
        <h3 class="filter-group-title">どんな鮨屋がいい?<span>(あてはまるものを選ぶと、それに合う店だけが表示されます/複数選択可)</span></h3>
        <div class="filter-checks" id="filter-checks">
          <label class="check-pill"><input type="checkbox" data-filter="room" value="yes"><span>個室で使いたい</span></label>
          <label class="check-pill"><input type="checkbox" data-filter="feature" value="コスパがいい"><span>コスパがいい</span></label>
          <label class="check-pill"><input type="checkbox" data-filter="feature" value="落ち着いた雰囲気"><span>落ち着いた雰囲気</span></label>
          <label class="check-pill"><input type="checkbox" data-filter="feature" value="大将との会話が楽しい"><span>大将との会話が楽しい</span></label>
          <label class="check-pill"><input type="checkbox" data-filter="feature" value="王道の江戸前鮨"><span>王道の江戸前鮨</span></label>
          <label class="check-pill"><input type="checkbox" data-filter="feature" value="モダンな鮨"><span>モダンな鮨</span></label>
          <label class="check-pill"><input type="checkbox" data-filter="feature" value="鮪が強い"><span>鮪が強い</span></label>
          <label class="check-pill"><input type="checkbox" data-filter="feature" value="シャリが特徴的"><span>シャリが特徴的</span></label>
          <label class="check-pill"><input type="checkbox" data-filter="feature" value="つまみが充実"><span>つまみが充実</span></label>
          <label class="check-pill"><input type="checkbox" data-filter="feature" value="ボリュームがある"><span>ボリュームがある</span></label>
        </div>
      </div>

      <div class="filter-group">
        <h3 class="filter-group-title">価格帯(コース料金)</h3>
        <div class="price-range">
          <select id="f-price-min" aria-label="価格帯 下限">
            <option value="15000">¥15,000</option>
            <option value="17500">¥17,500</option>
            <option value="20000">¥20,000</option>
            <option value="22500">¥22,500</option>
            <option value="25000">¥25,000</option>
            <option value="27500">¥27,500</option>
            <option value="30000">¥30,000</option>
            <option value="32500">¥32,500</option>
            <option value="35000">¥35,000</option>
          </select>
          <span class="price-range-sep">〜</span>
          <select id="f-price-max" aria-label="価格帯 上限">
            <option value="17500">¥17,500</option>
            <option value="20000">¥20,000</option>
            <option value="22500">¥22,500</option>
            <option value="25000">¥25,000</option>
            <option value="27500">¥27,500</option>
            <option value="30000">¥30,000</option>
            <option value="32500">¥32,500</option>
            <option value="35000">¥35,000</option>
            <option value="40000" selected>¥40,000</option>
          </select>
        </div>
      </div>

      <div class="filter-group filter-group-sub">
        <div class="filterbar-item">
          <div class="fb-text">
            <label for="f-start">コース開始時間</label>
            <select id="f-start">
              <option value="all">すべて</option>
              <option value="17">17時台</option>
              <option value="18">18時台</option>
            </select>
          </div>
        </div>
        <div class="filterbar-item">
          <div class="fb-text">
            <label for="f-service">サービス料</label>
            <select id="f-service">
              <option value="all">すべて</option>
              <option value="none">なし</option>
              <option value="some">あり</option>
              <option value="unknown">情報なし</option>
            </select>
          </div>
        </div>
        <div class="filterbar-item">
          <div class="fb-text">
            <label for="f-twopax">2名・料理利用額</label>
            <select id="f-twopax">
              <option value="all">すべて</option>
              <option value="t1">〜¥40,000</option>
              <option value="t2">¥40,000〜55,000</option>
              <option value="t3">¥55,000〜</option>
              <option value="unknown">情報なし</option>
            </select>
          </div>
        </div>
      </div>

      <button type="button" id="filter-reset" class="filterbar-reset">
        <svg viewBox="0 0 24 24" aria-hidden="true" focusable="false" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M4 12a8 8 0 0 1 14-5.3M20 12a8 8 0 0 1-14 5.3"/><path d="M18 4v4h-4M6 20v-4h4"/></svg>
        条件をリセット
      </button>
    </div>"""


def condition_links_html(up, current_slug=None):
    """条件別ページへのリンク一覧(要件5・要件3の内部リンクハブ)"""
    items = []
    for c in CONDITIONS:
        if c["slug"] == current_slug:
            continue
        items.append(f'<a href="{up}nishiazabu/sushi/{c["slug"]}/index.html" class="cond-link">{esc(c["navLabel"])}</a>')
    return '<div class="cond-links">' + "".join(items) + "</div>"


# ---------------------------------------------------------------------------
# 店舗詳細ページ
# ---------------------------------------------------------------------------
def build_shop_page(shop):
    s = shop
    path = f"/{AREA['slug']}/{AREA['genreSlug']}/{s['slug']}/index.html"
    up = "../../../"
    title = f"{s['name']}｜価格・個室・開始時間・特徴｜{BRAND}"
    description = f"{AREA['name']}の{AREA['genreName']}店「{s['name']}」。{s['lead']}"

    price_rows_html = "".join(
        f'<tr><td>{esc(r["label"])}</td><td class="amount">{esc(r["amount"])}</td></tr>' for r in s["priceRows"]
    )
    scene_rows_html = "".join(
        f'<tr><td>{esc(r["label"])}</td><td class="{"unknown" if r["unknown"] else ""}">{esc(r["value"])}</td></tr>'
        for r in s["sceneRows"]
    )

    info_rows = [("住所", s["address"]), ("電話番号", s["telDisplay"])]
    if s.get("openHours"):
        info_rows.append(("営業時間", s["openHours"]))
    else:
        info_rows.append(("コース開始時間", s["startLabel"]))
    info_rows.append(("定休日", s["closedDay"]))
    if s.get("seats"):
        info_rows.append(("席数", s["seats"]))
    info_rows.append(("個室", s["roomDetail"]))
    info_rows.append(("サービス料", s["serviceFeeLabel"]))
    info_rows.append(("予約", s["reserveMethod"]))
    info_dl = "".join(f"<dt>{esc(k)}</dt><dd>{esc(v)}</dd>" for k, v in info_rows)
    info_dl += f'<dt>食べログ</dt><dd><a href="{esc(s["tabelogUrl"])}" target="_blank" rel="noopener">店舗ページを見る</a></dd>'

    extra_section = ""
    if s.get("extraRows"):
        extra_dl = "".join(
            f'<dt>{esc(r["label"])}</dt><dd class="{"unknown" if r["unknown"] else ""}">{esc(r["value"])}</dd>'
            for r in s["extraRows"]
        )
        extra_section = f"""
<section class="detail-section">
  <div class="container">
    <h2>こだわりデータ</h2>
    <p class="story-text" style="margin-bottom:16px;">当メディア独自の比較項目です。公開情報から確認できた範囲のみ掲載し、不明な項目は正直に「情報なし」と表記しています。</p>
    <dl class="info-grid">{extra_dl}</dl>
  </div>
</section>"""

    features_pills = "".join(f'<span class="feature-pill">{esc(t)}</span>' for t in s["features"])

    # 関連ページ(要件5: 内部リンク)
    related_links = []
    price_cond = condition_path_for_price(s["priceMin"])
    if price_cond:
        label = "2万円台" if price_cond == "20000" else "3万円台"
        related_links.append(f'<a href="{up}nishiazabu/sushi/{price_cond}/index.html">{label}の鮨を見る</a>')
    if s["room"] == "yes":
        related_links.append(f'<a href="{up}nishiazabu/sushi/private-room/index.html">個室ありの鮨を見る</a>')
    related_links.append(f'<a href="{up}nishiazabu/sushi/index.html">同価格帯・条件で絞り込んで探す</a>')

    similar_shops = [
        o for o in SHOPS if o["slug"] != s["slug"] and set(o["features"]) & set(s["features"])
    ][:3]
    similar_html = ""
    if similar_shops:
        links = "".join(
            f'<a href="{up}nishiazabu/sushi/{o["slug"]}/index.html">{esc(o["name"])}</a>' for o in similar_shops
        )
        similar_html = f"""
      <div class="related-similar">
        <p>似ている特徴を持つ店舗:</p>
        <div class="cond-links">{links}</div>
      </div>"""

    related_section = f"""
<section class="detail-section" style="border-bottom:none;">
  <div class="container">
    <h2>関連ページ</h2>
    <div class="cond-links">{"".join(f'<span class="related-item">{l}</span>' for l in related_links)}</div>{similar_html}
    <p style="margin-top:16px;"><a href="{up}nishiazabu/sushi/index.html" style="color:#7a5f3a;text-decoration:underline;">最大3店舗で比較する</a></p>
  </div>
</section>"""

    breadcrumb_ld = breadcrumb_jsonld(
        [
            (BRAND, seo_url(f"{SITE_URL}/index.html")),
            (f"{AREA['name']}の{AREA['genreName']}", seo_url(f"{SITE_URL}/{AREA['slug']}/{AREA['genreSlug']}/index.html")),
            (s["name"], None),
        ]
    )
    restaurant_ld = {
        "@context": "https://schema.org",
        "@type": "Restaurant",
        "name": s["name"],
        "servesCuisine": "寿司",
        "telephone": s["telJsonld"],
        "address": {
            "@type": "PostalAddress",
            "streetAddress": s["streetAddress"],
            "addressLocality": "港区",
            "addressRegion": "東京都",
            "addressCountry": "JP",
        },
        "acceptsReservations": "True",
        "url": seo_url(f"{SITE_URL}{path}"),
    }
    if s.get("priceRangeJsonld"):
        restaurant_ld["priceRange"] = s["priceRangeJsonld"]

    html = f"""<!DOCTYPE html>
<html lang="ja">
<head>
{head_common(title, description, path, 3)}
<script type="application/ld+json">
{json.dumps(restaurant_ld, ensure_ascii=False, indent=2)}
</script>
<script type="application/ld+json">
{breadcrumb_ld}
</script>
</head>
<body>

{header_nav(up)}

<main>

<section class="detail-hero">
  <div class="container">
    <div class="breadcrumb"><a href="{up}nishiazabu/sushi/index.html">店舗一覧</a> / <a href="{up}nishiazabu/sushi/index.html">{esc(AREA['name'])}エリア</a> / {esc(s['name'])}</div>
    <div class="store-area">{esc(AREA['name'])}</div>
    <h1>{esc(s['name'])}</h1>
    <p class="lead">{esc(s['lead'])}</p>
    <div class="detail-tags">{features_pills}</div>
  </div>
</section>

<section class="detail-section">
  <div class="container">
    <h2>店舗紹介</h2>
    <div class="story-text">
      <p>{esc(s['storyText'])}</p>
    </div>
  </div>
</section>

<section class="detail-section">
  <div class="container">
    <h2>価格帯</h2>
    <table class="price-table">
      <tr><th>コース</th><th>価格目安</th></tr>
      {price_rows_html}
    </table>
    <p class="price-note">{esc(s['priceNote'])}</p>
  </div>
</section>

<section class="detail-section">
  <div class="container">
    <h2>利用シーン</h2>
    <table class="price-table">
      <tr><th>シーン</th><th>目安</th></tr>
      {scene_rows_html}
    </table>
  </div>
</section>

<section class="detail-section">
  <div class="container">
    <h2>基本情報</h2>
    <dl class="info-grid">{info_dl}</dl>
    <p class="price-note" style="margin-top:10px;">※「コース開始時間」は基本情報の営業時間(食べログ確認情報)から算出した目安です。実際の予約可能時間は店舗・予約先にご確認ください。</p>
  </div>
</section>
{extra_section}
<section class="detail-section" style="border-bottom:none;">
  <div class="container">
    <h2>アクセス</h2>
    <div class="map-placeholder">{esc(s['address'])}(地図は近日公開予定)</div>
    <p class="price-note" style="margin-top:14px;">{esc(s['accessNote'])}</p>
  </div>
</section>
{related_section}
</main>

{footer_common(up)}

</body>
</html>
"""
    return path, html


# ---------------------------------------------------------------------------
# 条件別ページ
# ---------------------------------------------------------------------------
def build_condition_page(cond):
    matched = [s for s in SHOPS if cond["filter"](s)]
    path = f"/{AREA['slug']}/{AREA['genreSlug']}/{cond['slug']}/index.html"
    up = "../../../"

    cards_html = "\n".join(
        hikaku_card_html(s, f"{up}nishiazabu/sushi/{s['slug']}/index.html") for s in matched
    )

    breadcrumb_ld = breadcrumb_jsonld(
        [
            (BRAND, seo_url(f"{SITE_URL}/index.html")),
            (f"{AREA['name']}の{AREA['genreName']}", seo_url(f"{SITE_URL}/{AREA['slug']}/{AREA['genreSlug']}/index.html")),
            (cond["h1"], None),
        ]
    )
    item_list_ld = {
        "@context": "https://schema.org",
        "@type": "ItemList",
        "name": cond["h1"],
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": i + 1,
                "url": seo_url(f"{SITE_URL}/{AREA['slug']}/{AREA['genreSlug']}/{s['slug']}/index.html"),
                "name": s["name"],
            }
            for i, s in enumerate(matched)
        ],
    }

    empty_note = ""
    if not matched:
        empty_note = '<p class="price-note">現在、この条件に完全に一致する店舗はありません。<a href="../index.html">西麻布の鮨一覧</a>から近い条件の店舗をお探しください。</p>'

    body_html = "\n".join(f'<p style="margin-top:16px;">{esc(p)}</p>' for p in cond.get("body", []))

    html = f"""<!DOCTYPE html>
<html lang="ja">
<head>
{head_common(cond['title'], cond['description'], path, 3)}
<script type="application/ld+json">
{json.dumps(item_list_ld, ensure_ascii=False, indent=2)}
</script>
<script type="application/ld+json">
{breadcrumb_ld}
</script>
</head>
<body>

{header_nav(up)}

<main>

<section class="detail-hero">
  <div class="container">
    <div class="breadcrumb"><a href="{up}nishiazabu/sushi/index.html">店舗一覧</a> / <a href="{up}nishiazabu/sushi/index.html">{esc(AREA['name'])}エリア</a> / {esc(cond['label'])}</div>
    <div class="store-area">{esc(AREA['name'])}</div>
    <h1>{esc(cond['h1'])}</h1>
    <p class="lead">{esc(cond['lead'])}</p>
  </div>
</section>

<section class="detail-section" style="border-bottom:none;">
  <div class="container">
    <div class="compare-result-bar">
      <span class="result-count">{len(matched)}件を表示</span>
    </div>
    <div class="hikaku-grid">
{cards_html}
    </div>
    {empty_note}
    <h2 style="margin-top:32px;">選び方のポイント</h2>
    {body_html}
    <h2 style="margin-top:32px;">他の条件で探す</h2>
    {condition_links_html(up, current_slug=cond['slug'])}
    <p style="margin-top:20px;"><a href="{up}nishiazabu/sushi/index.html" style="color:#7a5f3a;text-decoration:underline;">絞り込み・3店舗比較はこちら</a></p>
  </div>
</section>

</main>

{footer_common(up)}

</body>
</html>
"""
    return path, html


# ---------------------------------------------------------------------------
# エリア×ジャンル トップページ(/nishiazabu/sushi/index.html)
# ---------------------------------------------------------------------------
def build_area_top_page():
    path = f"/{AREA['slug']}/{AREA['genreSlug']}/index.html"
    up = "../../"
    title = f"{AREA['name']}の{AREA['genreName']}を比較｜価格・個室・開始時間から選ぶ｜{BRAND}"
    description = f"{AREA['name']}の{AREA['genreName']}店から、大切な相手を安心して連れていける店だけを厳選した{len(SHOPS)}店舗を掲載。価格帯・個室・特徴・開始時間で絞り込んで比較できる意思決定サイト「{BRAND}」です。"

    cards_html = "\n".join(
        hikaku_card_html(s, f"{s['slug']}/index.html") for s in SHOPS
    )

    room_count = sum(1 for s in SHOPS if s["room"] == "yes")
    price_values = sorted(s["priceMin"] for s in SHOPS)

    faq_ld = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": f"{AREA['name']}で個室がある{AREA['genreName']}屋はありますか？",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": f"{AREA['name']}エリアの掲載{len(SHOPS)}店舗のうち、{room_count}店舗が個室・半個室を備えています。2〜8名程度の少人数個室が中心です。個室の有無は店舗ごとに異なるため、各店舗ページでご確認ください。",
                },
            },
            {
                "@type": "Question",
                "name": f"{AREA['name']}の{AREA['genreName']}屋の予算相場はどれくらいですか？",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": f"掲載店舗のディナーのおまかせコースは、1人{price_values[0]:,}円〜{price_values[-1]:,}円(税込)が中心です。同じ価格帯でもサービス料の有無で実際の支払額は変わるため、各店舗ページの「2名・料理利用額」もあわせてご確認ください。",
                },
            },
            {
                "@type": "Question",
                "name": f"{AREA['name']}の{AREA['genreName']}屋は何駅から近いですか？",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": "六本木駅・広尾駅・乃木坂駅からいずれも徒歩2〜15分程度の範囲に集まっています。",
                },
            },
        ],
    }
    breadcrumb_ld = breadcrumb_jsonld(
        [
            (BRAND, seo_url(f"{SITE_URL}/index.html")),
            (f"{AREA['name']}の{AREA['genreName']}", None),
        ]
    )

    cond_cards = "".join(
        f'<a href="{c["slug"]}/index.html" class="cond-card"><span class="cond-card-label">{esc(c["label"])}</span><span class="cond-card-arrow">→</span></a>'
        for c in CONDITIONS
        if c["slug"] != "osusume"
    )

    html = f"""<!DOCTYPE html>
<html lang="ja">
<head>
{head_common(title, description, path, 2)}
<script type="application/ld+json">
{json.dumps(faq_ld, ensure_ascii=False, indent=2)}
</script>
<script type="application/ld+json">
{breadcrumb_ld}
</script>
</head>
<body>

{header_nav(up)}

<main>

<section class="detail-hero">
  <div class="container">
    <div class="breadcrumb"><a href="{up}index.html">トップ</a> / {esc(AREA['name'])}の{esc(AREA['genreName'])}</div>
    <div class="store-area">{esc(AREA['name'])}</div>
    <h1>{esc(AREA['name'])}の{esc(AREA['genreName'])}を比較する</h1>
    <p class="lead">気になる店舗は「比較に追加」で最大3店舗まで並べて見られます。掲載{len(SHOPS)}店舗はすべてオンライン予約が可能な厳選店です。</p>
  </div>
</section>

<section class="stores">
  <div class="container">
    <h2 style="margin-bottom:16px;">目的から探す</h2>
    <div class="cond-card-grid">{cond_cards}</div>

{filter_panel_html()}
    <div class="compare-result-bar">
      <span id="result-count" class="result-count"></span>
    </div>

    <div class="hikaku-grid" id="hikaku-grid">
{cards_html}
    </div>

    <div class="compare-tray" id="compare-tray" hidden>
      <div class="compare-tray-head">
        <h2>3店舗比較</h2>
        <p>最大3店舗まで比較できます。</p>
      </div>
      <div class="compare-table-wrap" id="compare-table-wrap"></div>
      <p class="compare-empty" id="compare-empty" hidden>比較する店舗を選んでください。</p>
    </div>
  </div>
</section>

<section class="detail-section" style="border-bottom:none;">
  <div class="container">
    <h2>{esc(AREA['name'])}で{esc(AREA['genreName'])}屋を選ぶなら</h2>
    <div class="area-intro">
      <p>{esc(AREA['name'])}は大使館や高級住宅街に囲まれた閑静なエリアで、隠れ家的な名店が多く集まる{esc(AREA['genreName'])}激戦区のひとつです。大通りに面した看板の少ない店も多く、"知る人ぞ知る"一軒との出会い方が難しいエリアでもあります。</p>
      <p>以下は、店舗の公式サイトや飲食店情報サイトで公開されている情報をもとにまとめた参考情報です。個室の有無・価格帯・アクセスを軸に、目的に合わせてお選びいただけます。</p>
    </div>

    <h2 style="margin-top:32px;">よくある質問</h2>
    <div class="faq-list">
{"".join(f'''      <div class="faq-item">
        <div class="q">{esc(qa["name"])}</div>
        <div class="a">{esc(qa["acceptedAnswer"]["text"])}</div>
      </div>''' for qa in faq_ld["mainEntity"])}
    </div>

    <div class="area-links">
      <a href="{up}index.html">サービストップに戻る</a>
    </div>
  </div>
</section>

</main>

{footer_common(up)}

<script src="{up}script.js"></script>
</body>
</html>
"""
    return path, html


# ---------------------------------------------------------------------------
# 旧URLの案内(リダイレクト)ページ
# ---------------------------------------------------------------------------
def build_redirect_page(new_path, depth, title):
    up = "../" * depth
    new_path = seo_url(new_path)
    new_url = f"{SITE_URL}{new_path}"
    # ルート相対で組み直す(旧ファイルからの相対パス)
    rel = up + new_path.lstrip("/")
    return f"""<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{esc(title)}</title>
<link rel="canonical" href="{new_url}">
<meta http-equiv="refresh" content="0; url={rel}">
<link rel="stylesheet" href="{up}style.css">
</head>
<body>
<header class="site-header">
  <div class="container">
    <div class="logo"><a href="{up}index.html">モノ<span>サシ</span></a></div>
  </div>
</header>
<section class="detail-section">
  <div class="container">
    <p>このページは新しいURLに移動しました。自動的に移動しない場合は、下記のリンクからお進みください。</p>
    <p style="margin-top:16px;"><a href="{rel}" style="color:#7a5f3a;text-decoration:underline;">{esc(title)}へ進む</a></p>
  </div>
</section>
</body>
</html>
"""


# ---------------------------------------------------------------------------
# sitemap.xml / robots.txt
# ---------------------------------------------------------------------------
def build_sitemap(urls):
    entries = "\n".join(f"  <url><loc>{seo_url(SITE_URL + u)}</loc></url>" for u in urls)
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{entries}
</urlset>
"""


def build_robots():
    return f"""User-agent: *
Allow: /

Sitemap: {SITE_URL}/sitemap.xml
"""


def write(rel_path, content):
    full = os.path.join(ROOT, rel_path.lstrip("/"))
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(content)
    return rel_path


def main():
    written = []

    # 店舗詳細ページ
    for s in SHOPS:
        path, html = build_shop_page(s)
        written.append(write(path, html))

    # 条件別ページ
    for c in CONDITIONS:
        path, html = build_condition_page(c)
        written.append(write(path, html))

    # エリアトップ
    path, html = build_area_top_page()
    written.append(write(path, html))

    # 旧shops/*.html を新URLへの案内ページに置換
    for s in SHOPS:
        old_path = f"shops/{s['slug']}.html"
        new_path = f"/{AREA['slug']}/{AREA['genreSlug']}/{s['slug']}/index.html"
        html = build_redirect_page(new_path, depth=1, title=f"{s['name']}｜{BRAND}")
        written.append(write(old_path, html))

    # 旧areas/nishiazabu.html を新URLへの案内ページに置換
    old_area_path = "areas/nishiazabu.html"
    new_area_path = f"/{AREA['slug']}/{AREA['genreSlug']}/index.html"
    html = build_redirect_page(new_area_path, depth=1, title=f"{AREA['name']}の{AREA['genreName']}を比較｜{BRAND}")
    written.append(write(old_area_path, html))

    # sitemap.xml / robots.txt
    sitemap_urls = ["/index.html", f"/{AREA['slug']}/{AREA['genreSlug']}/index.html"]
    sitemap_urls += [f"/{AREA['slug']}/{AREA['genreSlug']}/{s['slug']}/index.html" for s in SHOPS]
    sitemap_urls += [f"/{AREA['slug']}/{AREA['genreSlug']}/{c['slug']}/index.html" for c in CONDITIONS]
    sitemap_urls += ["/columns/index.html", "/columns/date-guide.html", "/columns/entertain-guide.html", "/columns/anniversary-guide.html", "/columns/scene-guide.html", "/for-owners.html"]
    written.append(write("sitemap.xml", build_sitemap(sitemap_urls)))
    written.append(write("robots.txt", build_robots()))

    print(f"生成完了: {len(written)}ファイル")
    for w in written:
        print(" -", w)


if __name__ == "__main__":
    main()
