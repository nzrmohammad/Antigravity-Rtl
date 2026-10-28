#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Antigravity RTL - Anti-Sanction & Proxy Shield Manager (OOP)
Manages process-level DLL proxy injection, cryptographic integrity checks,
smart config merging, and real SOCKS5/HTTP protocol reachability tests.
"""

import os
import sys
import json
import time
import socket
import struct
import shutil
import hashlib
from typing import Tuple, Dict, Any, Optional
from ..constants import (
    logger,
    DEFAULT_PROXY_PORT,
    DEFAULT_PROXY_HOST,
    DEFAULT_PROXY_TYPE,
    PROXY_VERSION_DLL_SHA256,
)


class ProxyManager:
    """
    Orchestrates the Anti-Sanction Proxy Shield using native process-level DLL interception
    with strict cryptographic verification, non-destructive config merging, and protocol testing.
    """

    DEFAULT_HOST = DEFAULT_PROXY_HOST
    DEFAULT_PORT = DEFAULT_PROXY_PORT
    DEFAULT_TYPE = DEFAULT_PROXY_TYPE
    EXPECTED_SHA256 = PROXY_VERSION_DLL_SHA256

    @classmethod
    def get_bin_dir(cls) -> str:
        """Returns the bundled binaries directory."""
        core_dir = os.path.dirname(os.path.abspath(__file__))
        pkg_dir = os.path.dirname(core_dir)
        return os.path.join(pkg_dir, "bin")

    @classmethod
    def get_bundled_dll_path(cls) -> str:
        """Returns the absolute path to bundled version.dll."""
        return os.path.join(cls.get_bin_dir(), "version.dll")

    @classmethod
    def get_bundled_template_path(cls) -> str:
        """Returns the path to config.template.json."""
        return os.path.join(cls.get_bin_dir(), "config.template.json")

    @classmethod
    def compute_sha256(cls, file_path: str) -> str:
        """Calculates the SHA-256 hexadecimal digest of a file on disk."""
        if not os.path.isfile(file_path):
            return ""
        hasher = hashlib.sha256()
        with open(file_path, "rb") as f:
            while chunk := f.read(65536):
                hasher.update(chunk)
        return hasher.hexdigest().lower()

    @classmethod
    def verify_binary_integrity(cls, file_path: Optional[str] = None) -> bool:
        """
        Cryptographically verifies that version.dll matches the pinned official release SHA-256.
        Prevents tampering, corrupted downloads, and untrusted binary substitutions.
        """
        target = file_path or cls.get_bundled_dll_path()
        if not os.path.isfile(target):
            logger.error("Binary not found for verification: %s", target)
            return False
        digest = cls.compute_sha256(target)
        is_valid = digest == cls.EXPECTED_SHA256.lower()
        if not is_valid:
            logger.critical(
                "SECURITY ALERT: Binary SHA-256 mismatch!\n  Expected: %s\n  Computed: %s",
                cls.EXPECTED_SHA256,
                digest,
            )
        return is_valid

    @classmethod
    def is_installed(cls, target_dir: str) -> bool:
        """Checks if version.dll is installed in the target Antigravity directory."""
        if not target_dir:
            return False
        dll_path = os.path.join(target_dir, "version.dll")
        return os.path.isfile(dll_path)

    @classmethod
    def get_config_path(cls, target_dir: str) -> str:
        """Returns target config.json path."""
        return os.path.join(target_dir, "config.json")

    @classmethod
    def test_gemini_reachability(
        cls,
        host: str = DEFAULT_HOST,
        port: int = DEFAULT_PORT,
        proxy_type: str = DEFAULT_TYPE,
        timeout: float = 3.5,
        target_host: str = "generativelanguage.googleapis.com",
        target_port: int = 443,
    ) -> Tuple[bool, float, str]:
        """
        Actively verifies end-to-end anti-sanction tunnel through local proxy to Google Gemini API
        (generativelanguage.googleapis.com:443).

        Returns:
            (is_unblocked: bool, latency_ms: float, status_message: str)
        """
        host = (host or cls.DEFAULT_HOST).strip()
        try:
            port = int(port)
        except (ValueError, TypeError):
            return False, 0.0, f"Invalid port: {port}"

        ptype = (proxy_type or cls.DEFAULT_TYPE).lower().strip()
        t0 = time.perf_counter()
        sock = None
        try:
            sock = socket.create_connection((host, port), timeout=timeout)
            sock.settimeout(timeout)

            if ptype == "socks5":
                sock.sendall(b"\x05\x01\x00")
                resp = sock.recv(2)
                if len(resp) < 2 or resp[0] != 0x05 or resp[1] != 0x00:
                    return False, 0.0, "SOCKS5 greeting failed"

                host_bytes = target_host.encode("ascii")
                cmd = b"\x05\x01\x00\x03" + bytes([len(host_bytes)]) + host_bytes + struct.pack(">H", target_port)
                sock.sendall(cmd)
                resp = sock.recv(10)
                t1 = time.perf_counter()
                latency_ms = round((t1 - t0) * 1000.0, 1)

                if len(resp) >= 4 and resp[0] == 0x05 and resp[1] == 0x00:
                    return True, latency_ms, f"Gemini API tunnel verified & unblocked via SOCKS5 ({latency_ms}ms)"
                rep_code = resp[1] if len(resp) >= 2 else 0xFF
                return False, latency_ms, f"Proxy rejected upstream tunnel to {target_host} (REP: 0x{rep_code:02x})"

            elif ptype == "http":
                req = f"CONNECT {target_host}:{target_port} HTTP/1.1\r\nHost: {target_host}:{target_port}\r\nConnection: close\r\n\r\n".encode("ascii")
                sock.sendall(req)
                resp = sock.recv(256)
                t1 = time.perf_counter()
                latency_ms = round((t1 - t0) * 1000.0, 1)
                if b"200" in resp:
                    return True, latency_ms, f"Gemini API tunnel verified & unblocked via HTTP CONNECT ({latency_ms}ms)"
                return False, latency_ms, f"HTTP proxy rejected tunnel to {target_host}"

            return False, 0.0, f"Unsupported proxy type for upstream test: {ptype}"
        except Exception as e:
            return False, 0.0, f"Upstream connection failed: {e}"
        finally:
            if sock:
                try:
                    sock.close()
                except Exception:
                    pass

    @classmethod
    def test_connection(
        cls,
        host: str = DEFAULT_HOST,
        port: int = DEFAULT_PORT,
        timeout: float = 2.0,
        proxy_type: str = DEFAULT_TYPE,
        check_upstream: bool = False,
    ) -> Tuple[bool, float, str]:
        """
        Tests whether a local proxy software is actively listening on host:port and
        verifies the handshake for SOCKS5 or HTTP protocols.
        If check_upstream is True, also verifies end-to-end tunnel to Google Gemini API.

        Returns:
            (is_active: bool, latency_ms: float, status_message: str)
        """
        if check_upstream:
            return cls.test_gemini_reachability(host=host, port=port, proxy_type=proxy_type, timeout=timeout)
        host = (host or cls.DEFAULT_HOST).strip()
        try:
            port = int(port)
        except (ValueError, TypeError):
            return False, 0.0, f"Invalid port number: {port}"

        ptype = (proxy_type or cls.DEFAULT_TYPE).lower().strip()
        t0 = time.perf_counter()
        sock = None
        try:
            sock = socket.create_connection((host, port), timeout=timeout)
            sock.settimeout(timeout)
            t1 = time.perf_counter()
            latency_ms = round((t1 - t0) * 1000.0, 1)

            # Protocol Handshake Verification
            if ptype == "socks5":
                # SOCKS5 Client Greeting: Ver=5, 1 Method, Method 0 (No Auth)
                sock.sendall(b"\x05\x01\x00")
                resp = sock.recv(2)
                t2 = time.perf_counter()
                total_latency = round((t2 - t0) * 1000.0, 1)
                if len(resp) == 2 and resp[0] == 0x05:
                    if resp[1] == 0x00:
                        return (
                            True,
                            total_latency,
                            f"SOCKS5 proxy active & verified on {host}:{port} ({total_latency}ms)",
                        )
                    elif resp[1] == 0xFF:
                        return (
                            False,
                            total_latency,
                            f"Port {host}:{port} is open, but SOCKS5 rejected authentication methods ({total_latency}ms)",
                        )
                    else:
                        return (
                            True,
                            total_latency,
                            f"SOCKS5 proxy active on {host}:{port} (Auth method: 0x{resp[1]:02x}) ({total_latency}ms)",
                        )
                else:
                    return (
                        False,
                        latency_ms,
                        f"Port {host}:{port} is open, but did not respond to SOCKS5 greeting (not a SOCKS5 proxy)",
                    )

            elif ptype == "http":
                # Send minimal HTTP probing request
                sock.sendall(b"HEAD http://www.gstatic.com/generate_204 HTTP/1.1\r\nHost: www.gstatic.com\r\nConnection: close\r\n\r\n")
                resp = sock.recv(256)
                t2 = time.perf_counter()
                total_latency = round((t2 - t0) * 1000.0, 1)
                if b"HTTP/" in resp:
                    return (
                        True,
                        total_latency,
                        f"HTTP proxy active & verified on {host}:{port} ({total_latency}ms)",
                    )
                else:
                    return (
                        False,
                        latency_ms,
                        f"Port {host}:{port} is open, but response does not match HTTP proxy format",
                    )

            # Generic TCP
            return True, latency_ms, f"Port {host}:{port} is open & reachable ({latency_ms}ms)"

        except (ConnectionRefusedError, socket.error) as e:
            err_msg = str(e)
            if "10061" in err_msg or "refused" in err_msg.lower():
                return (
                    False,
                    0.0,
                    f"Connection refused: No proxy app is listening on {host}:{port}",
                )
            if "timed out" in err_msg.lower():
                return (
                    False,
                    0.0,
                    f"Connection timed out: {host}:{port} did not respond within {timeout}s",
                )
            return False, 0.0, f"Connection failed: {err_msg}"
        except Exception as e:
            return False, 0.0, f"Network error: {e}"
        finally:
            if sock:
                try:
                    sock.close()
                except Exception:
                    pass

    @classmethod
    def build_config(
        cls,
        host: str = DEFAULT_HOST,
        port: int = DEFAULT_PORT,
        proxy_type: str = DEFAULT_TYPE,
        base_config: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Builds a configuration dictionary matching Antigravity Proxy specification.
        If base_config is provided, performs a smart non-destructive merge to preserve
        custom user rules, processes, and diagnostic settings.
        """
        if base_config and isinstance(base_config, dict):
            cfg = json.loads(json.dumps(base_config))  # Deep copy
        else:
            tpl_path = cls.get_bundled_template_path()
            cfg = {}
            if os.path.isfile(tpl_path):
                try:
                    with open(tpl_path, "r", encoding="utf-8") as f:
                        cfg = json.load(f)
                except Exception as e:
                    logger.debug("Failed reading template config: %s", e)

            if not cfg:
                cfg = {
                    "child_injection_mode": "filtered",
                    "fake_ip": {"cidr": "198.18.0.0/15", "enabled": True},
                    "traffic_logging": False,
                    "timeout": {"connect": 5000, "recv": 5000, "send": 5000},
                    "diagnostics": {"agent_ip_probe": False},
                    "_version": "2.4",
                    "_comment": "Antigravity-Proxy Configuration",
                    "log_level": "info",
                    "child_injection": True,
                    "proxy_rules": {
                        "routing": {
                            "default_action": "proxy",
                            "priority_mode": "order",
                            "rules": [],
                            "use_default_private": True,
                            "enabled": True,
                        },
                        "allowed_ports": [80, 443],
                        "udp_mode": "auto",
                        "ipv6_mode": "proxy",
                        "udp_fallback": "block",
                        "dns_mode": "direct",
                    },
                    "child_injection_exclude": [],
                    "updates": {
                        "enabled": False,
                        "allow_insecure_mirrors": False,
                        "check_delay_ms": 15000,
                        "timeout_ms": 5000,
                        "notify_once": False,
                        "mirrors": [],
                    },
                    "target_processes": [
                        "agy.exe",
                        "language_server.exe",
                        "language_server_windows",
                        "Antigravity.exe",
                        "Antigravity IDE.exe",
                        "node.exe",
                    ],
                }

        # Ensure updates are securely disabled
        if "updates" not in cfg:
            cfg["updates"] = {}
        cfg["updates"]["enabled"] = False
        cfg["updates"]["allow_insecure_mirrors"] = False
        cfg["updates"]["mirrors"] = []

        # UI notification control (defaults to 'none' for silent background operation)
        if "ui" not in cfg or not isinstance(cfg["ui"], dict):
            cfg["ui"] = {}
        if "load_notify" not in cfg["ui"]:
            cfg["ui"]["load_notify"] = "none"

        cfg["child_injection"] = True
        cfg["proxy"] = {
            "type": (proxy_type or cls.DEFAULT_TYPE).lower().strip(),
            "host": (host or cls.DEFAULT_HOST).strip(),
            "port": int(port),
        }
        return cfg

    @classmethod
    def read_config(cls, target_dir: str) -> Optional[Dict[str, Any]]:
        """Reads and returns the active config.json if present."""
        cfg_path = cls.get_config_path(target_dir)
        if os.path.isfile(cfg_path):
            try:
                with open(cfg_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                logger.debug("Error reading config.json from %s: %s", target_dir, e)
        return None

    @classmethod
    def install(
        cls,
        target_dir: str,
        host: str = DEFAULT_HOST,
        port: int = DEFAULT_PORT,
        proxy_type: str = DEFAULT_TYPE,
    ) -> bool:
        """
        Deploys version.dll and config.json into the target Antigravity installation folder.
        Verifies SHA-256 integrity, creates automatic config backups, and merges settings.
        """
        if sys.platform != "win32":
            logger.debug("Proxy Shield DLL is Windows-specific.")
            return False

        if not os.path.isdir(target_dir):
            return False

        dll_src = cls.get_bundled_dll_path()
        if not os.path.isfile(dll_src):
            logger.error("Bundled version.dll not found at %s", dll_src)
            return False

        # 1. Cryptographic Integrity Check
        if not cls.verify_binary_integrity(dll_src):
            logger.critical("Aborting Proxy Shield installation due to failed SHA-256 integrity check.")
            return False

        target_dll = os.path.join(target_dir, "version.dll")
        target_cfg = cls.get_config_path(target_dir)

        try:
            # 2. Deploy binary safely
            if not os.path.isfile(target_dll):
                shutil.copy2(dll_src, target_dll)
            else:
                try:
                    shutil.copy2(dll_src, target_dll)
                except Exception as ex:
                    logger.debug("version.dll in use by process, keeping active binary: %s", ex)

            # 3. Smart Merge & Automatic Backup of existing config.json
            existing_cfg = None
            if os.path.isfile(target_cfg):
                backup_cfg = target_cfg + ".bak"
                try:
                    shutil.copy2(target_cfg, backup_cfg)
                    with open(target_cfg, "r", encoding="utf-8") as f:
                        existing_cfg = json.load(f)
                except Exception as ex:
                    logger.debug("Notice: Failed reading existing config for merge: %s", ex)

            cfg_data = cls.build_config(
                host=host,
                port=port,
                proxy_type=proxy_type,
                base_config=existing_cfg,
            )
            with open(target_cfg, "w", encoding="utf-8") as f:
                json.dump(cfg_data, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            logger.error("Failed installing proxy shield: %s", e)
            return False

    @classmethod
    def uninstall(cls, target_dir: str) -> bool:
        """
        Removes version.dll and config.json from target directory.
        Preserves an automatic config.json.bak backup so user customizations are never lost.
        If version.dll is locked by a running process, config.json is set to direct/bypass
        so subsequent launches never trigger missing-config errors.
        """
        if not target_dir or not os.path.isdir(target_dir):
            return False

        target_dll = os.path.join(target_dir, "version.dll")
        target_cfg = cls.get_config_path(target_dir)

        # 1. Create safety backup of user config before deletion
        if os.path.isfile(target_cfg):
            try:
                shutil.copy2(target_cfg, target_cfg + ".bak")
            except Exception:
                pass

        removed_dll = False
        if os.path.isfile(target_dll):
            try:
                os.unlink(target_dll)
                removed_dll = True
            except Exception as e:
                logger.debug(
                    "version.dll is locked by running Antigravity process: %s (will be cleaned on restart)",
                    e,
                )

        if removed_dll:
            if os.path.isfile(target_cfg):
                try:
                    os.unlink(target_cfg)
                except Exception as e:
                    logger.debug("Could not remove config.json: %s", e)
            return True
        else:
            # If version.dll exists and is locked, set config to direct mode so no error dialog pops up
            if os.path.isfile(target_dll) and os.path.isfile(target_cfg):
                try:
                    cfg = cls.build_config(proxy_type="direct")
                    cfg["child_injection"] = False
                    with open(target_cfg, "w", encoding="utf-8") as f:
                        json.dump(cfg, f, indent=2, ensure_ascii=False)
                except Exception:
                    pass
            elif os.path.isfile(target_cfg):
                try:
                    os.unlink(target_cfg)
                except Exception:
                    pass
            return False
