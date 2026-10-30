#!/usr/bin/env python3
"""Chụp luồng demo trên mobile 390: trang chủ → loại phòng → chi tiết phòng → đặt phòng → xác nhận → menu. Chạy: python3 tools/flow.py [thư-mục-gốc] [đường-dẫn-con]"""
import os,sys,threading,http.server,functools
from playwright.sync_api import sync_playwright
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)));OUT=None if os.environ.get('NOSHOT') else os.path.join(ROOT,'screenshots','hotel-v2')
SERVE=sys.argv[1] if len(sys.argv)>1 else ROOT; SUB=sys.argv[2] if len(sys.argv)>2 else ''
class Q(http.server.SimpleHTTPRequestHandler):
    def log_message(s,*a):pass
srv=http.server.ThreadingHTTPServer(('127.0.0.1',8766),functools.partial(Q,directory=SERVE));threading.Thread(target=srv.serve_forever,daemon=True).start()
B=f'http://127.0.0.1:8766/{SUB}'
LOAD="async()=>{document.querySelectorAll('img[loading=lazy]').forEach(i=>i.loading='eager');await Promise.all([...document.images].map(i=>i.complete?0:new Promise(r=>{i.onload=i.onerror=r})));return [...document.images].filter(i=>!i.naturalWidth).length}"
errs=[];shots=[]
def shot(pg,n,full=True):
    b=pg.evaluate(LOAD)
    if b:errs.append(f'{n}: {b} broken images')
    if pg.evaluate('document.documentElement.scrollWidth')>390:errs.append(f'{n}: overflow')
    if OUT:pg.evaluate('window.scrollTo(0,0)');pg.wait_for_timeout(150);f=f'{OUT}/{n}.png';pg.screenshot(path=f,full_page=full);shots.append(f)
with sync_playwright() as p:
    br=p.chromium.launch();ctx=br.new_context(viewport={'width':390,'height':844},device_scale_factor=2,locale='vi-VN',is_mobile=True,has_touch=True)
    pg=ctx.new_page();pg.on('console',lambda m:m.type=='error' and errs.append('console: '+m.text));pg.on('pageerror',lambda e:errs.append(f'pageerror: {e}'))
    pg.goto(B+'index.html');pg.wait_for_load_state('networkidle');shot(pg,'flow-01-home',False)
    pg.click('#menuBtn');pg.click('#nav a[href$="phong/index.html"]');pg.wait_for_load_state('networkidle');shot(pg,'flow-02-loai-phong',False)
    pg.click('#roomList a[href$="villa-ho-boi-eo-gio.html"]');pg.wait_for_load_state('networkidle');shot(pg,'flow-03-chi-tiet-phong',False)
    pg.click('#cn')
    pair=pg.evaluate("()=>{const b=[...document.querySelectorAll('#cal .d[data-d]')];for(let i=0;i<b.length-3;i++)if(!b[i].disabled&&!b[i+1].disabled&&!b[i+2].disabled&&!b[i+3].disabled)return [b[i].dataset.d,b[i+3].dataset.d]}")
    pg.click(f'#cal [data-d="{pair[0]}"]');pg.click(f'#cal [data-d="{pair[1]}"]');pg.click('#bb-go');pg.wait_for_load_state('networkidle')
    pg.fill('#name','Khách Demo');pg.fill('#phone','0900000000');pg.check('#agree');shot(pg,'flow-04-dat-phong',False)
    pg.click('#bookForm button[type=submit]');pg.wait_for_timeout(300)
    if not pg.is_visible('#okBox'):errs.append('confirmation not shown: '+pg.inner_text('#formErr'))
    shot(pg,'flow-05-xac-nhan',False)
    pg.goto(B+'index.html');pg.click('#menuBtn');pg.wait_for_timeout(200);shot(pg,'flow-06-menu',False)
    br.close()
srv.shutdown();print('ISSUES:',len(errs));[print(' ',e) for e in errs];print('\n'.join(shots))
