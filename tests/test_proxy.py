#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Unit tests for ProxyManager: Cryptographic verification, smart config merge,
automatic backups, unified constants, and SOCKS5/HTTP protocol handshakes.
"""

import os
import json
import socket
import shutil
import sys
import tempfile
import threading
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)), "src"))

from antigravity_rtl.constants import (
    DEFAULT_PROXY_PORT,
    DEFAULT_PROXY_HOST,
    DEFAULT_PROXY_TYPE,
    PROXY_VERSION_DLL_SHA256,
)
from antigravity_rtl.core.proxy import ProxyManager


class TestProxyManager(unittest.TestCase):
    """Test suite for ProxyManager security, configuration, and connectivity verification."""

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp(prefix="ag_proxy_test_")

    def tearDown(self):
        if os.path.isdir(self.temp_dir):
            shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_unified_constants(self):
        """Verifies unified default proxy constants across the project."""
        self.assertEqual(DEFAULT_PROXY_PORT, 10808)
        self.assertEqual(DEFAULT_PROXY_HOST, "127.0.0.1")
        self.assertEqual(DEFAULT_PROXY_TYPE, "socks5")
        self.assertEqual(ProxyManager.DEFAULT_PORT, 10808)
        self.assertEqual(ProxyManager.DEFAULT_HOST, "127.0.0.1")
        self.assertEqual(ProxyManager.DEFAULT_TYPE, "socks5")

    def test_bundled_binary_cryptographic_integrity(self):
        """Verifies that the bundled version.dll strictly matches the pinned release SHA-256."""
        bundled_dll = ProxyManager.get_bundled_dll_path()
        self.assertTrue(os.path.isfile(bundled_dll), f"version.dll not found at {bundled_dll}")

        computed_hash = ProxyManager.compute_sha256(bundled_dll)
        self.assertEqual(
            computed_hash,
            PROXY_VERSION_DLL_SHA256.lower(),
            f"SHA-256 mismatch for bundled binary: {computed_hash} != {PROXY_VERSION_DLL_SHA256}"
        )
        self.assertTrue(ProxyManager.verify_binary_integrity(bundled_dll))

    def test_tampered_binary_rejected(self):
        """Ensures that modified/tampered binaries fail cryptographic validation."""
        fake_dll = os.path.join(self.temp_dir, "fake_version.dll")
        with open(fake_dll, "wb") as f:
            f.write(b"NOT_A_VALID_OFFICIAL_RELEASE_DLL")

        self.assertFalse(ProxyManager.verify_binary_integrity(fake_dll))

    def test_build_config_defaults(self):
        """Verifies default config structure, sanitized update mirrors, and port 10808."""
        cfg = ProxyManager.build_config()
        self.assertEqual(cfg["proxy"]["port"], 10808)
        self.assertEqual(cfg["proxy"]["host"], "127.0.0.1")
        self.assertEqual(cfg["proxy"]["type"], "socks5")
        self.assertTrue(cfg["child_injection"])

        # Security check: updates must be disabled with zero untrusted third-party mirrors
        self.assertFalse(cfg["updates"]["enabled"])
        self.assertFalse(cfg["updates"]["allow_insecure_mirrors"])
        self.assertEqual(cfg["updates"]["mirrors"], [])

    def test_build_config_smart_merge(self):
        """Ensures custom user processes and rules are preserved during config rebuilding."""
        custom_base = {
            "custom_user_setting": "preserved_value",
            "log_level": "debug",
            "target_processes": ["custom_ide.exe", "worker.exe"],
            "proxy": {"type": "http", "host": "10.0.0.1", "port": 8080}
        }
        merged = ProxyManager.build_config(host="127.0.0.1", port=10808, proxy_type="socks5", base_config=custom_base)

        # Custom fields preserved
        self.assertEqual(merged["custom_user_setting"], "preserved_value")
        self.assertEqual(merged["log_level"], "debug")
        self.assertEqual(merged["target_processes"], ["custom_ide.exe", "worker.exe"])

        # Proxy updated
        self.assertEqual(merged["proxy"]["host"], "127.0.0.1")
        self.assertEqual(merged["proxy"]["port"], 10808)
        self.assertEqual(merged["proxy"]["type"], "socks5")

    def test_install_and_smart_merge_backup(self):
        """Tests installation, file generation, and non-destructive .bak creation upon update."""
        if os.name != "nt":
            self.skipTest("version.dll deployment tests are Windows-specific.")

        ok = ProxyManager.install(self.temp_dir, host="127.0.0.1", port=10808, proxy_type="socks5")
        self.assertTrue(ok)
        self.assertTrue(ProxyManager.is_installed(self.temp_dir))

        cfg_path = ProxyManager.get_config_path(self.temp_dir)
        self.assertTrue(os.path.isfile(cfg_path))

        # Add a custom rule to simulate an advanced user configuration
        with open(cfg_path, "r", encoding="utf-8") as f:
            cfg_data = json.load(f)
        cfg_data["user_custom_marker"] = 9999
        with open(cfg_path, "w", encoding="utf-8") as f:
            json.dump(cfg_data, f)

        # Run install again with new port (e.g. switching to Clash on 7890)
        ok2 = ProxyManager.install(self.temp_dir, host="127.0.0.1", port=7890, proxy_type="socks5")
        self.assertTrue(ok2)

        # Verify backup was created
        bak_path = cfg_path + ".bak"
        self.assertTrue(os.path.isfile(bak_path))

        # Verify custom marker was preserved in new config
        with open(cfg_path, "r", encoding="utf-8") as f:
            updated_cfg = json.load(f)
        self.assertEqual(updated_cfg.get("user_custom_marker"), 9999)
        self.assertEqual(updated_cfg["proxy"]["port"], 7890)

    def test_uninstall_creates_backup(self):
        """Verifies uninstall removes files and safely archives config.json.bak."""
        if os.name != "nt":
            self.skipTest("version.dll deployment tests are Windows-specific.")

        ProxyManager.install(self.temp_dir, host="127.0.0.1", port=10808)
        cfg_path = ProxyManager.get_config_path(self.temp_dir)
        self.assertTrue(os.path.isfile(cfg_path))

        removed = ProxyManager.uninstall(self.temp_dir)
        self.assertTrue(removed)
        self.assertFalse(os.path.isfile(cfg_path))
        self.assertTrue(os.path.isfile(cfg_path + ".bak"), "Backup was not created before config deletion")

    def test_socks5_handshake_real_socket(self):
        """Runs an in-process mock SOCKS5 server to verify real handshake negotiation."""
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(("127.0.0.1", 0))
        server.listen(1)
        port = server.getsockname()[1]

        def serve_socks5():
            try:
                conn, _ = server.accept()
                data = conn.recv(16)
                if len(data) >= 3 and data[0] == 0x05:
                    conn.sendall(b"\x05\x00")  # Accept SOCKS5 No Auth
                conn.close()
            except Exception:
                pass
            finally:
                server.close()

        t = threading.Thread(target=serve_socks5, daemon=True)
        t.start()

        ok, lat, msg = ProxyManager.test_connection("127.0.0.1", port, proxy_type="socks5")
        t.join(timeout=2.0)

        self.assertTrue(ok)
        self.assertIn("SOCKS5 proxy active & verified", msg)

    def test_socks5_handshake_rejected_on_non_socks(self):
        """Ensures that a non-SOCKS5 HTTP server returns false when tested as SOCKS5."""
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(("127.0.0.1", 0))
        server.listen(1)
        port = server.getsockname()[1]

        def serve_http():
            try:
                conn, _ = server.accept()
                conn.recv(16)
                conn.sendall(b"HTTP/1.1 200 OK\r\n\r\n")  # Non-SOCKS response
                conn.close()
            except Exception:
                pass
            finally:
                server.close()

        t = threading.Thread(target=serve_http, daemon=True)
        t.start()

        ok, lat, msg = ProxyManager.test_connection("127.0.0.1", port, proxy_type="socks5")
        t.join(timeout=2.0)

        self.assertFalse(ok)
        self.assertIn("not a SOCKS5 proxy", msg)


if __name__ == "__main__":
    unittest.main()
