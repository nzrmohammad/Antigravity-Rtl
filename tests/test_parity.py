#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Parity & asset synchronization unit tests.
Validates that Python and JavaScript implementations and CSS bundles remain strictly synchronized.
"""

import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)), "src"))

from antigravity_rtl.assets import get_effective_css


class TestParity(unittest.TestCase):

    def setUp(self):
        self.root_dir = os.path.dirname(os.path.dirname(__file__))
        self.src_dir = os.path.join(self.root_dir, "src")
        self.css_path = os.path.join(self.src_dir, "antigravity-chat-rtl.css")
        self.patcher_js_path = os.path.join(self.src_dir, "patcher.js")

    def test_css_asset_parity(self):
        """Verifies that assets.py matches the bundled CSS."""
        self.assertTrue(os.path.isfile(self.css_path))
        with open(self.css_path, "r", encoding="utf-8") as f:
            css_disk = f.read()

        css_effective = get_effective_css()
        self.assertEqual(css_disk.strip(), css_effective.strip())

    def test_font_inclusions_in_css(self):
        """Verifies that essential fonts (Vazirmatn, JetBrains Mono, Inter) are embedded."""
        css = get_effective_css()
        self.assertIn("font-family: 'Vazirmatn'", css)
        self.assertIn("font-family: 'JetBrains Mono'", css)
        self.assertIn("font-family: 'Inter'", css)
        self.assertIn("data:font/woff2;charset=utf-8;base64,", css)

    def test_smart_justify_rules_in_css(self):
        """Verifies that Smart Justify rules are declared in the CSS."""
        css = get_effective_css()
        self.assertIn("ag-text-justify", css)
        self.assertIn("text-align: justify", css)
        self.assertIn("text-align-last: right", css)

    def test_input_toolbar_unflipped(self):
        """Verifies that the model selector and action toolbar are preserved LTR."""
        css = get_effective_css()
        self.assertIn('button[data-testid="model-selector-trigger"]', css)
        self.assertIn('direction: ltr !important;', css)

    def test_js_parity_and_presence(self):
        """Verifies that patcher.js exists and contains RTL_CSS."""
        self.assertTrue(os.path.isfile(self.patcher_js_path))
        with open(self.patcher_js_path, "r", encoding="utf-8") as f:
            js_code = f.read()
        self.assertIn("const RTL_CSS = `", js_code)
        self.assertIn("Vazirmatn", js_code)
        self.assertIn("JetBrains Mono", js_code)

    def test_js_css_deep_parity(self):
        """Extracts RTL_CSS from patcher.js and verifies exact string parity with get_effective_css()."""
        import re
        self.assertTrue(os.path.isfile(self.patcher_js_path))
        with open(self.patcher_js_path, "r", encoding="utf-8") as f:
            js_code = f.read()

        match = re.search(r'const RTL_CSS\s*=\s*`(.*?)`;\n', js_code, re.DOTALL)
        self.assertIsNotNone(match, "RTL_CSS declaration not found in patcher.js")

        extracted_raw = match.group(1)
        effective = get_effective_css()

        unescaped = extracted_raw.replace(r"\${", "${").replace(r"\`", "`").replace(r"\\", "\\")
        self.assertEqual(len(unescaped.strip()), len(effective.strip()), "Unescaped CSS length in patcher.js differs from get_effective_css()")
        self.assertEqual(unescaped.strip(), effective.strip(), "CSS in patcher.js does not match get_effective_css() character-for-character")

    def test_version_synchronization(self):
        """Verifies that constants.VERSION matches pyproject.toml version."""
        import re
        from antigravity_rtl.constants import VERSION

        pyproject_path = os.path.join(self.root_dir, "pyproject.toml")
        self.assertTrue(os.path.isfile(pyproject_path))
        with open(pyproject_path, "r", encoding="utf-8") as f:
            content = f.read()

        m = re.search(r'^version\s*=\s*["\']([^"\']+)["\']', content, re.MULTILINE)
        self.assertIsNotNone(m, "version field not found in pyproject.toml")
        pyproject_ver = m.group(1)
        self.assertEqual(VERSION, pyproject_ver, f"Version mismatch: constants.py ({VERSION}) vs pyproject.toml ({pyproject_ver})")

    def test_client_injection_feature_parity(self):
        """Verifies that Python CodeInjector and patcher.js share identical logic and migration rules."""
        from antigravity_rtl.core.injector import CodeInjector
        py_injection = CodeInjector.get_client_injection("MOCK_CSS")

        with open(self.patcher_js_path, "r", encoding="utf-8") as f:
            js_code = f.read()

        # Directly extract the client injection payload from patcher.js
        start_marker = "/* __ANTIGRAVITY_RTL_INJECTED__ */"
        idx_start = js_code.find(start_marker)
        self.assertNotEqual(idx_start, -1, "Injection start marker missing in patcher.js")
        idx_end = js_code.find("const patchedPreload = preloadCode", idx_start)
        self.assertNotEqual(idx_end, -1, "Injection end marker missing in patcher.js")
        js_injection = js_code[idx_start:idx_end]

        essential_features = [
            "justifyText",
            "ag-text-justify",
            "JetBrains Mono",
            "Inter",
            "parsed.codeFont === 'default'",
            "conversation-row-sidebar",
            "detectSmartDirection",
            "applySmartDirectionToElement",
            "isFontAvailable",
            "getFontStatus",
            "ag-font-family-badge",
            "ag-code-font-badge",
            "Bundled (Ready)",
            "Installed on OS",
            "proxyEnabled",
            "proxyType",
            "proxyHost",
            "proxyPort",
            "syncProxyConfigToFile",
            "testProxyConnection",
            "ag-toggle-proxy",
            "ag-proxy-test-btn",
            "ag-proxy-preset-btn",
            ".bak",
            "0x05, 0x01, 0x00",
            "7890",
            "7897",
            "10808",
            "10809",
            "2080",
            "user-message-content",
            "whitespace-pre-wrap",
            "updateInputDirection",
            "isInsideTechnicalContainer",
            "agy-button agy-button-sm",
            "calc(100vh",
        ]
        for feat in essential_features:
            self.assertIn(feat, py_injection, f"Feature '{feat}' missing in Python CodeInjector")
            self.assertIn(feat, js_injection, f"Feature '{feat}' missing in patcher.js direct client payload")

    def test_smart_direction_bilingual_examples(self):
        """Verifies that English-starting Persian sentences (technical tokens, commit logs) detect as RTL."""
        import subprocess
        import json

        with open(self.patcher_js_path, "r", encoding="utf-8") as f:
            code = f.read()

        fn_marker = "function detectSmartDirection(text, fallbackDir) {"
        start_idx = code.find(fn_marker)
        self.assertNotEqual(start_idx, -1, "detectSmartDirection not found in patcher.js")
        end_marker = "function isInsideTechnicalContainer(node) {"
        end_idx = code.find(end_marker, start_idx)
        self.assertNotEqual(end_idx, -1, "isInsideTechnicalContainer not found in patcher.js")
        fn_code = code[start_idx:end_idx]

        runner_script = f"""
{fn_code}

