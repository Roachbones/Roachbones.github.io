
print("""<!doctype html>
<html lang=en>
<head>
<meta charset=utf-8>
<meta name=viewport content="width=device-width, initial-scale=1.0">
<meta property=og:image content=https://rose.systems/88x31/i/rose.systems-scribble.png>
<meta property=og:description content="88x31 button walls">
<title>button walls</title>
<link rel=stylesheet type=text/css href=../style.css>
<link rel=stylesheet type=text/css href=style.css>

<main>

<div title=0x11xxx111111✪>
    <input type=checkbox id=b>
    <input type=checkbox id=c>
    <input type=checkbox id=d>
    <input type=checkbox id=e>
    <input type=checkbox id=f>
    <input type=checkbox id=g>
    <input type=checkbox id=h>
    <input type=checkbox id=i>
    <input type=checkbox id=x>
    <input type=checkbox id=j>
    <input type=checkbox id=k>
    <input type=checkbox id=l>
    <input type=checkbox id=m>
    <input type=checkbox id=z>
</div>

<img width=354 id=thanks src=thanks.png alt="Thanks for visiting :)" data-comment="from https://sweetfish.site/advent/2025">
<p>You can add my 88x31 to your site: <a href=https://rose.systems><img src=i/rose.systems-scribble.png alt=rose.systems></a></p>
""")

import json

with open('i/meta.json') as f:
    metadata=json.load(f)


imgs = []

for metadatum in metadata:
    img = '<img width=88 height=31 src="i/' + metadatum['src'] + '"'
    for attr in ['alt','title','onclick','lang','data-comment']:
        if attr in metadatum:
            img = img + ' ' + attr + '="' + metadatum[attr] + '"'
    img = img + '>'
    if 'href' in metadatum:
        href = metadatum['href']
        if not href.startswith('http'): href = 'https://'+href
        img = '<a href="'+href+'">'+img+'</a>'
    imgs.append(img)
    img = img + '\n'

walls = [[],[],[],[]]
loops = []

BLANK = '<img width=88 height=31 src=i/blank.gif>'

w = 4
h = 6
perimeter = w * 4

for _ in range(h):
    loop = imgs[:perimeter]
    imgs = imgs[perimeter:]
    while len(loop) < perimeter: loop.append(BLANK)
    walls[0].insert(0,loop[0:w+1])
    walls[1].insert(0,loop[w:2*w+1])
    walls[2].insert(0,loop[2*w:3*w+1])
    walls[3].insert(0,loop[3*w:] + [loop[0]])

print('<brick-house>')
for wall in walls:
    print(' <brick-wall>')
    for course in wall:
        print('  <brick-course>')
        for brick in course:
            print('   '+brick)
        print('  </brick-course>')
    print(' </brick-wall>')
print('</brick-house>')

print('\n</main>')
