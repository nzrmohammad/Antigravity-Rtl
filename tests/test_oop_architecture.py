#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Unit tests for Antigravity RTL Modular OOP Architecture
"""

import os
import sys
import unittest
import tempfile
import shutil

# Add src to sys.path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)), "src"))

from antigravity_rtl.constants import VERSION, DEFAULT_SETTINGS
from antigravity_rtl.core.detector import PlatformDetector
from antigravity_rtl.core.process import ProcessManager
from antigravity_rtl.core.injector import CodeInjector
from antigravity_rtl.core.asar import AsarArchive
from antigravity_rtl.core.patcher import AntigravityPatcher
from antigravity_rtl.ui.terminal import TerminalUI


class TestOOPArchitecture(unittest.TestCase):

    def test_constants(self):
        self.assertTrue(len(VERSION) >= 3)
        self.assertIn("rtlEnabled", DEFAULT_SETTINGS)
        self.assertEqual(DEFAULT_SETTINGS["fontFamily"], "Vazirmatn")

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
        backup_asar = r"C:\Users\Mohammad\AppData\Local\Programs\antigravity\resources\app.asar.original_backup"
        real_asar = r"C:\Users\Mohammad\AppData\Local\Programs\antigravity\resources\app.asar"
        clean_asar = backup_asar if os.path.isfile(backup_asar) else real_asar
        if not os.path.isfile(clean_asar):
            self.skipTest("Real app.asar not present")

        with tempfile.TemporaryDirectory() as tmp_dir:
            res_dir = os.path.join(tmp_dir, "resources")
            os.makedirs(res_dir)
            shutil.copy2(clean_asar, os.path.join(res_dir, "app.asar"))

            patcher = AntigravityPatcher(tmp_dir)
            ok_patch = patcher.patch(kill=False, install_shortcuts=False)
            self.assertTrue(ok_patch)

            is_p, _ = patcher.get_status()
            self.assertTrue(is_p)
            self.assertTrue(os.path.isfile(patcher.backup_path))

            ok_restore = patcher.restore(kill=False)
            self.assertTrue(ok_restore)

            is_p_after, _ = patcher.get_status()
            self.assertFalse(is_p_after)


if __name__ == "__main__":
    unittest.main()

