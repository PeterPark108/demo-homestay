#!/usr/bin/env python3
"""Sinh các trang tĩnh của bản hotel-v2 (chạy: python3 build.py). Không cần thư viện ngoài."""
import json, html, os
ROOT = os.path.dirname(os.path.abspath(__file__))
SITE = "https://example.invalid/nha-gio"  # canonical placeholder – thay khi có tên miền thật
E = html.escape
ROOMS = [  # khớp SEED_ROOMS trong js/data.js
 dict(id='r1',slug='phong-song-bien',name='Phòng Sóng Biển',type='Phòng đôi',price=850000,clean=100000,guests=2,beds='1 giường đôi',size=28,scene='sea',pal=0,amen=['wifi','ac','view','balcony','tv','breakfast'],desc='Phòng đôi ấm cúng với cửa kính lớn nhìn ra vịnh. Buổi sáng mở rèm là thấy bình minh trên biển, tối nghe tiếng sóng.'),
 dict(id='r2',slug='bungalow-dua',name='Bungalow Dừa',type='Bungalow',price=1200000,clean=150000,guests=3,beds='1 giường đôi + 1 sofa giường',size=35,scene='sea',pal=1,amen=['wifi','ac','view','balcony','bbq','parking'],desc='Bungalow mái lá giữa vườn dừa, vài bước chân ra bãi cát. Hiên gỗ rộng để nằm võng đọc sách.'),
 dict(id='r3',slug='can-doi-thong',name='Căn Đồi Thông',type='Nguyên căn',price=2200000,clean=250000,guests=6,beds='3 phòng ngủ',size=90,scene='hill',pal=2,amen=['wifi','hill','kitchen','bbq','parking','washer','pet'],desc='Nguyên căn nhà gỗ trên sườn đồi thông, có bếp đầy đủ, sân cỏ và khu nướng BBQ. Hợp nhóm bạn hoặc đại gia đình.'),
 dict(id='r4',slug='phong-gac-mai',name='Phòng Gác Mái',type='Phòng đôi',price=650000,clean=80000,guests=2,beds='1 giường đôi',size=22,scene='hill',pal=3,amen=['wifi','hill','tv','breakfast'],desc='Phòng gác mái nhỏ xinh với cửa sổ trời, nhìn ra rừng thông. Hợp cặp đôi hoặc người đi một mình.'),
 dict(id='r5',slug='phong-gia-dinh-hoa-giay',name='Phòng Gia Đình Hoa Giấy',type='Phòng gia đình',price=1500000,clean=150000,guests=4,beds='2 giường đôi',size=42,scene='sea',pal=4,amen=['wifi','ac','view','tv','bath','breakfast','parking'],desc='Phòng rộng cho gia đình 4 người, ban công phủ hoa giấy, có bồn tắm và góc chơi cho bé.'),
 dict(id='r6',slug='studio-ghenh-rang',name='Studio Ghềnh Ráng',type='Studio',price=1000000,clean=120000,guests=3,beds='1 giường đôi + 1 giường đơn',size=32,scene='sea',pal=5,amen=['wifi','ac','kitchen','washer','tv'],desc='Studio có bếp nhỏ và bàn làm việc, hợp ở dài ngày. Gần điểm ngắm hoàng hôn (vị trí minh họa).'),
 dict(id='r7',slug='villa-ho-boi-eo-gio',name='Villa Hồ Bơi Eo Gió',type='Nguyên căn',price=3500000,clean=400000,guests=8,beds='4 phòng ngủ',size=160,scene='pool',pal=6,amen=['wifi','ac','view','pool','kitchen','bbq','parking','washer','bath'],desc='Villa riêng có hồ bơi, sân hiên hướng biển và bếp lớn. Phù hợp kỳ nghỉ nhóm 6–8 người.'),
]
AMEN={'wifi':('📶','Wi‑Fi'),'ac':('❄️','Điều hòa'),'view':('🌅','Hướng biển'),'hill':('🌲','Hướng đồi thông'),'balcony':('🪴','Ban công'),'tv':('📺','Smart TV'),'kitchen':('🍳','Bếp riêng'),'pool':('🏊','Hồ bơi'),'bbq':('🔥','Khu BBQ'),'parking':('🅿️','Chỗ đậu xe'),'washer':('🧺','Máy giặt'),'breakfast':('🥐','Bữa sáng'),'pet':('🐾','Cho thú cưng'),'bath':('🛁','Bồn tắm')}
money=lambda n: f"{n:,}".replace(',', '.')+'₫'
NAV=[('index.html','Trang chủ'),('phong/index.html','Loại phòng'),('tien-ich.html','Tiện ích'),('thu-vien-anh.html','Thư viện ảnh'),('uu-dai.html','Ưu đãi'),('danh-gia.html','Đánh giá'),('lien-he.html','Liên hệ')]

def art(kind,pal,label,cls='',tag=True):
    return f'<div class="art {cls}" data-art="{kind}" data-pal="{pal}" data-label="{E(label)} (ảnh minh họa)">{"<span class=tag aria-hidden=true>Minh họa</span>" if tag else ""}</div>'

