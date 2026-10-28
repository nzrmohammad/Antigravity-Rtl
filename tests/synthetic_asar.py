#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Helper utility for generating synthetic, standard-compliant Electron ASAR archives for testing.
Completely removes any reliance on hardcoded local disk paths.
"""

import os
import json
import struct
from typing import Dict, Union, Optional
from antigravity_rtl.core.asar import sha256_blocks


def build_synthetic_asar(
    output_path: str,
    files: Optional[Dict[str, Union[str, bytes]]] = None,
    version: str = "2.28.0",
    is_patched: bool = False
) -> str:
    """
    Builds a synthetic Electron ASAR archive containing mock files.
    """
    if files is None:
        preload_content = "console.log('original-preload');"
        if is_patched:
            preload_content += "\n/* __ANTIGRAVITY_RTL_INJECTED__ */"

        files = {
            "package.json": json.dumps({"name": "antigravity", "version": version}),
            "dist/preload.js": preload_content,
            "dist/updater.js": "class Updater { quitAndInstall() { return true; } }",
            "node_modules/electron-updater/out/NsisUpdater.js": "class NsisUpdater { quitAndInstall(isSilent, isForce) { return true; } }",
            "node_modules/electron-updater/out/BaseUpdater.js": "class BaseUpdater { install(isSilent, isForce) { return true; } }"
        }

    header = {"files": {}}
    payload = bytearray()
    curr_offset = 0

    for path_str, content in files.items():
        if isinstance(content, str):
            data = content.encode("utf-8")
        else:
            data = content

        parts = path_str.replace("\\", "/").split("/")
        curr = header["files"]
        for p in parts[:-1]:
            if p not in curr:
                curr[p] = {"files": {}}
            curr = curr[p]["files"]

        curr[parts[-1]] = {
            "offset": str(curr_offset),
            "size": len(data),
            "integrity": sha256_blocks(data)
        }
        payload.extend(data)
        curr_offset += len(data)

    json_bytes = json.dumps(header, separators=(",", ":")).encode("utf-8")
    json_len = len(json_bytes)
    pad_len = (4 - (json_len % 4)) % 4
    pad = b"\0" * pad_len
    size_hdr = json_len + pad_len + 4
    size_tot = size_hdr + 4
    hdr_prefix = struct.pack("<IIII", 4, size_tot, size_hdr, json_len)

    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    with open(output_path, "wb") as f:
        f.write(hdr_prefix)
        f.write(json_bytes)
        f.write(pad)
        f.write(payload)

    return output_path