const userExamples = [
    '.env.example و README.md: اجباری شدن BACKUP_PASSWORD و هماهنگی زمانبندی.',
    'app.html و admin.html: اعداد انگلیسی بازه‌ها (7 روز، 30 روز، هفته 1 تا 4) و اصلاح برچسب مجموع مصرف دیروز.',
    'user_subscription_detail.py: بازگرداندن بازه‌های توزیع مصرف به ۱۲ بازهٔ ۲ ساعته.',
    'app.js و charts.js و admin_charts.js: هماهنگی داده‌های ۲ ساعته و ارقام انگلیسی نمودارها و رده‌بندی.',
    'tailwind.config.js، base.css، components.css و tailwind.min.css: اعمال یکپارچهٔ فونت وزیرمتن و جلوگیری از بازگشت به فونت پیش‌فرض سیستم در دسکتاپ.'
];

const results = userExamples.map(s => detectSmartDirection(s));
const engResults = [
    detectSmartDirection('const x = 123; // calculate value'),
    detectSmartDirection('This is a completely English sentence explaining code.'),
    detectSmartDirection('git commit -m "feat: added new feature"')
];

console.log(JSON.stringify({{ rtl: results, ltr: engResults }}));
"""
        proc = subprocess.run(["node", "-e", runner_script], capture_output=True, text=True, encoding="utf-8")
        self.assertEqual(proc.returncode, 0, f"Node script execution failed: {proc.stderr}")
        out = json.loads(proc.stdout.strip())

        for idx, res in enumerate(out["rtl"]):
            self.assertEqual(res, "rtl", f"User example {idx + 1} failed to detect as RTL")

        for idx, res in enumerate(out["ltr"]):
            self.assertEqual(res, "ltr", f"English example {idx + 1} failed to detect as LTR")


if __name__ == "__main__":
    unittest.main()