def page(path,title,desc,body,current=None,jsonld=None,extra_head=''):
    depth=path.count('/'); p='../'*depth
    navh=''.join(f'<li><a href="{p}{h}"{" aria-current=page" if h==current else ""}>{t}</a></li>' for h,t in NAV)
    ld=[{"@context":"https://schema.org","@type":"Hotel","name":"Nhà Gió (bản demo)","description":"Website demo – khách sạn giả lập, không phải doanh nghiệp thật. Nội dung, giá và địa chỉ đều là minh họa.","url":SITE+'/',"address":{"@type":"PostalAddress","streetAddress":"Địa chỉ minh họa","addressCountry":"VN"},"telephone":"0900 000 000","priceRange":"Giá minh họa","checkinTime":"14:00","checkoutTime":"12:00"}]
    if jsonld: ld.append(jsonld)
    can=SITE+'/'+('' if path=='index.html' else path)
    return f'''<!doctype html>
<html lang="vi"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{E(title)} · Nhà Gió (demo)</title>
<meta name="description" content="{E(desc)}">
<meta name="robots" content="noindex,nofollow">
<link rel="canonical" href="{can}">
<meta property="og:type" content="website"><meta property="og:locale" content="vi_VN"><meta property="og:site_name" content="Nhà Gió (demo)">
<meta property="og:title" content="{E(title)} · Nhà Gió (demo)"><meta property="og:description" content="{E(desc)}"><meta property="og:url" content="{can}"><meta property="og:image" content="{SITE}/assets/og.svg">
<meta name="theme-color" content="#b5472c">
<link rel="icon" href="{p}assets/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="{p}assets/site.css">{extra_head}
<script type="application/ld+json">{json.dumps(ld if len(ld)>1 else ld[0],ensure_ascii=False)}</script>
</head><body>
<a class="skip" href="#main">Bỏ qua, đến nội dung chính</a>
<div class="demo-bar" role="note"><b>Bản demo.</b> Nội dung, giá và hình ảnh đều là minh họa – không nhận đặt phòng thật.</div>
<header class="top"><div class="wrap top-in">
<a class="logo" href="{p}index.html"><span class="lg-ico" aria-hidden="true">⌂</span><span>Nhà Gió<small>Khách sạn ven biển · demo</small></span></a>
<button id="menuBtn" class="menu-btn" aria-expanded="false" aria-controls="nav"><span aria-hidden="true">☰</span><span class="t">Menu</span></button>
<nav id="nav" class="nav" aria-label="Điều hướng chính"><ul>{navh}<li><a class="cta" href="{p}dat-phong.html"{" aria-current=page" if current=="dat-phong.html" else ""}>Đặt phòng</a></li></ul></nav>
</div></header>
<main id="main" tabindex="-1">
{body}
</main>
<footer class="foot"><div class="wrap">
<div class="foot-in">
<div><h2>Nhà Gió (demo)</h2><p>Địa chỉ minh họa, thành phố ven biển, Việt Nam<br>Điện thoại: 0900 000 000 (số mẫu)<br>Email: xinchao@vidu.test (mẫu)</p></div>
<div><h2>Lưu trú</h2><ul><li><a href="{p}phong/index.html">Loại phòng</a></li><li><a href="{p}dat-phong.html">Đặt phòng</a></li><li><a href="{p}uu-dai.html">Ưu đãi</a></li><li><a href="{p}tien-ich.html">Tiện ích &amp; dịch vụ</a></li></ul></div>
<div><h2>Thông tin</h2><ul><li><a href="{p}faq.html">Câu hỏi thường gặp</a></li><li><a href="{p}chinh-sach.html">Chính sách</a></li><li><a href="{p}lien-he.html">Vị trí &amp; liên hệ</a></li><li><a href="{p}danh-gia.html">Đánh giá mẫu</a></li></ul></div>
<div><h2>Bản cũ</h2><ul><li><a href="{p}homestay-v1/index.html">Demo homestay v1</a></li><li><a href="{p}homestay-v1/index.html#/quan-ly">Trang quản lý (demo)</a></li><li><a href="{p}thu-vien-anh.html">Thư viện ảnh</a></li></ul></div>
</div>
<p class="demo"><b>Lưu ý bản demo:</b> Nhà Gió là khách sạn giả lập để trình diễn giao diện. Giá, đánh giá, địa chỉ, số điện thoại đều là minh họa; không có giấy phép kinh doanh thật; ảnh là tranh SVG tự vẽ. Không có dữ liệu nào được gửi lên máy chủ. © <span data-year>2026</span></p>
</div></footer>
<div id="toasts" aria-live="polite"></div>
<script src="{p}js/data.js"></script><script src="{p}js/art.js"></script><script src="{p}assets/site.js"></script>
</body></html>
'''

def crumb(p,items):
    li=''.join(f'<li><a href="{p}{h}">{t}</a></li>' if h else f'<li aria-current="page">{t}</li>' for h,t in items)
    return f'<nav class="crumb" aria-label="Đường dẫn"><ol>{li}</ol></nav>'
def head(p,title,lead,items):
    return f'<section class="page-h"><div class="wrap">{crumb(p,items)}<h1>{title}</h1><p>{lead}</p></div></section>'

def card(r,p,order=0,showbadge=False):
    return f'''<li data-room data-type="{E(r['type'])}" data-guests="{r['guests']}" data-price="{r['price']}" data-order="{order}"><article class="card">
{art(r['scene'],r['pal'],r['name'])}{'<span class="badge">Nổi bật</span>' if showbadge else ''}
<div class="cb"><p class="sm muted" style="margin:0">{E(r['type'])}</p><h3><a href="{p}phong/{r['slug']}.html">{E(r['name'])}</a></h3>
<p class="meta">{r['guests']} khách · {E(r['beds'])} · {r['size']} m²</p>
<p class="price"><b>{money(r['price'])}</b> <span class="muted sm">/ đêm · giá minh họa</span></p></div></article></li>'''

REVIEWS=[('Khách mẫu A','Phòng Sóng Biển',5,'Nội dung demo: phòng sạch, nhìn ra biển, nhân viên chỉ đường nhiệt tình.'),('Khách mẫu B','Căn Đồi Thông',5,'Nội dung demo: nhà rộng, bếp đủ đồ, buổi tối nướng BBQ rất vui.'),('Khách mẫu C','Studio Ghềnh Ráng',4,'Nội dung demo: Wi‑Fi ổn để làm việc, bếp nhỏ tiện nấu ăn.'),('Khách mẫu D','Villa Hồ Bơi Eo Gió',5,'Nội dung demo: hồ bơi riêng, cả nhóm 8 người ở thoải mái.'),('Khách mẫu E','Phòng Gia Đình Hoa Giấy',4,'Nội dung demo: bé rất thích góc chơi, bồn tắm rộng.'),('Khách mẫu F','Bungalow Dừa',5,'Nội dung demo: hiên gỗ, võng và tiếng sóng – đúng như ảnh minh họa.')]
def rv(n,room,s,t):
    return f'<li><figure class="rv"><div class="who"><span class="av" aria-hidden="true">{n[-1]}</span><div><b>{n}</b><br><span class="sm muted">{room}</span></div></div><p class="stars" aria-label="{s} trên 5 sao (mẫu)">{"★"*s}{"☆"*(5-s)}</p><blockquote><p>{t}</p></blockquote><figcaption><span class="demo-tag">Đánh giá mẫu (demo)</span></figcaption></figure></li>'

