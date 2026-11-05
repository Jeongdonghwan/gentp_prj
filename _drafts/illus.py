"""한도 카드 3D풍 일러스트 3종 (SVG, 그라데이션+그림자로 입체감) → static/img/lim-*.svg"""
OUT = 'C:/side_Prj/gentlepay_prj/static/img'

DEFS = '''<defs>
<radialGradient id="cg" cx=".35" cy=".3" r=".8"><stop offset="0" stop-color="#FFE7A3"/><stop offset=".55" stop-color="#FFC24D"/><stop offset="1" stop-color="#E8962B"/></radialGradient>
<linearGradient id="pk" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#FFB3BE"/><stop offset="1" stop-color="#F2667F"/></linearGradient>
<linearGradient id="bl" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#8CBBFF"/><stop offset="1" stop-color="#3A6CF2"/></linearGradient>
<linearGradient id="pu" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#F3F0FF"/><stop offset="1" stop-color="#D9D1FF"/></linearGradient>
<linearGradient id="pu2" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#A38BFF"/><stop offset="1" stop-color="#6E4EE8"/></linearGradient>
<linearGradient id="or" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#FFC99B"/><stop offset=".5" stop-color="#FFB27A"/><stop offset="1" stop-color="#EE8D4E"/></linearGradient>
<linearGradient id="rd" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#FF7A7A"/><stop offset="1" stop-color="#E5323D"/></linearGradient>
<linearGradient id="cr" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#FF9E86"/><stop offset="1" stop-color="#E35B47"/></linearGradient>
<linearGradient id="yl" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#FFE48A"/><stop offset="1" stop-color="#F5B83D"/></linearGradient>
<linearGradient id="gr" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#B6F0C8"/><stop offset="1" stop-color="#4CC97A"/></linearGradient>
<filter id="sh" x="-20%" y="-20%" width="140%" height="150%"><feDropShadow dx="0" dy="5" stdDeviation="4" flood-color="#1B2A55" flood-opacity=".16"/></filter>
</defs>'''

def coin(x, y, r, rot=0):
    """정면 동전 — 두께(뒤 원) + 앞면 그라데이션 + 테두리 + ₩"""
    return (f'<g transform="translate({x} {y}) rotate({rot})" filter="url(#sh)">'
            f'<circle cx="2" cy="3" r="{r}" fill="#D38424"/><circle r="{r}" fill="url(#cg)"/>'
            f'<circle r="{r*.72:.1f}" fill="none" stroke="#E29A32" stroke-width="{r*.1:.1f}"/>'
            f'<text y="{r*.36:.1f}" text-anchor="middle" font-family="Arial Black,Arial" font-weight="900" font-size="{r*.95:.1f}" fill="#D9822B">₩</text></g>')

