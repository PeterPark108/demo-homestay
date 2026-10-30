#!/usr/bin/env python3
"""Tương phản WCAG 2.x cho các cặp màu chữ/nền dùng trong assets/site.css."""
def L(h):
    h=h.lstrip('#');c=[int(h[i:i+2],16)/255 for i in(0,2,4)];c=[x/12.92 if x<=.03928 else((x+.055)/1.055)**2.4 for x in c];return .2126*c[0]+.7152*c[1]+.0722*c[2]
def cr(a,b):x,y=sorted([L(a),L(b)],reverse=True);return(x+.05)/(y+.05)
P=[('chữ/nền','#2b2622','#fffaf5'),('muted/nền','#6f645b','#fffaf5'),('muted/trắng','#6f645b','#ffffff'),('muted/cát','#6f645b','#fbeee2'),('nút chính','#ffffff','#b5472c'),('nút hover','#ffffff','#9a3a22'),('link/nền','#b5472c','#fffaf5'),('link/cát','#b5472c','#fbeee2'),('eyebrow/trắng','#b5472c','#ffffff'),('demo bar','#ffffff','#1f5f63'),('toast','#ffffff','#1f5f63'),('footer phụ','#c9bcb0','#2b2622'),('footer nhấn','#ffd8a8','#2b2622'),('demo-tag','#7a5200','#fff1c2'),('lỗi/ô lỗi','#b42318','#fff5f5'),('nav active','#ffffff','#2b2622'),('tag ảnh (~nền tối)','#ffffff','#2b2622'),('icon OK','#ffffff','#1f7a6e'),('note','#2b2622','#fff4e5'),('viền input/trắng (≥3)','#a38b76','#ffffff')]
bad=0
for n,a,b in P:
    r=cr(a,b);need=3 if '≥3' in n else 4.5;ok=r>=need;bad+=not ok;print(f'{"OK " if ok else "BAD"} {r:5.2f}  {n} {a} / {b}')
raise SystemExit(bad)
