"""젠틀페이 로고 생성기 — 실제 서체(Google Fonts)를 harfbuzz로 조판 → 글자 외곽선을 SVG 패스로 변환.
출력: templates/_logos.html (스프라이트+CSS), templates/_lockup.html (macro), static/logos/logoN.svg (단독 파일)"""
import os, uharfbuzz as hb
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.boundsPen import BoundsPen

FD = os.path.join(os.path.dirname(__file__), 'fonts')  # Google Fonts TTF 8종을 여기에 받아서 실행
WIN = 'C:/Windows/Fonts'
OUT = 'C:/side_Prj/gentlepay_prj'
D, A = 'var(--mk-d)', 'var(--m2)'          # 진한색 / 강조색 (테마 따라 바뀜)
_fonts = {}

def font(path, var):
    key = (path, tuple(sorted(var.items())))
    if key not in _fonts:
        face = hb.Face(hb.Blob.from_file_path(path)); f = hb.Font(face)
        if var: f.set_variations(var)
        _fonts[key] = (f, face.upem)
    return _fonts[key]

class Logo:
    def __init__(s): s.items = []; s.box = [1e9, 1e9, -1e9, -1e9]
    def _grow(s, b):
        if b: s.box = [min(s.box[0], b[0]), min(s.box[1], b[1]), max(s.box[2], b[2]), max(s.box[3], b[3])]
    def text(s, path, var, txt, size, x, y, fill, track=0.0):
        """글자 패스 추가. track = em 단위 자간. 반환: 끝 x"""
        f, upem = font(path, var)
        buf = hb.Buffer(); buf.add_str(txt); buf.guess_segment_properties(); hb.shape(f, buf, {"kern": True, "liga": True})
        k = size / upem; pen = SVGPathPen(None); bp = BoundsPen(None); cx = 0
        for gi, gp in zip(buf.glyph_infos, buf.glyph_positions):
            for p in (pen, bp):
                f.draw_glyph_with_pen(gi.codepoint, TransformPen(p, (k, 0, 0, -k, x + (cx + gp.x_offset) * k, y - gp.y_offset * k)))
            cx += gp.x_advance + track * upem
        b = bp.bounds
        if b: s._grow((b[0], b[1], b[2], b[3]))
        s.items.append(f'<path d="{pen.getCommands()}" style="fill:{fill}"/>')
        return x + cx * k - track * size, b
    def raw(s, svg, bounds):
        s.items.append(svg); s._grow(bounds)
    def svg(s, pad=6):
        x0, y0, x1, y1 = s.box
        return f'{x0-pad:.0f} {y0-pad:.0f} {x1-x0+2*pad:.0f} {y1-y0+2*pad:.0f}', ''.join(s.items)

FR = f'{FD}/Fraunces.ttf'; OU = f'{FD}/Outfit.ttf'; SY = f'{FD}/Syne.ttf'; SG = f'{FD}/SpaceGrotesk.ttf'
DS = f'{FD}/DMSerifDisplay-Italic.ttf'; UN = f'{FD}/Unbounded.ttf'; BR = f'{FD}/BricolageGrotesque.ttf'
SO = f'{FD}/Sora.ttf'; NK = f'{WIN}/NotoSansKR-VF.ttf'

logos = {}
O = 'var(--mk-on)'   # 채운 면 위 색 (테마 배경색)