OFFERS=[('Ở 3 đêm, giảm 10%','sea',0,'DEMO3DEM','Áp dụng minh họa cho mọi loại phòng khi ở từ 3 đêm.'),('Đặt sớm 30 ngày','hill',2,'DEMOSOM','Giảm minh họa 15% khi đặt trước tối thiểu 30 ngày.'),('Gói gia đình cuối tuần','pool',6,'DEMOGIADINH','Tặng bữa sáng cho 2 trẻ em (nội dung demo).'),('Ở dài ngày làm việc từ xa','bed',5,'DEMOREMOTE','Từ 7 đêm: giá tuần minh họa, giặt ủi miễn phí.')]
def offer(t,k,pal,code,d,p):
    return f'<li><article class="offer">{art(k,pal,t)}<div class="ob"><span class="demo-tag">Ưu đãi minh họa</span><h3 style="margin-top:8px">{t}</h3><p class="muted">{d}</p><p class="sm">Mã: <span class="code">{code}</span> (mã demo, không có giá trị)</p><a class="btn" href="{p}dat-phong.html">Đặt với ưu đãi</a></div></article></li>'

MAP='''<svg viewBox="0 0 800 450" role="img" aria-labelledby="mapT mapD" xmlns="http://www.w3.org/2000/svg"><title id="mapT">Bản đồ minh họa</title><desc id="mapD">Sơ đồ minh họa không theo tỉ lệ: khách sạn Nhà Gió nằm giữa bãi biển và đồi thông, gần chợ và bến xe (vị trí giả lập).</desc>
<rect width="800" height="450" fill="#eef4e8"/><path d="M0 300 Q200 260 400 300 T800 280 L800 450 L0 450z" fill="#8ecae6"/><path d="M0 290 Q200 250 400 290 T800 270 L800 290 Q600 300 400 315 T0 310z" fill="#f3d9a4"/>
<path d="M560 0 Q620 120 800 140 L800 0z" fill="#b7d3a8"/><g fill="#52796f"><path d="M640 40 l12 -30 l12 30z"/><path d="M690 70 l12 -30 l12 30z"/><path d="M740 50 l12 -30 l12 30z"/></g>
<g stroke="#fff" stroke-width="14" fill="none" stroke-linecap="round"><path d="M0 230 H800"/><path d="M300 0 V230"/><path d="M560 230 Q600 150 700 110"/></g>
<g stroke="#d6cbb8" stroke-width="2" fill="none" stroke-dasharray="6 6"><path d="M0 230 H800"/><path d="M300 0 V230"/></g>
<rect x="120" y="120" width="110" height="70" rx="8" fill="#fff" stroke="#a8917c"/><text x="175" y="160" text-anchor="middle" font-size="16" fill="#2b2622" font-family="system-ui">Chợ (minh họa)</text>
<rect x="340" y="60" width="130" height="70" rx="8" fill="#fff" stroke="#a8917c"/><text x="405" y="100" text-anchor="middle" font-size="16" fill="#2b2622" font-family="system-ui">Bến xe (minh họa)</text>
<g transform="translate(470 250)"><circle r="30" fill="#b5472c"/><path d="M-14 4 L0 -12 L14 4 V16 H-14z" fill="#fff"/></g><rect x="390" y="182" width="160" height="34" rx="17" fill="#2b2622"/><text x="470" y="205" text-anchor="middle" font-size="16" fill="#fff" font-weight="700" font-family="system-ui">Nhà Gió (demo)</text>
<text x="640" y="380" font-size="18" fill="#1f5f63" font-family="system-ui" font-weight="700">Biển (minh họa)</text><text x="640" y="125" font-size="15" fill="#2d4a35" font-family="system-ui">Đồi thông</text></svg>'''

def bbar(p):
    return f'''<form class="bbar" action="{p}dat-phong.html" method="get" aria-label="Kiểm tra phòng trống" novalidate>
<div class="f"><label for="bb-ci">Nhận phòng</label><input id="bb-ci" name="ci" type="date" required></div>
<div class="f"><label for="bb-co">Trả phòng</label><input id="bb-co" name="co" type="date" required></div>
<div class="f g"><label for="bb-gg">Số khách</label><select id="bb-gg" name="g">{''.join(f'<option value="{i}"{" selected" if i==2 else ""}>{i} khách</option>' for i in range(1,9))}</select></div>
<button class="btn primary lg" type="submit">Kiểm tra phòng</button><p class="err" role="alert"></p></form>'''

