#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Antigravity RTL Asset Bundler & Synchronizer
Encodes offline WOFF2 fonts into Base64 and keeps CSS and patcher scripts in sync.
"""

import os
import sys
import base64
import re

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONTS_DIR = os.path.join(ROOT_DIR, "fonts")
SRC_DIR = os.path.join(ROOT_DIR, "src")
CSS_FILE = os.path.join(SRC_DIR, "antigravity-chat-rtl.css")
PATCHER_PY = os.path.join(SRC_DIR, "patcher.py")
ASSETS_PY = os.path.join(SRC_DIR, "antigravity_rtl", "assets.py")
PATCHER_JS = os.path.join(SRC_DIR, "patcher.js")

FONT_MAPPINGS = [
    ("Vazirmatn", 400, "Vazirmatn-Regular.woff2"),
    ("Vazirmatn", 500, "Vazirmatn-Medium.woff2"),
    ("Vazirmatn", 700, "Vazirmatn-Bold.woff2"),
    ("IRANSans", 400, "IRANSans-Regular.woff2"),
    ("IRANSans", 500, "IRANSans-Medium.woff2"),
    ("IRANSans", 700, "IRANSans-Bold.woff2"),
    ("IRANYekan", 400, "IRANYekan-Regular.woff2"),
    ("IRANYekan", 500, "IRANYekan-Medium.woff2"),
    ("IRANYekan", 700, "IRANYekan-Bold.woff2"),
    ("Dana", 400, "Dana-Regular.woff2"),
    ("Dana", 500, "Dana-Medium.woff2"),
    ("Dana", 700, "Dana-Bold.woff2"),
    ("B Nazanin", 400, "B-Nazanin.woff2"),
    ("B Nazanin", 700, "B-Nazanin.woff2"),
    ("Shabnam", 400, "Shabnam.woff2"),
    ("Shabnam", 700, "Shabnam-Bold.woff2"),
    ("Sahel", 400, "Sahel.woff2"),
    ("Sahel", 700, "Sahel-Bold.woff2"),
    ("Samim", 400, "Samim.woff2"),
    ("Samim", 700, "Samim-Bold.woff2"),
]

def encode_font(file_path):
    with open(file_path, "rb") as f:
        data = f.read()
    b64 = base64.b64encode(data).decode("ascii")
    return f"data:font/woff2;charset=utf-8;base64,{b64}"

def generate_font_faces():
    lines = [
        "/* =========================================================",
        "   0. Embedded Offline WOFF2 Fonts (100% Offline, Zero CDN)",
        "   Families: Vazirmatn, IRANSans, IRANYekan, Dana, B Nazanin, Shabnam, Sahel, Samim",
        "   ========================================================= */",
        ""
    ]
    for family, weight, filename in FONT_MAPPINGS:
        font_path = os.path.join(FONTS_DIR, filename)
        if not os.path.isfile(font_path):
            print(f"[!] Warning: Font file missing: {font_path}")
            continue
        data_uri = encode_font(font_path)
        family_clean = family.replace(" ", "")
        lines.append(f"@font-face {{")
        lines.append(f"  font-family: '{family}';")
        if family != family_clean:
            lines.append(f"  src: local('{family}'), local('{family_clean}'), url('{data_uri}') format('woff2');")
        else:
            lines.append(f"  src: local('{family}'), url('{data_uri}') format('woff2');")
        lines.append(f"  font-weight: {weight};")
        lines.append(f"  font-style: normal;")
        lines.append(f"  font-display: swap;")
        lines.append(f"}}\n")
    return "\n".join(lines)

def sync_patchers(css_content):
    print("[*] Synchronizing CSS into assets.py and patcher.js...")
    
    # Sync assets.py (modular OOP engine)
    if os.path.isfile(ASSETS_PY):
        with open(ASSETS_PY, "r", encoding="utf-8") as f:
            py_code = f.read()
        pattern = r'(RTL_CSS\s*=\s*r?""")(.*?)("""\n\ndef get_effective_css)'
        new_py = re.sub(pattern, lambda m: m.group(1) + css_content + m.group(3), py_code, flags=re.DOTALL)
        with open(ASSETS_PY, "w", encoding="utf-8") as f:
            f.write(new_py)
        print("  [OK] assets.py updated.")

    # Sync patcher.py (if monolithic fallback)
    if os.path.isfile(PATCHER_PY):
        with open(PATCHER_PY, "r", encoding="utf-8") as f:
            py_code = f.read()
        if "RTL_CSS" in py_code:
            pattern = r'(RTL_CSS\s*=\s*r?""")(.*?)("""\n# Enable ANSI)'
            new_py = re.sub(pattern, lambda m: m.group(1) + css_content + m.group(3), py_code, flags=re.DOTALL)
            with open(PATCHER_PY, "w", encoding="utf-8") as f:
                f.write(new_py)
            print("  [OK] patcher.py updated.")

    # Sync patcher.js
    if os.path.isfile(PATCHER_JS):
        with open(PATCHER_JS, "r", encoding="utf-8") as f:
            js_code = f.read()
        pattern = r'(const RTL_CSS\s*=\s*`)(.*?)(`;\n)'
        clean_js_css = css_content.replace("\\", "\\\\").replace("`", r"\`").replace("${", r"\${")
        new_js = re.sub(pattern, lambda m: m.group(1) + clean_js_css + m.group(3), js_code, flags=re.DOTALL)
        with open(PATCHER_JS, "w", encoding="utf-8") as f:
            f.write(new_js)
        print("  [OK] patcher.js updated.")

def main():
    print("[*] Reading fonts and verifying assets...")
    if not os.path.isdir(FONTS_DIR):
        print(f"[-] Fonts directory not found: {FONTS_DIR}")
        sys.exit(1)

    font_faces = generate_font_faces()
    
    # Read existing rules after font-faces in CSS
    if os.path.isfile(CSS_FILE):
        with open(CSS_FILE, "r", encoding="utf-8") as f:
            content = f.read()
        # Find where Section 1 starts
        idx = content.find("/* =========================================================\n   1.")
        if idx != -1:
            rules = content[idx:]
        else:
            idx = content.find("/* =========================================================\n   ۱.")
            rules = content[idx:] if idx != -1 else ""
    else:
        rules = ""

    header = """/**
 * Antigravity IDE Chat & Markdown RTL Support (Smart Auto-Direction & Tool Isolation)
 */

"""
    full_css = header + font_faces + "\n" + rules
    with open(CSS_FILE, "w", encoding="utf-8") as f:
        f.write(full_css)
    print(f"[OK] {CSS_FILE} bundled successfully ({len(full_css):,} bytes).")

    if "--sync" in sys.argv or "-s" in sys.argv:
        sync_patchers(full_css)

if __name__ == "__main__":
    main()