# 심볼 — 100x100 박스 좌표 (y 아래로). 글자 없이 도형만
M = {
  'hat':   f'<path d="M24 62V40A26 26 0 0 1 76 40V62Z" style="fill:{D}"/><rect x="6" y="62" width="88" height="13" rx="6.5" style="fill:{D}"/><rect x="24" y="49" width="52" height="10" style="fill:{A}"/>',
  'gp':    f'<circle cx="28" cy="38" r="20" fill="none" stroke-width="13" style="stroke:{D}"/><circle cx="72" cy="38" r="20" fill="none" stroke-width="13" style="stroke:{A}"/><rect x="43.5" y="38" width="13" height="56" rx="6.5" style="fill:{D}"/>',
  'cards': f'<rect x="30" y="10" width="64" height="44" rx="8" style="fill:{D}"/><rect x="6" y="40" width="64" height="46" rx="8" style="fill:{A}"/><rect x="6" y="52" width="64" height="9" style="fill:{O}" opacity=".9"/>',
  'swap':  f'<path d="M12 34H78M64 18L82 34L64 50" fill="none" stroke-width="12" stroke-linecap="round" stroke-linejoin="round" style="stroke:{A}"/><path d="M88 68H22M36 52L18 68L36 84" fill="none" stroke-width="12" stroke-linecap="round" stroke-linejoin="round" style="stroke:{D}"/>',
  'leaf':  f'<path d="M6 50A44 44 0 0 1 50 6H94V50A44 44 0 0 1 50 94A44 44 0 0 1 6 50Z" style="fill:{A}"/><circle cx="50" cy="50" r="15" style="fill:{O}"/>',
  'coins': f'<circle cx="34" cy="50" r="30" style="fill:{A}"/><circle cx="70" cy="50" r="24" fill="none" stroke-width="12" style="stroke:{D}"/>',
  'bars':  ''.join(f'<path d="M{8+i*28} 92L{26+i*28} {92-h}H{44+i*28}L{26+i*28} 92Z" style="fill:{A if i == 2 else D}"/>' for i, h in enumerate((40, 62, 86))),
  'gem':   f'<path d="M50 4L93 47H7Z" style="fill:{D}"/><path d="M7 53H93L50 96Z" style="fill:{A}"/>',
  'wave':  f'<path d="M4 50A46 46 0 0 1 96 50C80 38 66 38 50 50S20 62 4 50Z" style="fill:{D}"/><path d="M4 50C20 62 34 62 50 50S80 38 96 50A46 46 0 0 1 4 50Z" style="fill:{A}"/>',
  'pin':   f'<path d="M48 48H4A44 44 0 0 1 48 4Z" style="fill:{D}"/><path d="M52 48V4A44 44 0 0 1 96 48Z" style="fill:{A}"/><path d="M52 52H96A44 44 0 0 1 52 96Z" style="fill:{D}"/><path d="M48 52V96A44 44 0 0 1 4 52Z" style="fill:{D}"/>',
  'check': f'<circle cx="50" cy="50" r="46" style="fill:{A}"/><path d="M28 52L43 67L73 35" fill="none" stroke-width="11" stroke-linecap="round" stroke-linejoin="round" style="stroke:{O}"/>',
}
def mark(L, key, x=0, top=-72, size=84):
    k = size / 100
    L.raw(f'<g transform="translate({x} {top}) scale({k})">{M[key]}</g>', (x, top, x + size, top + size))
    return x + size

def en(n, name, key, path, var, a, b, size=96, gap=28, track=-0.02, sep=0, top=-84, msize=104):
    L = Logo(); x = mark(L, key, 0, top, msize) + gap
    x, _ = L.text(path, var, a, size, x, 0, D, track)
    L.text(path, var, b, size, x + sep, 0, A, track)
    logos[n] = (name, L)

en(1, '중절모 · 소프트 세리프', 'hat', FR, {'wght': 720, 'SOFT': 100, 'WONK': 0, 'opsz': 72}, 'gentle', 'pay', sep=3, top=-98, msize=118)
en(2, 'gp 모노그램 · 기하 산세리프', 'gp', OU, {'wght': 600}, 'gentle', 'pay', top=-80, msize=104)
en(3, '상품권 카드 · 그로테스크', 'cards', SG, {'wght': 700}, 'Gentle', 'Pay', size=90, track=-0.03, sep=20, top=-84)
en(4, '교환 화살표 · Sora', 'swap', SO, {'wght': 700}, 'gentle', 'pay', size=88, track=-0.04)
en(5, '잎사귀 코인 · 브리콜라주', 'leaf', BR, {'wght': 700, 'wdth': 100, 'opsz': 96}, 'gentle', 'pay', track=-0.03)
en(6, '겹친 동전 · 와이드 캡스', 'coins', SY, {'wght': 800}, 'GENTLE', 'PAY', size=78, track=0.01, sep=18, top=-74, msize=86)
en(7, '상승 막대 · 언바운디드', 'bars', UN, {'wght': 700}, 'gentle', 'pay', size=78, track=-0.03, top=-78, msize=96)
en(8, '다이아 · 이탤릭 세리프', 'gem', DS, {}, 'Gentle', 'Pay', size=100, sep=20, top=-88, msize=106)
en(9, '물결 원 · 기하 산세리프', 'wave', OU, {'wght': 500}, 'gentle', 'pay', track=-0.02, sep=2)
en(10, '바람개비 · 그로테스크', 'pin', SG, {'wght': 500}, 'gentle', 'pay', size=92, track=-0.03, sep=14)

