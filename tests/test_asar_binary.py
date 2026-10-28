#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Binary tests for Electron ASAR format integrity and compliance.
Uses synthetic ASAR archives to run 100% self-contained across CI and all OS platforms.
"""

import os
import sys
import json
import struct
import unittest
import tempfile

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)), "src"))

from antigravity_rtl.core.asar import AsarArchive
from synthetic_asar import build_synthetic_asar


class TestAsarBinary(unittest.TestCase):

    def test_asar_rebuild_and_integrity(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            input_asar = os.path.join(tmpdir, "input.asar")
            out_asar = os.path.join(tmpdir, "test.asar")

            # 0. Generate synthetic, spec-compliant ASAR
            build_synthetic_asar(input_asar, version="2.28.0", is_patched=False)
            archive = AsarArchive(input_asar)

            replacements = {
                "dist/preload.js": "console.log('test-rtl'); /* __ANTIGRAVITY_RTL_INJECTED__ */"
            }
            stats = archive.patch_files(out_asar, replacements)

            # Check stats dictionary return
            self.assertIsInstance(stats, dict)
            self.assertEqual(stats["updated_count"], 1)
            self.assertEqual(stats["updated_files"][0]["path"], "dist/preload.js")

            # 1. Verify binary header structure matches Electron C++ Archive::Init spec
            with open(out_asar, "rb") as f:
                hdr = f.read(16)
                magic, size_total, size_header, json_len = struct.unpack("<IIII", hdr)
                self.assertEqual(magic, 4)

                pad = (4 - (json_len % 4)) % 4
                self.assertEqual(size_header, json_len + pad + 4)
                self.assertEqual(size_total, size_header + 4)

                raw_json = f.read(json_len)
                header = json.loads(raw_json.decode("utf-8"))
                self.assertIn("files", header)

                # Check SHA256 integrity block
                preload_node = header["files"]["dist"]["files"]["preload.js"]
                self.assertIn("integrity", preload_node)
                self.assertEqual(preload_node["integrity"]["algorithm"], "SHA256")
                self.assertTrue(len(preload_node["integrity"]["hash"]) == 64)

            # 2. Verify extraction of both modified and unmodified files
            out_archive = AsarArchive(out_asar)
            extracted_preload = out_archive.extract_file("dist/preload.js")
            self.assertEqual(extracted_preload, replacements["dist/preload.js"])

            extracted_pkg = out_archive.extract_file("package.json")
            self.assertIsNotNone(extracted_pkg)
            self.assertIn("version", extracted_pkg)

            # 3. Verify metadata
            meta = out_archive.get_metadata()
            orig_meta = archive.get_metadata()
            self.assertTrue(meta["is_patched"])
            self.assertEqual(meta["version_str"], orig_meta["version_str"])
            self.assertEqual(meta["version_tuple"], (2, 28, 0))


if __name__ == "__main__":
    unittest.main()