pages={}
# --- Trang chủ
p=''
FEAT=[('🌊','Sát biển','Vài bước chân ra bãi cát (mô tả minh họa).'),('🏊','Hồ bơi','Hồ bơi ngoài trời mở 6:00–21:00.'),('🥐','Bữa sáng','Bữa sáng địa phương phục vụ tại sảnh.'),('🚲','Xe đạp','Mượn xe đạp dạo quanh khu phố.')]
feats=''.join(f'<li class="feat"><div class="ico" aria-hidden="true">{i}</div><h3>{t}</h3><p>{d}</p></li>' for i,t,d in FEAT)
pages['index.html']=('Khách sạn ven biển – đặt phòng trực tuyến','Nhà Gió (demo): khách sạn ven biển giả lập với 7 loại phòng, hồ bơi, bữa sáng. Website trình diễn – giá và nội dung minh họa.',f'''
<section class="hero">{art('sea',0,'Toàn cảnh khách sạn bên bờ biển',tag=False)}<div class="wrap hero-in">
<p class="eyebrow">Khách sạn ven biển · bản demo</p><h1>Nghỉ ngơi nơi gió biển gặp đồi thông</h1>
<p class="lead">7 loại phòng từ phòng đôi gác mái đến villa hồ bơi. Chọn ngày, xem tạm tính ngay – mọi giá trên trang là giá minh họa.</p>
{bbar(p)}</div></section>
<section class="sec" aria-labelledby="h-rooms"><div class="wrap"><div class="sec-h"><div><p class="eyebrow">Lưu trú</p><h2 id="h-rooms">Phòng nổi bật</h2></div><a href="phong/index.html">Xem tất cả loại phòng →</a></div>
<ul class="grid" style="list-style:none;padding:0;margin:0">{''.join(card(r,p,i,True) for i,r in enumerate([ROOMS[0],ROOMS[2],ROOMS[6]]))}</ul></div></section>
<section class="sec alt" aria-labelledby="h-am"><div class="wrap"><div class="sec-h"><div><p class="eyebrow">Tiện ích</p><h2 id="h-am">Mọi thứ cho một kỳ nghỉ nhẹ nhàng</h2></div><a href="tien-ich.html">Tất cả tiện ích →</a></div>
<ul class="grid g4" style="list-style:none;padding:0;margin:0">{feats}</ul></div></section>
<section class="sec" aria-labelledby="h-of"><div class="wrap"><div class="sec-h"><div><p class="eyebrow">Ưu đãi</p><h2 id="h-of">Ưu đãi minh họa</h2></div><a href="uu-dai.html">Xem ưu đãi →</a></div>
<ul class="grid" style="list-style:none;padding:0;margin:0;grid-template-columns:repeat(auto-fill,minmax(min(100%,460px),1fr))">{''.join(offer(*o,p) for o in OFFERS[:2])}</ul></div></section>
<section class="sec alt" aria-labelledby="h-rv"><div class="wrap"><div class="sec-h"><div><p class="eyebrow">Khách nói gì</p><h2 id="h-rv">Đánh giá mẫu</h2></div><a href="danh-gia.html">Đọc thêm →</a></div>
<p class="note">Các đánh giá dưới đây là <b>nội dung mẫu (demo)</b> để minh họa bố cục, không phải đánh giá của khách thật.</p>
<ul class="grid" style="list-style:none;padding:0;margin:16px 0 0">{''.join(rv(*x) for x in REVIEWS[:3])}</ul></div></section>
<section class="sec" aria-labelledby="h-loc"><div class="wrap split"><div><p class="eyebrow">Vị trí</p><h2 id="h-loc">Giữa biển và đồi thông</h2><p class="muted">Địa chỉ minh họa. Bản đồ là sơ đồ tự vẽ, không theo tỉ lệ.</p>
<ul class="ticks"><li>Ra bãi biển: đi bộ (mô tả minh họa)</li><li>Chợ địa phương gần khách sạn</li><li>Hỗ trợ đặt xe đưa đón (dịch vụ demo)</li></ul><a class="btn" href="lien-he.html">Xem vị trí &amp; liên hệ</a></div>
<div class="map">{MAP}</div></div></section>''','index.html')

# --- Loại phòng
p='../'
types=sorted({r['type'] for r in ROOMS})
pages['phong/index.html']=('Các loại phòng','Danh sách 7 loại phòng tại Nhà Gió (demo): lọc theo loại, số khách, sắp xếp theo giá minh họa.',head(p,'Các loại phòng','Lọc theo loại phòng và số khách, sắp xếp theo giá. Giá hiển thị là giá minh họa mỗi đêm.',[('index.html','Trang chủ'),(None,'Loại phòng')])+f'''
<section class="sec" style="padding-top:24px"><div class="wrap">
<div class="toolbar" role="search" aria-label="Lọc phòng">
<div class="fg"><label for="f-type">Loại phòng</label><select id="f-type"><option value="">Tất cả</option>{''.join(f'<option>{E(t)}</option>' for t in types)}</select></div>
<div class="fg"><label for="f-guests">Số khách tối thiểu</label><select id="f-guests"><option value="">Bất kỳ</option>{''.join(f'<option value="{i}">{i}+ khách</option>' for i in (2,3,4,6,8))}</select></div>
<div class="fg"><label for="f-sort">Sắp xếp</label><select id="f-sort"><option value="">Đề xuất</option><option value="asc">Giá thấp → cao</option><option value="desc">Giá cao → thấp</option><option value="guests">Sức chứa lớn nhất</option></select></div>
<p class="count muted" id="count" aria-live="polite">{len(ROOMS)} loại phòng</p></div>
<ul class="grid" id="roomList" style="list-style:none;padding:0;margin:0">{''.join(card(r,p,i) for i,r in enumerate(ROOMS))}</ul>
<div class="empty" id="empty" hidden><h2>Không có phòng phù hợp</h2><p class="muted">Thử bỏ bớt điều kiện lọc.</p><button class="btn primary" id="resetF" type="button">Xóa bộ lọc</button></div>
</div></section>''','phong/index.html')

