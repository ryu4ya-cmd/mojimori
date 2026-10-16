"""src/game.html から、GitHub Pages で配る index.html を作る。

src/game.html は claude.ai のアーティファクトと同じ「中身だけ」の形式なので、
ここで <head>（アイコン・ホーム画面用の設定）を足して、ふつうのページにする。
使い方: python3 tools/build.py
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
src = (ROOT / "src" / "game.html").read_text(encoding="utf-8")
src = "\n".join(line for line in src.splitlines() if "claude:viewport-fit-sides" not in line)

# 最初の </style> までを <head> に、残りを <body> に入れる
cut = src.index("</style>") + len("</style>")
head_part, body_part = src[:cut], src[cut:]

HEAD = """<!doctype html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="description" content="ひらがな・カタカナの五十音と濁音で遊べる、幼児向けのもじあそび">
<meta name="theme-color" content="#bfe8ff">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-title" content="もじもり">
<link rel="icon" type="image/png" sizes="32x32" href="icons/icon-32.png">
<link rel="apple-touch-icon" sizes="180x180" href="icons/icon-180.png">
<link rel="manifest" href="manifest.webmanifest">
<style>:root{box-sizing:border-box;padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}body{margin:0;font:14px -apple-system,BlinkMacSystemFont,sans-serif}[hidden]{display:none!important}</style>
"""

out = HEAD + head_part.strip() + "\n</head>\n<body>\n" + body_part.strip() + "\n</body>\n</html>\n"
(ROOT / "index.html").write_text(out, encoding="utf-8")
print("index.html を作りました")