# 11. 체크 원 + 한글
L = Logo(); x = mark(L, 'check', 0, -88, 100) + 22
x, _ = L.text(NK, {'wght': 900}, '젠틀', 96, x, 0, D, -0.06)
L.text(NK, {'wght': 900}, '페이', 96, x + 2, 0, A, -0.06)
logos[11] = ('체크 원 · 한글', L)

# 12. gp 모노그램 + 한글/영문 2단
L = Logo(); x = mark(L, 'gp', 0, -72, 116) + 22
x2, _ = L.text(NK, {'wght': 900}, '젠틀', 66, x, 0, D, -0.05)
L.text(NK, {'wght': 900}, '페이', 66, x2 + 2, 0, A, -0.05)
L.text(SO, {'wght': 600}, 'GENTLE PAY', 21, x + 3, 32, D, 0.36)
logos[12] = ('gp 모노그램 · 한글 2단', L)

# ── 출력 ──
sprite, vbs = [], {}
for n, (name, L) in logos.items():
    vb, body = L.svg()
    vbs[n] = vb
    sprite.append(f'    <!-- {n}. {name} -->\n    <symbol id="gl{n}" viewBox="{vb}">{body}</symbol>')
    for theme, (d, a) in {'': ('#0B2470', '#1A5CE6')}.items():
        os.makedirs(f'{OUT}/static/logos', exist_ok=True)
        open(f'{OUT}/static/logos/logo{n}.svg', 'w', encoding='utf-8').write(
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}">{body.replace(D, d).replace(A, a).replace(O, "#fff")}</svg>')

css = '\n'.join(f'[data-l="{n}"] .lg{n}' for n in logos)
open(f'{OUT}/templates/_logos.html', 'w', encoding='utf-8', newline='\n').write(f'''{{# 젠틀페이 로고 시안 12종 — scratchpad/mklogos.py 로 생성 (실제 서체 외곽선 패스). 직접 수정 X
   색: --mk-d 진한색 / --m2 강조색 (디자인 테마 따라 바뀜) #}}
<style>
:root{{--mk-d:#0B2470;--mk-on:#fff}}
:root[data-d="B"]{{--mk-d:#fff;--mk-on:#0B1C4D}}
:root[data-d="C"]{{--mk-d:#0F3D33}}
.lg{{display:none;width:auto;max-width:100%}}
{css.replace(chr(10), ',')}{{display:block}}
[data-l="11"] .hide8,[data-l="12"] .hide8{{display:none!important}}
</style>
<svg style="position:absolute;width:0;height:0;overflow:hidden" aria-hidden="true" xmlns="http://www.w3.org/2000/svg">
{chr(10).join(sprite)}
</svg>
''')
open(f'{OUT}/templates/_lockup.html', 'w', encoding='utf-8', newline='\n').write(
    '{# 로고 락업 매크로 — 12종 모두 출력, 현재 data-l 에 해당하는 것만 보임 #}\n{% macro lockup(cls="") %}' +
    ''.join(f'<svg class="lg lg{n} {{{{ cls }}}}" viewBox="0 0 {' '.join(vb.split()[2:])}" aria-hidden="true"><use href="#gl{n}"/></svg>' for n, vb in vbs.items()) +
    '{% endmacro %}\n')
for n, vb in vbs.items(): print(n, logos[n][0], vb)