# --- Chi tiết phòng
GKINDS=lambda r:[(r['scene'],'Toàn cảnh'),('bed','Phòng ngủ'),('kitchen' if 'kitchen' in r['amen'] else 'living','Bếp' if 'kitchen' in r['amen'] else 'Phòng khách'),('bath','Phòng tắm'),('living','Góc thư giãn')]
for r in ROOMS:
    gal=''.join(f'<button type="button" data-lb data-art="{k}" data-pal="{r["pal"]}" data-cap="{E(r["name"])} – {c} (ảnh minh họa)" aria-label="Phóng to ảnh: {c}">{art(k,r["pal"],r["name"]+" – "+c)}</button>' for k,c in GKINDS(r))
    am=''.join(f'<li><span aria-hidden="true">{AMEN[a][0]}</span>{AMEN[a][1]}</li>' for a in r['amen'])
    others=''.join(card(o,p,i) for i,o in enumerate([x for x in ROOMS if x is not r][:3]))
    ld={"@context":"https://schema.org","@type":"HotelRoom","name":r['name']+" (demo)","description":r['desc']+" Nội dung minh họa.","occupancy":{"@type":"QuantitativeValue","maxValue":r['guests']},"floorSize":{"@type":"QuantitativeValue","value":r['size'],"unitCode":"MTK"}}
    body=f'''<div class="wrap" style="padding-top:24px">{crumb(p,[('index.html','Trang chủ'),('phong/index.html','Loại phòng'),(None,r['name'])])}
<h1>{E(r['name'])}</h1><p class="muted">{E(r['type'])} · {r['guests']} khách · {E(r['beds'])} · {r['size']} m² · <span class="demo-tag">Nội dung demo</span></p>
<div class="gal" aria-label="Thư viện ảnh phòng">{gal}</div>
<div class="dt"><div class="dt-main">
<section aria-labelledby="h-ab" style="border-top:0"><h2 id="h-ab">Giới thiệu phòng</h2><p>{E(r['desc'])}</p><ul class="facts"><li>👥 Tối đa {r['guests']} khách</li><li>🛏️ {E(r['beds'])}</li><li>📐 {r['size']} m²</li><li>🕑 Nhận 14:00 · Trả 12:00</li></ul></section>
<section aria-labelledby="h-am"><h2 id="h-am">Tiện nghi trong phòng</h2><ul class="amen">{am}</ul></section>
<section aria-labelledby="h-cal"><h2 id="h-cal">Chọn ngày</h2><p class="sm muted">Chọn ngày nhận rồi ngày trả phòng. Ngày "đã kín" là dữ liệu minh họa.</p>
<div id="cal" class="cal"></div>
<ul class="legend"><li><span class="lgd"></span>Còn trống</li><li><span class="lgd sel"></span>Đã chọn</li><li><span class="lgd in"></span>Trong khoảng</li><li><span class="lgd bk"></span>Đã kín</li><li><span class="lgd past"></span>Đã qua</li></ul></section>
<section aria-labelledby="h-po"><h2 id="h-po">Chính sách tóm tắt</h2><ul><li>Hủy miễn phí trước 3 ngày (chính sách minh họa)</li><li>Trẻ dưới 6 tuổi ở miễn phí khi dùng giường có sẵn</li><li>{'Cho phép thú cưng nhỏ' if 'pet' in r['amen'] else 'Không nhận thú cưng ở loại phòng này'}</li></ul><a href="../chinh-sach.html">Xem đầy đủ chính sách</a></section>
</div>
<aside aria-labelledby="h-bb"><div class="bbox" id="bbox" data-room="{r['id']}">
<h2 id="h-bb" class="sr-only">Đặt phòng {E(r['name'])}</h2>
<p style="margin:0"><span class="rate">{money(r['price'])}</span> <span class="muted">/ đêm</span></p><p class="sm muted" style="margin:0">Giá minh họa</p>
<div class="picked"><div><small>Nhận phòng</small><span id="bb-ci">—</span></div><div><small>Trả phòng</small><span id="bb-co">—</span></div></div>
<div class="fg"><label for="bb-g">Số khách</label><select id="bb-g">{''.join(f'<option value="{i}"{" selected" if i==min(2,r["guests"]) else ""}>{i} khách</option>' for i in range(1,r['guests']+1))}</select></div>
<a class="btn primary full lg" id="bb-go" data-base="../dat-phong.html" href="../dat-phong.html?room={r['id']}">Chọn ngày để xem tạm tính</a>
<p class="err" id="bb-msg" role="alert"></p>
<dl class="calc" id="bb-calc" aria-live="polite"></dl>
<p class="sm muted center" style="margin-top:12px">Tạm tính, giá minh họa · chưa thu tiền</p></div></aside></div>
<section class="sec" aria-labelledby="h-ot"><h2 id="h-ot">Phòng khác</h2><ul class="grid" style="list-style:none;padding:0;margin:0">{others}</ul></section></div>
<dialog class="lb" id="lb" aria-label="Xem ảnh lớn"><div class="lb-in"><div class="art"></div><p class="lb-cap"><span id="lbCap"></span><span id="lbNum"></span></p>
<button class="x" type="button" aria-label="Đóng">✕</button><button class="pv" type="button" aria-label="Ảnh trước">‹</button><button class="nx" type="button" aria-label="Ảnh sau">›</button></div></dialog>'''
    pages[f'phong/{r["slug"]}.html']=(r['name'],f'{r["name"]} – {r["type"]}, tối đa {r["guests"]} khách, {r["size"]} m². Xem ảnh minh họa, tiện nghi, lịch trống và tạm tính (demo).',body,'phong/index.html',ld)

