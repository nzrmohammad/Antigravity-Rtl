#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Unit tests for Antigravity RTL Modular OOP Architecture
"""

import os
import sys
import unittest
import tempfile

# Add src and tests to sys.path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)), "src"))
sys.path.insert(0, os.path.dirname(__file__))

from antigravity_rtl.constants import VERSION, DEFAULT_SETTINGS
from antigravity_rtl.core.detector import PlatformDetector
from antigravity_rtl.core.injector import CodeInjector
from antigravity_rtl.core.asar import AsarArchive
from antigravity_rtl.core.patcher import AntigravityPatcher
from antigravity_rtl.ui.terminal import TerminalUI
from synthetic_asar import build_synthetic_asar


class TestOOPArchitecture(unittest.TestCase):

    def test_constants(self):
        self.assertTrue(len(VERSION) >= 3)
        self.assertIn("rtlEnabled", DEFAULT_SETTINGS)
        self.assertIn("justifyText", DEFAULT_SETTINGS)
        self.assertEqual(DEFAULT_SETTINGS["fontFamily"], "Vazirmatn")
        self.assertEqual(DEFAULT_SETTINGS["codeFont"], "JetBrains Mono")

    def test_terminal_ui(self):
        card = TerminalUI.render_shadow_card("TEST CARD", ["Line 1", "Line 2"], width=50)
        self.assertIn("TEST CARD", card)
        self.assertIn("Line 1", card)
        self.assertIn("Line 2", card)

        logo = TerminalUI.get_gradient_logo()
        self.assertTrue(len(logo) > 100)

    def test_injector_code_generation(self):
        injection = CodeInjector.get_client_injection("/* test css */")
        self.assertIn("__ANTIGRAVITY_RTL_INJECTED__", injection)
        self.assertIn("initAppearanceMenu", injection)
        self.assertIn("showRTLToast", injection)
        self.assertIn("justifyText", injection)
        self.assertIn("ag-text-justify", injection)
        self.assertIn("/* test css */", injection)

        hook = CodeInjector.get_updater_hook()
        self.assertIn("__ANTIGRAVITY_UPDATE_HOOK__", hook)
        self.assertIn("pythonw.exe", hook)

    def test_platform_detector(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            res_dir = os.path.join(tmp_dir, "resources")
            os.makedirs(res_dir)
            asar_file = os.path.join(res_dir, "app.asar")
            with open(asar_file, "w") as f:
                f.write("mock asar")

            resolved = PlatformDetector.find_installation(tmp_dir)
            self.assertEqual(os.path.abspath(resolved), os.path.abspath(tmp_dir))

            res_found = PlatformDetector.resolve_resources_dir(tmp_dir)
            self.assertEqual(os.path.abspath(res_found), os.path.abspath(res_dir))

            user_data = PlatformDetector.get_user_data_dir()
            self.assertTrue(len(user_data) > 0)
            app_dir = PlatformDetector.get_antigravity_data_dir()
            self.assertTrue(app_dir.endswith("Antigravity"))

    def test_asar_compare_versions(self):
        self.assertEqual(AsarArchive.compare_versions((2, 17, 0), (2, 16, 9)), 1)
        self.assertEqual(AsarArchive.compare_versions((2, 17, 0), (2, 17, 0)), 0)
        self.assertEqual(AsarArchive.compare_versions((2, 16, 0), (2, 17, 0)), -1)

    def test_patcher_diagnostics(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            patcher = AntigravityPatcher(tmp_dir)
            diag = patcher.diagnostics()
            self.assertIn("target_dir", diag)
            self.assertIn("asar_exists", diag)
            self.assertIn("is_patched", diag)
            self.assertIn("is_running", diag)
            self.assertFalse(diag["asar_exists"])
            self.assertFalse(diag["is_patched"])

    def test_full_patch_restore_lifecycle(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            res_dir = os.path.join(tmp_dir, "resources")
            os.makedirs(res_dir)
            asar_path = os.path.join(res_dir, "app.asar")
            build_synthetic_asar(asar_path, version="2.28.0", is_patched=False)

            patcher = AntigravityPatcher(tmp_dir)

            # 1. Test Dry-Run simulation
            ok_dry = patcher.patch(kill=False, install_shortcuts=False, dry_run=True)
            self.assertTrue(ok_dry)
            is_patched_dry, _ = patcher.get_status()
            self.assertFalse(is_patched_dry)

            # 2. Test actual patch
            ok_patch = patcher.patch(kill=False, install_shortcuts=False, dry_run=False)
            self.assertTrue(ok_patch)

            is_p, _ = patcher.get_status()
            self.assertTrue(is_p)
            self.assertTrue(os.path.isfile(patcher.backup_path))

            # 3. Test factory restore
            ok_restore = patcher.restore(kill=False)
            self.assertTrue(ok_restore)

            is_p_after, _ = patcher.get_status()
            self.assertFalse(is_p_after)


if __name__ == "__main__":
    unittest.main()
