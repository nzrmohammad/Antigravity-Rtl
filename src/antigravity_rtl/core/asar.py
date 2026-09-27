#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Antigravity RTL - Electron ASAR Archive Manager (OOP)
High-performance, pure Python binary parser and builder for Electron ASAR format archives.
Follows the official Electron ASAR binary specification including SHA-256 block integrity hashes.
"""

import os
import json
import struct
import hashlib
from typing import Optional, Dict, Any, Tuple


def sha256_blocks(data: bytes, block_size: int = 4 * 1024 * 1024) -> Dict[str, Any]:
    """Calculates Electron-compatible SHA256 integrity block hashes."""
    blocks = []
    for i in range(0, len(data), block_size):
        chunk = data[i:i + block_size]
        blocks.append(hashlib.sha256(chunk).hexdigest())
    return {
        "algorithm": "SHA256",
        "hash": hashlib.sha256(data).hexdigest(),
        "blockSize": block_size,
        "blocks": blocks
    }


class AsarArchive:
    """
    Object-Oriented handler for Electron ASAR archives.
    Pure Python parser and builder compliant with Electron 20+ ASAR specifications.
    """

    def __init__(self, file_path: str):
        self.file_path = file_path

    def extract_file(self, target_path: str) -> Optional[str]:
        """Extracts and decodes a UTF-8 text file from inside the ASAR archive."""
        if not os.path.isfile(self.file_path):
            return None
        try:
            with open(self.file_path, "rb") as f:
                header_raw = f.read(16)
                if len(header_raw) < 16:
                    return None
                magic, size_total, size_header, json_len = struct.unpack("<IIII", header_raw)
                if magic != 4:
                    return None

                json_bytes = f.read(json_len)
                header = json.loads(json_bytes.decode("utf-8"))

                padding = (4 - (json_len % 4)) % 4
                payload_start = 16 + json_len + padding

                parts = target_path.replace("\\", "/").split("/")
                curr = header
                for p in parts:
                    if "files" in curr and p in curr["files"]:
                        curr = curr["files"][p]
                    else:
                        return None

                if "offset" in curr and "size" in curr:
                    offset = int(curr["offset"])
                    size = int(curr["size"])
                    f.seek(payload_start + offset)
                    file_data = f.read(size)
                    return file_data.decode("utf-8", errors="replace")
        except Exception:
            return None
        return None

    def get_metadata(self) -> Optional[Dict[str, Any]]:
        """Extracts version and patch status metadata from this ASAR archive."""
        if not os.path.isfile(self.file_path):
            return None
        try:
            mtime = os.path.getmtime(self.file_path)
            size = os.path.getsize(self.file_path)

            pkg_code = self.extract_file("package.json")
            version_str = "0.0.0"
            if pkg_code:
                try:
                    pkg = json.loads(pkg_code)
                    version_str = pkg.get("version", "0.0.0")
                except Exception:
                    pass

            v_parts = []
            for p in version_str.split("."):
                nums = "".join(filter(str.isdigit, p))
                v_parts.append(int(nums) if nums else 0)
            while len(v_parts) < 3:
                v_parts.append(0)

            preload_code = self.extract_file("dist/preload.js")
            is_patched = "__ANTIGRAVITY_RTL_INJECTED__" in (preload_code or "")

            return {
                "version_str": version_str,
                "version_tuple": tuple(v_parts),
                "is_patched": is_patched,
                "mtime": mtime,
                "size": size,
                "path": self.file_path
            }
        except Exception:
            return None

    def patch_files(self, output_path: str, replacements: Dict[str, Any]):
        """
        Reconstructs the ASAR archive replacing files in-place with new content.
        Follows the exact Electron ASAR binary specification with SHA256 integrity block hashes.
        """
        with open(self.file_path, "rb") as f_in:
            header_raw = f_in.read(16)
            if len(header_raw) < 16:
                raise ValueError("Unexpected EOF while reading ASAR header")
            magic, size_total, size_header, json_len = struct.unpack("<IIII", header_raw)
            if magic != 4:
                raise ValueError(f"Invalid ASAR format (Magic: {magic})")

            json_bytes = f_in.read(json_len)
            header = json.loads(json_bytes.decode("utf-8"))

            padding = (4 - (json_len % 4)) % 4
            payload_start = 16 + json_len + padding

            file_entries = []
            def traverse(curr, parts):
                if "files" in curr:
                    for name, child in curr["files"].items():
                        traverse(child, parts + [name])
                else:
                    is_unpacked = curr.get("unpacked", False)
                    file_entries.append((parts, is_unpacked, curr))

            traverse(header, [])

            norm_replacements = {}
            for k, v in replacements.items():
                k_norm = k.replace("\\", "/")
                if isinstance(v, str):
                    norm_replacements[k_norm] = v.encode("utf-8")
                else:
                    norm_replacements[k_norm] = v

            new_payload = bytearray()
            current_offset = 0

            for parts, is_unpacked, node in file_entries:
                path_str = "/".join(parts)
                if is_unpacked:
                    continue

                if path_str in norm_replacements:
                    content = norm_replacements[path_str]
                    print(f"  [+] Updated in archive: {path_str} ({len(content):,} bytes)")
                else:
                    old_offset = int(node["offset"])
                    old_size = int(node["size"])
                    f_in.seek(payload_start + old_offset)
                    content = f_in.read(old_size)

                node["offset"] = str(current_offset)
                node["size"] = len(content)
                node["integrity"] = sha256_blocks(content)
                new_payload.extend(content)
                current_offset += len(content)

        new_json_bytes = json.dumps(header, separators=(",", ":")).encode("utf-8")
        new_json_len = len(new_json_bytes)
        new_padding_len = (4 - (new_json_len % 4)) % 4
        new_padding = b"\0" * new_padding_len

        new_size_header = new_json_len + new_padding_len + 4
        new_size_total = new_size_header + 4
        new_header_prefix = struct.pack("<IIII", 4, new_size_total, new_size_header, new_json_len)

        with open(output_path, "wb") as out:
            out.write(new_header_prefix)
            out.write(new_json_bytes)
            out.write(new_padding)
            out.write(new_payload)

    @staticmethod
    def compare_versions(v1: Tuple[int, ...], v2: Tuple[int, ...]) -> int:
        """Returns 1 if v1 > v2, -1 if v1 < v2, 0 if v1 == v2."""
        for a, b in zip(v1, v2):
            if a > b:
                return 1
            if a < b:
                return -1
        return 0