p=''
# --- Tiện ích
SV=[('🏊','Hồ bơi ngoài trời','Mở 6:00–21:00, có khăn tắm.'),('🥐','Nhà hàng & bữa sáng','Bữa sáng 6:30–9:30, thực đơn địa phương (minh họa).'),('💆','Spa & massage','Đặt lịch tại lễ tân (dịch vụ demo).'),('🚐','Đưa đón','Hỗ trợ đặt xe từ sân bay/bến xe (minh họa).'),('🚲','Xe đạp & xe máy','Mượn xe đạp; hỗ trợ thuê xe máy.'),('🧺','Giặt ủi','Dịch vụ giặt trong ngày.'),('📶','Wi‑Fi toàn khu','Miễn phí trong phòng và khu chung.'),('👶','Góc trẻ em','Sân chơi nhỏ, ghế ăn cho bé.'),('🅿️','Bãi đậu xe','Chỗ đậu xe trong khuôn viên.'),('🧳','Giữ hành lý','Miễn phí trước nhận và sau trả phòng.'),('🔥','Khu BBQ','Đặt trước để chuẩn bị bếp nướng.'),('🗺️','Tư vấn tour','Gợi ý lịch trình quanh vùng (demo).')]
pages['tien-ich.html']=('Tiện ích & dịch vụ','Tiện ích và dịch vụ tại Nhà Gió (demo): hồ bơi, bữa sáng, spa, đưa đón, xe đạp, giặt ủi, góc trẻ em.',head(p,'Tiện ích &amp; dịch vụ','Danh sách dịch vụ minh họa. Một số dịch vụ có thể tính phí – giá cụ thể sẽ được cập nhật khi có thông tin thật.',[('index.html','Trang chủ'),(None,'Tiện ích')])+f'''
<section class="sec" style="padding-top:24px"><div class="wrap"><ul class="grid g4" style="list-style:none;padding:0;margin:0">{''.join(f'<li class="feat"><div class="ico" aria-hidden="true">{i}</div><h2 style="font-size:var(--fs-md);margin-bottom:4px">{t}</h2><p>{d}</p></li>' for i,t,d in SV)}</ul></div></section>
<section class="sec alt"><div class="wrap split"><div class="map">{art('pool',6,'Khu hồ bơi',cls='r43')}</div><div><h2>Khung giờ chính</h2><ul class="ticks"><li>Lễ tân: 24/7</li><li>Bữa sáng: 6:30 – 9:30</li><li>Hồ bơi: 6:00 – 21:00</li><li>Yên lặng sau 22:00</li></ul><a class="btn primary" href="dat-phong.html">Đặt phòng</a></div></div></section>''','tien-ich.html')

# --- Thư viện ảnh
G=[]
for r in ROOMS:
    for k,c in GKINDS(r)[:3]:
        cat='ngoai' if k in('sea','hill','pool') else 'phong'
        G.append((cat,k,r['pal'],f"{r['name']} – {c}"))
G+= [('tien','pool',6,'Hồ bơi'),('tien','kitchen',2,'Bếp nhà hàng'),('tien','living',1,'Sảnh chờ'),('tien','bath',4,'Khu spa')]
gli=''.join(f'<li data-cat="{c}"><figure><button type="button" data-lb data-art="{k}" data-pal="{pl}" data-cap="{E(cap)} (ảnh minh họa)" aria-label="Phóng to: {E(cap)}">{art(k,pl,cap)}</button><figcaption>{E(cap)}</figcaption></figure></li>' for c,k,pl,cap in G)
pages['thu-vien-anh.html']=('Thư viện ảnh','Thư viện ảnh minh họa của Nhà Gió (demo): phòng nghỉ, cảnh quan, tiện ích. Tranh SVG tự vẽ.',head(p,'Thư viện ảnh','Tất cả hình là tranh minh họa SVG tự vẽ, không phải ảnh chụp thực tế. Bấm vào ảnh để xem lớn; dùng phím ← → để chuyển, Esc để đóng.',[('index.html','Trang chủ'),(None,'Thư viện ảnh')])+f'''
<section class="sec" style="padding-top:24px"><div class="wrap"><div class="filters" role="group" aria-label="Lọc ảnh"><button class="chip" data-filter="all" aria-pressed="true">Tất cả</button><button class="chip" data-filter="phong" aria-pressed="false">Phòng</button><button class="chip" data-filter="ngoai" aria-pressed="false">Cảnh quan</button><button class="chip" data-filter="tien" aria-pressed="false">Tiện ích</button></div>
<ul class="masonry">{gli}</ul></div></section>
<dialog class="lb" id="lb" aria-label="Xem ảnh lớn"><div class="lb-in"><div class="art"></div><p class="lb-cap"><span id="lbCap"></span><span id="lbNum"></span></p>
<button class="x" type="button" aria-label="Đóng">✕</button><button class="pv" type="button" aria-label="Ảnh trước">‹</button><button class="nx" type="button" aria-label="Ảnh sau">›</button></div></dialog>''','thu-vien-anh.html')

# --- Ưu đãi
pages['uu-dai.html']=('Ưu đãi','Các ưu đãi minh họa tại Nhà Gió (demo): ở dài ngày, đặt sớm, gói gia đình. Mã ưu đãi chỉ để trình diễn.',head(p,'Ưu đãi','Các ưu đãi dưới đây là nội dung minh họa, mã không có giá trị sử dụng.',[('index.html','Trang chủ'),(None,'Ưu đãi')])+f'''
<section class="sec" style="padding-top:24px"><div class="wrap"><ul class="grid" style="list-style:none;padding:0;margin:0;grid-template-columns:repeat(auto-fill,minmax(min(100%,460px),1fr))">{''.join(offer(*o,p) for o in OFFERS)}</ul>
<p class="note" style="margin-top:24px">Điều kiện chung (minh họa): không cộng dồn ưu đãi; áp dụng theo tình trạng phòng; nội dung sẽ được thay khi có chương trình thật.</p></div></section>''','uu-dai.html')

