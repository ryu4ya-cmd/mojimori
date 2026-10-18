"""文字のフォント（Klee One・Zen Maru Gothic）を、ゲームで使う字だけにしぼって fonts/ に作り直す。

Google Fonts から読みこむと、遊んだ人の接続情報が Google に送られるので、
フォントはこのリポジトリに入れて、同じサイトから配る。そのままだと重いので、
src/game.html と voice/index.json に出てくる字と、ひらがな・カタカナ・英数字・記号の
ぜんぶだけを残して woff2 にする。ゲームに新しい漢字などを足したら実行する。
使い方: pip install fonttools brotli → python3 tools/make_text_fonts.py [元の ttf があるフォルダ]
（フォルダを省くと、google/fonts リポジトリから元の ttf を取ってくる。ライセンスは fonts/OFL.txt）
"""
import subprocess
import sys
import tempfile
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FONTS_URL = 'https://raw.githubusercontent.com/google/fonts/main/ofl/'
# 元の ttf → 作る woff2
FONTS = {
    'kleeone/KleeOne-SemiBold.ttf': 'klee-one-600.woff2',
    'zenmarugothic/ZenMaruGothic-Bold.ttf': 'zen-maru-gothic-700.woff2',
    'zenmarugothic/ZenMaruGothic-Black.ttf': 'zen-maru-gothic-900.woff2',
}

text = (ROOT / 'src' / 'game.html').read_text(encoding='utf-8')
text += (ROOT / 'voice' / 'index.json').read_text(encoding='utf-8')
chars = {c for c in text if ord(c) >= 0x20}
# 英数字・記号、和文の記号、ひらがな・カタカナ（濁音・小書き・長音を含む）、全角の英数字は必ず入れる
for lo, hi in [(0x20, 0x7E), (0xA0, 0xFF), (0x2010, 0x2027), (0x3000, 0x30FF), (0x31F0, 0x31FF), (0xFF01, 0xFF9F)]:
    chars.update(chr(c) for c in range(lo, hi + 1))
unicodes = ','.join(f'U+{ord(c):04X}' for c in sorted(chars))

src_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(tempfile.mkdtemp())
for name, out_name in FONTS.items():
    src = src_dir / Path(name).name
    if not src.exists():
        print(f'{FONTS_URL}{name} を取ってきます')
        urllib.request.urlretrieve(FONTS_URL + name, src)
    out = ROOT / 'fonts' / out_name
    subprocess.run(['pyftsubset', str(src), f'--unicodes={unicodes}', '--layout-features+=tnum',
                    '--flavor=woff2', f'--output-file={out}'], check=True)
    print(f'{out.relative_to(ROOT)} を作りました（{out.stat().st_size // 1024} KB）')
