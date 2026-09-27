#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Antigravity RTL - Platform & Installation Detector (OOP)
Locates Antigravity installation across Windows, macOS, and Linux via processes, registries, and standard filesystem trees.
"""

import os
import sys
import subprocess
from typing import Optional, List, Tuple


class PlatformDetector:
    """
    Detects and validates Antigravity IDE installation directories.
    """

    @classmethod
    def find_installation(cls, custom_path: Optional[str] = None) -> Optional[str]:
        """
        Locates the root Antigravity installation directory.
        """
        if custom_path:
            cp = os.path.abspath(custom_path.strip().strip('"'))
            for rel in ["resources/app.asar", "Contents/Resources/app.asar", "app.asar"]:
                if os.path.isfile(os.path.join(cp, rel)):
                    return cp
            if os.path.isfile(cp) and cp.endswith("app.asar"):
                parent = os.path.dirname(cp)
                if os.path.basename(parent).lower() == "resources":
                    return os.path.dirname(parent)
                return parent

        candidates: List[str] = []

        # 1. Active running processes
        try:
            if sys.platform == "win32":
                ps_cmd = 'Get-Process Antigravity -ErrorAction SilentlyContinue | Select-Object -ExpandProperty Path'
                res = subprocess.run(
                    ['powershell', '-NoProfile', '-Command', ps_cmd],
                    capture_output=True,
                    text=True,
                    timeout=3
                )
                if res.returncode == 0 and res.stdout.strip():
                    for line in res.stdout.strip().splitlines():
                        p = line.strip()
                        if os.path.isfile(p) and p.lower().endswith("antigravity.exe"):
                            d = os.path.dirname(p)
                            if d not in candidates:
                                candidates.append(d)
            elif sys.platform == "darwin":
                res = subprocess.run(["pgrep", "-fl", "Antigravity"], capture_output=True, text=True, timeout=3)
                if res.returncode == 0 and res.stdout.strip():
                    for line in res.stdout.strip().splitlines():
                        if ".app" in line:
                            idx = line.find(".app")
                            app_p = line[:idx + 4].split()[-1]
                            if os.path.isdir(app_p) and app_p not in candidates:
                                candidates.append(app_p)
            else:
                res = subprocess.run(["pgrep", "-fl", "antigravity"], capture_output=True, text=True, timeout=3)
                if res.returncode == 0 and res.stdout.strip():
                    for line in res.stdout.strip().splitlines():
                        parts = line.split()
                        if len(parts) >= 2 and os.path.isfile(parts[1]):
                            d = os.path.dirname(parts[1])
                            if d not in candidates:
                                candidates.append(d)
        except Exception:
            pass

        # 2. Platform standard installation locations
        if sys.platform == "win32":
            local_app_data = os.environ.get("LOCALAPPDATA", "")
            if local_app_data:
                std_path = os.path.join(local_app_data, "Programs", "antigravity")
                if os.path.isdir(std_path) and std_path not in candidates:
                    candidates.append(std_path)

            # Registry search
            try:
                import winreg
                reg_paths = [
                    (winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Uninstall\antigravity"),
                    (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\antigravity"),
                    (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall\antigravity")
                ]
                for root_key, sub_key in reg_paths:
                    try:
                        with winreg.OpenKey(root_key, sub_key) as key:
                            loc, _ = winreg.QueryValueEx(key, "InstallLocation")
                            if loc and os.path.isdir(loc) and loc not in candidates:
                                candidates.append(loc)
                    except Exception:
                        pass
            except Exception:
                pass

            for prog_env in ["ProgramFiles", "ProgramFiles(x86)", "ProgramW6432"]:
                pf = os.environ.get(prog_env, "")
                if pf:
                    p = os.path.join(pf, "Antigravity")
                    if os.path.isdir(p) and p not in candidates:
                        candidates.append(p)
                    p_lower = os.path.join(pf, "antigravity")
                    if os.path.isdir(p_lower) and p_lower not in candidates:
                        candidates.append(p_lower)

            roaming = os.environ.get("APPDATA", "")
            if roaming:
                p_roam = os.path.join(roaming, "Programs", "antigravity")
                if os.path.isdir(p_roam) and p_roam not in candidates:
                    candidates.append(p_roam)

        elif sys.platform == "darwin":
            mac_dirs = [
                "/Applications/Antigravity.app",
                os.path.expanduser("~/Applications/Antigravity.app"),
                "/Applications/Google Antigravity.app",
                os.path.expanduser("~/Applications/Google Antigravity.app")
            ]
            for md in mac_dirs:
                if os.path.isdir(md) and md not in candidates:
                    candidates.append(md)

        else:
            linux_dirs = [
                "/opt/Antigravity",
                "/opt/antigravity",
                "/usr/lib/antigravity",
                "/usr/share/antigravity",
                os.path.expanduser("~/.local/share/programs/antigravity"),
                os.path.expanduser("~/.local/share/antigravity")
            ]
            for ld in linux_dirs:
                if os.path.isdir(ld) and ld not in candidates:
                    candidates.append(ld)

        # 3. Verify presence of app.asar
        for c in candidates:
            for sub in [
                os.path.join(c, "resources", "app.asar"),
                os.path.join(c, "Contents", "Resources", "app.asar"),
                os.path.join(c, "app.asar")
            ]:
                if os.path.isfile(sub):
                    return c

        return None

    @classmethod
    def resolve_resources_dir(cls, target_dir: str) -> str:
        """Finds the directory containing app.asar inside target_dir."""
        resources_dir = os.path.join(target_dir, "resources")
        if not os.path.isdir(resources_dir):
            for candidate in [
                os.path.join(target_dir, "Contents", "Resources"),
                os.path.join(target_dir, "Resources"),
                target_dir
            ]:
                if os.path.isfile(os.path.join(candidate, "app.asar")):
                    return candidate
        return resources_dir