# --- Đặt phòng
pages['dat-phong.html']=('Đặt phòng','Đặt phòng Nhà Gió (demo): chọn ngày, số khách, xem tạm tính. Xác nhận chỉ lưu trong trình duyệt – không gửi đi đâu.',head(p,'Đặt phòng','Điền thông tin để tạo yêu cầu đặt phòng minh họa. Không thu tiền, không gửi dữ liệu – xác nhận chỉ lưu trong trình duyệt của bạn (localStorage).',[('index.html','Trang chủ'),(None,'Đặt phòng')])+'''
<section class="sec" style="padding-top:24px"><div class="wrap">
<div id="bkWrap" class="bk-grid"><form id="bookForm" class="panel" novalidate aria-describedby="formErr">
<fieldset><legend class="h">1. Phòng &amp; ngày</legend>
<div class="fg"><label for="room">Loại phòng</label><select id="room" name="room" required aria-describedby="room-err"></select><p class="err" id="room-err"></p></div>
<div class="row2"><div class="fg"><label for="ci">Nhận phòng</label><input id="ci" name="ci" type="date" required aria-describedby="ci-err"><p class="err" id="ci-err"></p></div>
<div class="fg"><label for="co">Trả phòng</label><input id="co" name="co" type="date" required aria-describedby="co-err"><p class="err" id="co-err"></p></div></div>
<div class="fg"><label for="g">Số khách</label><input id="g" name="g" type="number" min="1" max="8" inputmode="numeric" required aria-describedby="g-err"><p class="err" id="g-err"></p></div></fieldset>
<fieldset><legend class="h">2. Thông tin liên hệ</legend>
<div class="fg"><label for="name">Họ và tên</label><input id="name" name="name" autocomplete="name" required aria-describedby="name-err"><p class="err" id="name-err"></p></div>
<div class="row2"><div class="fg"><label for="phone">Số điện thoại</label><input id="phone" name="phone" type="tel" autocomplete="tel" placeholder="0900 000 000" required aria-describedby="phone-err"><p class="err" id="phone-err"></p></div>
<div class="fg"><label for="email">Email (không bắt buộc)</label><input id="email" name="email" type="email" autocomplete="email" aria-describedby="email-err"><p class="err" id="email-err"></p></div></div>
<div class="fg"><label for="note">Yêu cầu thêm (không bắt buộc)</label><textarea id="note" name="note"></textarea></div>
<label class="chk" for="agree"><input id="agree" name="agree" type="checkbox" aria-describedby="agree-err"><span>Tôi đã đọc <a href="chinh-sach.html">chính sách</a> và hiểu đây là bản demo</span></label><p class="err" id="agree-err"></p></fieldset>
<p class="err" id="formErr" role="alert"></p>
<button class="btn primary lg full" type="submit">Gửi yêu cầu đặt phòng (demo)</button></form>
<aside aria-labelledby="h-sum"><div class="panel"><h2 id="h-sum">Tạm tính</h2><div id="sum" aria-live="polite"></div><p class="sm muted">Tạm tính = giá/đêm × số đêm + phí dọn phòng + phí dịch vụ 5%. Tất cả là <b>giá minh họa</b>.</p></div></aside></div>
<div id="okBox" class="panel ok" hidden><div class="ico" aria-hidden="true">✓</div><h2 id="okTitle" tabindex="-1">Đã ghi nhận yêu cầu (demo)</h2><p>Mã tham chiếu: <span class="code" id="okCode"></span></p>
<dl class="calc" id="okInfo" style="max-width:420px;margin:16px auto;text-align:left"></dl><p class="note" style="max-width:520px;margin:0 auto 16px">Đây là bản demo: yêu cầu chỉ được lưu trong trình duyệt này, không có email/SMS nào được gửi và không có phòng nào được giữ thật.</p>
<button class="btn" id="again" type="button">Tạo yêu cầu khác</button> <a class="btn primary" href="index.html">Về trang chủ</a></div>
</div></section>''','dat-phong.html')

# --- Liên hệ
pages['lien-he.html']=('Vị trí & liên hệ','Vị trí minh họa và thông tin liên hệ mẫu của Nhà Gió (demo). Form liên hệ không gửi dữ liệu.',head(p,'Vị trí &amp; liên hệ','Địa chỉ, số điện thoại và bản đồ đều là minh họa.',[('index.html','Trang chủ'),(None,'Liên hệ')])+f'''
<section class="sec" style="padding-top:24px"><div class="wrap split" style="align-items:start">
<div><div class="map">{MAP}</div><h2 style="margin-top:24px">Thông tin</h2><ul class="ticks"><li>Địa chỉ minh họa, thành phố ven biển, Việt Nam</li><li>Điện thoại: 0900 000 000 (số mẫu)</li><li>Email: xinchao@vidu.test (mẫu)</li><li>Lễ tân: 24/7</li></ul></div>
<form id="contactForm" class="panel" novalidate><h2>Gửi lời nhắn</h2><p class="sm muted">Form demo: nội dung không được gửi đi đâu.</p>
<div class="fg"><label for="cname">Họ và tên</label><input id="cname" name="cname" autocomplete="name" aria-describedby="cname-err"><p class="err" id="cname-err"></p></div>
<div class="fg"><label for="cemail">Email</label><input id="cemail" name="cemail" type="email" autocomplete="email" aria-describedby="cemail-err"><p class="err" id="cemail-err"></p></div>
<div class="fg"><label for="ctopic">Chủ đề</label><select id="ctopic" name="ctopic"><option>Hỏi về phòng</option><option>Đặt tiệc / sự kiện</option><option>Góp ý</option></select></div>
<div class="fg"><label for="cmsg">Nội dung</label><textarea id="cmsg" name="cmsg" aria-describedby="cmsg-err"></textarea><p class="err" id="cmsg-err"></p></div>
<button class="btn primary full" type="submit">Gửi (demo)</button><p id="cfOk" class="note" tabindex="-1" hidden style="margin-top:12px">Đã ghi nhận trên trình duyệt (demo). Không có tin nhắn nào được gửi.</p></form>
</div></section>''','lien-he.html')

# --- Đánh giá
pages['danh-gia.html']=('Đánh giá mẫu','Đánh giá mẫu (demo) để minh họa bố cục – không phải đánh giá của khách thật.',head(p,'Đánh giá','Tất cả đánh giá trên trang là <b>nội dung mẫu (demo)</b>. Khi có khách thật, phần này sẽ lấy từ nguồn đánh giá đã xác minh.',[('index.html','Trang chủ'),(None,'Đánh giá')])+f'''
<section class="sec" style="padding-top:24px"><div class="wrap"><ul class="grid" style="list-style:none;padding:0;margin:0">{''.join(rv(*x) for x in REVIEWS)}</ul></div></section>''','danh-gia.html')

