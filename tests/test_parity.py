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
        ]
        for feat in essential_features:
            self.assertIn(feat, py_injection, f"Feature '{feat}' missing in Python CodeInjector")
            self.assertIn(feat, js_code, f"Feature '{feat}' missing in patcher.js")


if __name__ == "__main__":
    unittest.main()