def svg(name, body):
    open(f'{OUT}/lim-{name}.svg', 'w', encoding='utf-8').write(
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 150">{DEFS}{body}</svg>')

# 1. 소액결제 — 계산기 + 카드 + 동전
svg('micro', ''.join([
    '<g transform="rotate(-10 92 92)" filter="url(#sh)">',
    '<rect x="50" y="46" width="90" height="92" rx="18" fill="#E0566F"/>',
    '<rect x="46" y="40" width="90" height="92" rx="18" fill="url(#pk)"/>',
    '<rect x="58" y="52" width="66" height="20" rx="7" fill="#FFE1E6"/>',
    *[f'<rect x="{58+i*24}" y="{80+j*24}" width="18" height="18" rx="6" fill="#FFF3F5"/>' for i in range(2) for j in range(2)],
    '<path d="M64 89h6M67 86v6M88 89h6M91 86v6M64 110l6 6M70 110l-6 6M88 113h6" stroke="#F2667F" stroke-width="2.4" stroke-linecap="round"/>',
    '<rect x="106" y="80" width="18" height="42" rx="6" fill="#FFD36B"/>',
    '</g>',
    '<g transform="rotate(-8 140 46)" filter="url(#sh)"><rect x="104" y="22" width="76" height="48" rx="9" fill="url(#bl)"/>',
    '<rect x="114" y="34" width="26" height="4" rx="2" fill="#fff" opacity=".85"/><rect x="114" y="42" width="38" height="4" rx="2" fill="#fff" opacity=".6"/>',
    '<rect x="114" y="54" width="20" height="4" rx="2" fill="#A9D2FF"/><circle cx="164" cy="50" r="9" fill="#fff"/>',
    '<path d="M159.5 50.5l3 3 6-6.5" fill="none" stroke="#3A6CF2" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/></g>',
    coin(46, 30, 13, -15), coin(170, 102, 13, 12), coin(34, 122, 14, 8),
]))

# 2. 정보이용료 — 휴대폰 받침 + 동전 탑 + 지그재그 화살표
stacks = ''
for i, n in enumerate((6, 5, 4, 2)):
    x = 70 + i * 26
    for k in range(n):
        y = 112 - k * 7
        stacks += f'<ellipse cx="{x}" cy="{y+3}" rx="12" ry="5" fill="#E07F3E"/><ellipse cx="{x}" cy="{y}" rx="12" ry="5" fill="url(#or)"/>'
svg('info', ''.join([
    '<g filter="url(#sh)"><path d="M30 118L60 100H190L160 118Z" fill="url(#pu)"/>',
    '<path d="M30 118H160V126H30Z" fill="url(#pu2)"/><path d="M160 118L190 100V108L160 126Z" fill="#5A3BD6"/>',
    '<rect x="90" y="120" width="22" height="2.6" rx="1.3" fill="#fff" opacity=".7"/></g>',
    f'<g filter="url(#sh)">{stacks}</g>',
    '<path d="M162 100L148 74L136 88L122 52L106 68L90 26L80 40" fill="none" stroke="#C7262F" stroke-width="7" stroke-linejoin="round" transform="translate(1.5 2)"/>',
    '<path d="M162 100L148 74L136 88L122 52L106 68L90 26L80 40" fill="none" stroke="url(#rd)" stroke-width="7" stroke-linejoin="round"/>',
    '<path d="M68 12L94 14L80 40Z" fill="url(#rd)"/>',
    '<g transform="rotate(-25 150 22)"><ellipse cx="150" cy="24" rx="11" ry="5" fill="#E07F3E"/><ellipse cx="150" cy="22" rx="11" ry="5" fill="url(#or)"/></g>',
    '<g transform="rotate(20 174 62)"><ellipse cx="174" cy="64" rx="10" ry="4.5" fill="#E07F3E"/><ellipse cx="174" cy="62" rx="10" ry="4.5" fill="url(#or)"/></g>',
]))

# 3. 신용카드 — 지갑 + 카드 + 지폐 + 동전
svg('card', ''.join([
    '<g filter="url(#sh)"><rect x="66" y="16" width="78" height="50" rx="8" fill="#8C6CF5" transform="rotate(-14 105 41)"/>',
    '<rect x="96" y="22" width="70" height="46" rx="8" fill="url(#yl)" transform="rotate(10 131 45)"/>',
    '<rect x="104" y="36" width="40" height="7" rx="3" fill="#E8A42E" transform="rotate(10 131 45)"/></g>',
    '<g filter="url(#sh)"><rect x="50" y="48" width="112" height="84" rx="20" fill="#CF4C3A"/>',
    '<rect x="46" y="44" width="112" height="84" rx="20" fill="url(#cr)"/>',
    '<path d="M118 66H164A10 10 0 0 1 174 76V94A10 10 0 0 1 164 104H118A6 6 0 0 1 112 98V72A6 6 0 0 1 118 66Z" fill="#F07A62"/>',
    '<circle cx="128" cy="85" r="7" fill="#FFF4EE"/><circle cx="128" cy="85" r="3.5" fill="#E9B4A6"/></g>',
    '<g transform="rotate(-12 172 112)" filter="url(#sh)"><rect x="152" y="98" width="44" height="26" rx="4" fill="url(#gr)"/>',
    '<circle cx="174" cy="111" r="7" fill="#fff" opacity=".7"/><rect x="157" y="103" width="6" height="16" rx="2" fill="#fff" opacity=".45"/></g>',
    coin(44, 54, 13, -10), coin(150, 132, 12, 15),
]))
print('ok')
