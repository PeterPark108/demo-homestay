#!/usr/bin/env python3
"""Kiểm tra mọi liên kết nội bộ (href/src) trong các file .html đều trỏ tới file tồn tại, và id #anchor tồn tại."""
import os,re,sys,html.parser,urllib.parse
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
class P(html.parser.HTMLParser):
    def __init__(s):super().__init__();s.links=[];s.ids=set();s.imgs_noalt=0;s.svg_noname=0
    def handle_starttag(s,t,a):
        a=dict(a)
        if 'id' in a:s.ids.add(a['id'])
        for k in('href','src'):
            if k in a and a[k]:s.links.append(a[k])
        if t=='img' and 'alt' not in a:s.imgs_noalt+=1
bad=[];n=0;files=[]
for d,_,fs in os.walk(ROOT):
    if '.git' in d or 'screenshots' in d or 'node_modules' in d:continue
    files+= [os.path.join(d,f) for f in fs if f.endswith('.html')]
cache={}
def parse(f):
    if f not in cache:p=P();p.feed(open(f,encoding='utf-8').read());cache[f]=p
    return cache[f]
for f in files:
    p=parse(f)
    for l in p.links:
        if re.match(r'^(https?:|mailto:|tel:|data:|javascript:)',l):continue
        n+=1;u=urllib.parse.urlparse(l);path=urllib.parse.unquote(u.path)
        tgt=os.path.normpath(os.path.join(os.path.dirname(f),path)) if path else f
        if os.path.isdir(tgt):tgt=os.path.join(tgt,'index.html')
        if not os.path.exists(tgt):bad.append((os.path.relpath(f,ROOT),l,'missing file'));continue
        if u.fragment and not u.fragment.startswith('/') and tgt.endswith('.html') and u.fragment not in parse(tgt).ids:bad.append((os.path.relpath(f,ROOT),l,'missing #id'))
    if p.imgs_noalt:bad.append((os.path.relpath(f,ROOT),'<img>','no alt'))
print(f'{len(files)} files, {n} internal links checked, {len(bad)} problems')
for b in bad:print(' ',*b)
sys.exit(1 if bad else 0)