# --- FAQ
FAQ=[('Giờ nhận và trả phòng là mấy giờ?','Nhận phòng từ 14:00, trả phòng trước 12:00. Nhận sớm/trả muộn tùy tình trạng phòng (chính sách minh họa).'),('Giá trên web đã gồm những gì?','Giá trên web là giá minh họa mỗi đêm. Tạm tính cộng thêm phí dọn phòng và phí dịch vụ 5% (đều là số minh họa).'),('Tôi có bị trừ tiền khi đặt trên web không?','Không. Đây là bản demo, không có thanh toán và không có dữ liệu nào được gửi lên máy chủ.'),('Chính sách hủy phòng thế nào?','Hủy miễn phí trước 3 ngày; sau thời điểm đó tính 1 đêm (minh họa). Xem trang Chính sách.'),('Có cho mang thú cưng không?','Chỉ một số loại phòng (ví dụ Căn Đồi Thông) nhận thú cưng nhỏ, cần báo trước.'),('Trẻ em có tính thêm phí không?','Trẻ dưới 6 tuổi miễn phí khi dùng giường có sẵn; từ 6 tuổi có thể tính phụ thu (minh họa).'),('Có chỗ đậu xe không?','Có chỗ đậu xe trong khuôn viên cho một số loại phòng (mô tả minh họa).'),('Có xuất hóa đơn không?','Nội dung sẽ được cập nhật khi có thông tin doanh nghiệp thật.')]
faq=''.join(f'<div class="acc"><h3><button type="button" aria-expanded="false" aria-controls="faq{i}" id="faqb{i}">{q}</button></h3><div class="pn" id="faq{i}" role="region" aria-labelledby="faqb{i}" hidden><p>{a}</p></div></div>' for i,(q,a) in enumerate(FAQ))
faqld={"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in FAQ]}
pages['faq.html']=('Câu hỏi thường gặp','Câu hỏi thường gặp về nhận/trả phòng, giá, hủy phòng, trẻ em, thú cưng tại Nhà Gió (demo).',head(p,'Câu hỏi thường gặp','Câu trả lời mang tính minh họa cho bản demo.',[('index.html','Trang chủ'),(None,'FAQ')])+f'<section class="sec" style="padding-top:24px"><div class="wrap prose">{faq}<p style="margin-top:24px">Chưa thấy câu trả lời? <a href="lien-he.html">Liên hệ với chúng tôi</a>.</p></div></section>','faq.html',faqld)

# --- Chính sách
POL=[('huy','Hủy &amp; thay đổi đặt phòng',['Hủy miễn phí trước 3 ngày so với ngày nhận phòng.','Hủy trong vòng 3 ngày: tính phí 1 đêm.','Không đến (no-show): tính phí 1 đêm.','Đổi ngày miễn phí 1 lần nếu còn phòng.']),('nhan-tra','Nhận &amp; trả phòng',['Nhận phòng từ 14:00, trả phòng trước 12:00.','Xuất trình giấy tờ tùy thân khi nhận phòng theo quy định.','Trả phòng muộn đến 15:00 có thể phụ thu (minh họa).']),('tre-em','Trẻ em &amp; giường phụ',['Trẻ dưới 6 tuổi: miễn phí khi dùng giường có sẵn.','Từ 6 tuổi: có thể phụ thu, bao gồm bữa sáng (minh họa).','Nôi em bé: miễn phí, cần báo trước.']),('thu-cung','Thú cưng',['Chỉ nhận thú cưng nhỏ ở loại phòng có ghi "Cho thú cưng".','Không để thú cưng một mình trong phòng.','Có thể tính phí vệ sinh (minh họa).']),('rieng-tu','Quyền riêng tư',['Bản demo không thu thập và không gửi dữ liệu cá nhân lên máy chủ.','Thông tin bạn nhập vào form đặt phòng chỉ lưu trong trình duyệt (localStorage) để hiển thị màn hình xác nhận.','Có thể xóa bằng cách xóa dữ liệu trang web trong trình duyệt.','Không dùng cookie theo dõi, không có mã phân tích bên thứ ba.'])]
toc=''.join(f'<li><a href="#{i}">{t}</a></li>' for i,t,_ in POL)
pol=''.join(f'<h2 id="{i}">{t}</h2><ul>{"".join(f"<li>{x}</li>" for x in xs)}</ul>' for i,t,xs in POL)
pages['chinh-sach.html']=('Chính sách','Chính sách minh họa của Nhà Gió (demo): hủy phòng, nhận/trả phòng, trẻ em, thú cưng, quyền riêng tư.',head(p,'Chính sách','Nội dung chính sách mang tính minh họa, cần được thay bằng chính sách chính thức trước khi dùng thật.',[('index.html','Trang chủ'),(None,'Chính sách')])+f'<section class="sec" style="padding-top:24px"><div class="wrap prose"><nav class="toc" aria-label="Mục lục"><b>Mục lục</b><ul>{toc}</ul></nav>{pol}</div></section>','chinh-sach.html')

# --- 404
pages['404.html']=('Không tìm thấy trang','Trang không tồn tại.',f'<section class="sec center"><div class="wrap"><p class="big404" aria-hidden="true">404</p><h1>Không tìm thấy trang</h1><p class="muted">Đường dẫn có thể đã thay đổi. Hãy quay lại trang chủ hoặc xem các loại phòng.</p><a class="btn primary" href="index.html">Về trang chủ</a> <a class="btn" href="phong/index.html">Xem phòng</a></div></section>',None)

for path,v in pages.items():
    title,desc,body,cur=v[:4]; ld=v[4] if len(v)>4 else None
    fp=os.path.join(ROOT,path); os.makedirs(os.path.dirname(fp),exist_ok=True)
    open(fp,'w',encoding='utf-8').write(page(path,title,desc,body,cur,ld))
urls=''.join(f'<url><loc>{SITE}/{"" if k=="index.html" else k}</loc></url>' for k in pages if k!='404.html')
open(os.path.join(ROOT,'sitemap.xml'),'w').write(f'<?xml version="1.0" encoding="UTF-8"?>\n<!-- Bản demo: tên miền là placeholder -->\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>\n')
open(os.path.join(ROOT,'robots.txt'),'w').write(f'# Bản demo – chặn lập chỉ mục. Bỏ Disallow khi lên web thật.\nUser-agent: *\nDisallow: /\nSitemap: {SITE}/sitemap.xml\n')
print(len(pages),'pages')
