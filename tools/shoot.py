#!/usr/bin/env python3
"""Chụp full-page desktop (1440) + mobile (390), ghi lỗi console, kiểm tra tương tác chính. Chạy: python3 tools/shoot.py"""
import os,sys,threading,http.server,functools,json
from playwright.sync_api import sync_playwright
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)));OUT=os.path.join(ROOT,'screenshots','hotel-v2');os.makedirs(OUT,exist_ok=True)
class Q(http.server.SimpleHTTPRequestHandler):
    def log_message(s,*a):pass
H=functools.partial(Q,directory=ROOT)
srv=http.server.ThreadingHTTPServer(('127.0.0.1',8765),H);threading.Thread(target=srv.serve_forever,daemon=True).start()
B='http://127.0.0.1:8765/'
PAGES=[('trang-chu','index.html'),('loai-phong','phong/index.html'),('chi-tiet-phong','phong/villa-ho-boi-eo-gio.html'),('tien-ich','tien-ich.html'),('thu-vien-anh','thu-vien-anh.html'),('uu-dai','uu-dai.html'),('dat-phong','dat-phong.html?room=r1'),('lien-he','lien-he.html'),('danh-gia','danh-gia.html'),('faq','faq.html'),('chinh-sach','chinh-sach.html'),('nguon-anh','nguon-anh.html'),('404','404.html'),('homestay-v1','homestay-v1/index.html')]
errs=[]
LOADIMG='''async()=>{document.querySelectorAll('img[loading=lazy]').forEach(i=>i.loading='eager');await Promise.all([...document.images].map(i=>i.complete?0:new Promise(r=>{i.onload=i.onerror=r})));return [...document.images].filter(i=>!i.naturalWidth).map(i=>i.getAttribute('src'))}'''
with sync_playwright() as p:
    br=p.chromium.launch()
    for dev,w,h in(('desktop',1440,900),('mobile',390,844),('narrow',360,780)):
        ctx=br.new_context(viewport={'width':w,'height':h},device_scale_factor=1,locale='vi-VN')
        for name,url in PAGES:
            pg=ctx.new_page();pg.on('console',lambda m,n=name:m.type=='error' and errs.append(f'{dev}/{n}: {m.text}'));pg.on('pageerror',lambda e,n=name:errs.append(f'{dev}/{n}: {e}'))
            pg.goto(B+url);pg.wait_for_load_state('networkidle')
            sw=pg.evaluate('document.documentElement.scrollWidth')
            if sw>w:errs.append(f'{dev}/{name}: horizontal overflow {sw}px')
            if name=='chi-tiet-phong':
                pg.click('#cn')
                pair=pg.evaluate("()=>{const b=[...document.querySelectorAll('#cal .d[data-d]')];for(let i=0;i<b.length-3;i++)if(!b[i].disabled&&!b[i+1].disabled&&!b[i+2].disabled&&!b[i+3].disabled)return [b[i].dataset.d,b[i+3].dataset.d]}")
                pg.click(f'#cal [data-d="{pair[0]}"]');pg.click(f'#cal [data-d="{pair[1]}"]')
                if 'Tạm tính' not in pg.inner_text('#bb-calc'):errs.append(f'{dev}: estimate not shown')
            if name=='faq':pg.click('#faqb0')
            broken=pg.evaluate(LOADIMG)
            if broken:errs.append(f'{dev}/{name}: broken images {broken}')
            pg.evaluate('window.scrollTo(0,document.body.scrollHeight)');pg.wait_for_timeout(600);pg.evaluate('window.scrollTo(0,0)');pg.wait_for_timeout(600);pg.screenshot(path=f'{OUT}/{dev}-{name}.png',full_page=True);pg.close()
        # tương tác
        pg=ctx.new_page();pg.on('pageerror',lambda e:errs.append(f'{dev}/booking: {e}'))
        pg.goto(B+'dat-phong.html');pg.click('#bookForm button[type=submit]')
        if pg.locator('[aria-invalid=true]').count()<3:errs.append(f'{dev}: validation not triggered')
        pg.evaluate('window.scrollTo(0,0)');pg.wait_for_timeout(100);pg.screenshot(path=f'{OUT}/{dev}-dat-phong-loi.png',full_page=True)
        js=pg.evaluate("""()=>{const t=new Date();const f=n=>{const d=new Date(t);d.setDate(d.getDate()+n);return d.toISOString().slice(0,10)};return [f(60),f(62)]}""")
        pg.select_option('#room','r4');pg.fill('#ci',js[0]);pg.fill('#co',js[1]);pg.fill('#g','2');pg.fill('#name','Khách Demo');pg.fill('#phone','0900000000');pg.check('#agree');pg.click('#bookForm button[type=submit]')
        if not pg.is_visible('#okBox'):errs.append(f'{dev}: confirmation not shown: '+pg.inner_text('#formErr'))
        else:pg.evaluate('window.scrollTo(0,0)');pg.wait_for_timeout(100);pg.screenshot(path=f'{OUT}/{dev}-xac-nhan.png',full_page=True)
        if dev=='mobile':
            pg.goto(B+'index.html');pg.click('#menuBtn');pg.screenshot(path=f'{OUT}/mobile-menu.png')
            if not pg.is_visible('#nav'):errs.append('mobile menu not opening')
        pg.goto(B+'thu-vien-anh.html');pg.click('[data-lb] >> nth=0');pg.keyboard.press('ArrowRight');pg.wait_for_timeout(800);pg.screenshot(path=f'{OUT}/{dev}-lightbox.png')
        pg.keyboard.press('Escape')
        if pg.evaluate('document.getElementById("lb").open'):errs.append(f'{dev}: lightbox esc')
        ctx.close()
    br.close()
srv.shutdown()
print('ISSUES:',len(errs));[print(' ',e) for e in errs]
