#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Antigravity RTL - Auto-Shield & Persistence Manager (OOP)
Handles shortcut redirection, launcher binary installation, and update survival daemon.
"""

import os
import sys
import time
import shutil
import subprocess
from typing import Optional


class AutoShieldManager:
    """
    Manages persistent patch files, launcher shortcuts, and automatic update re-patching.
    """

    @classmethod
    def setup_shortcuts(cls, target_dir: str, launcher_path: str):
        """Redirects desktop and Start Menu shortcuts to AntigravityLauncher.exe."""
        if sys.platform != "win32":
            return
        norm = target_dir.lower().replace('\\', '/')
        if os.environ.get("PYTEST_CURRENT_TEST") or "tmp" in norm or "temp" in norm or "mock" in norm:
            return

        dest_launcher = os.path.join(target_dir, "AntigravityLauncher.exe")
        try:
            shutil.copy2(launcher_path, dest_launcher)
            target_exe = dest_launcher
        except Exception:
            target_exe = launcher_path

        icon_source = os.path.join(target_dir, "Antigravity.exe")
        ps_code = f"""
        $wsh = New-Object -ComObject WScript.Shell
        $paths = @(
            [System.IO.Path]::Combine([System.Environment]::GetFolderPath('Desktop'), 'Antigravity.lnk'),
            [System.IO.Path]::Combine([System.Environment]::GetFolderPath('CommonDesktop'), 'Antigravity.lnk'),
            [System.IO.Path]::Combine([System.Environment]::GetFolderPath('StartMenu'), 'Programs', 'Antigravity.lnk'),
            [System.IO.Path]::Combine([System.Environment]::GetFolderPath('CommonStartMenu'), 'Programs', 'Antigravity.lnk')
        )
        $found = $false
        foreach ($p in $paths) {{
            if (Test-Path $p) {{
                $sc = $wsh.CreateShortcut($p)
                $sc.TargetPath = '{target_exe}'
                $sc.IconLocation = '{icon_source},0'
                $sc.WorkingDirectory = '{target_dir}'
                $sc.Save()
                $found = $true
            }}
        }}
        if (-not $found) {{
            $desktopP = [System.IO.Path]::Combine([System.Environment]::GetFolderPath('Desktop'), 'Antigravity.lnk')
            $sc = $wsh.CreateShortcut($desktopP)
            $sc.TargetPath = '{target_exe}'
            $sc.IconLocation = '{icon_source},0'
            $sc.WorkingDirectory = '{target_dir}'
            $sc.Save()
        }}
        """
        try:
            subprocess.run(['powershell', '-NoProfile', '-Command', ps_code], capture_output=True)
            print("  [OK] Auto-Shield launcher installed & shortcuts protected.")
        except Exception:
            pass

    @classmethod
    def restore_shortcuts(cls, target_dir: str):
        """Restores original shortcuts pointing directly to Antigravity.exe."""
        if sys.platform != "win32":
            return
        norm = target_dir.lower().replace('\\', '/')
        if os.environ.get("PYTEST_CURRENT_TEST") or "tmp" in norm or "temp" in norm or "mock" in norm:
            return

        real_exe = os.path.join(target_dir, "Antigravity.exe")
        ps_code = f"""
        $wsh = New-Object -ComObject WScript.Shell
        $paths = @(
            [System.IO.Path]::Combine([System.Environment]::GetFolderPath('Desktop'), 'Antigravity.lnk'),
            [System.IO.Path]::Combine([System.Environment]::GetFolderPath('CommonDesktop'), 'Antigravity.lnk'),
            [System.IO.Path]::Combine([System.Environment]::GetFolderPath('StartMenu'), 'Programs', 'Antigravity.lnk'),
            [System.IO.Path]::Combine([System.Environment]::GetFolderPath('CommonStartMenu'), 'Programs', 'Antigravity.lnk')
        )
        foreach ($p in $paths) {{
            if (Test-Path $p) {{
                $sc = $wsh.CreateShortcut($p)
                $sc.TargetPath = '{real_exe}'
                $sc.IconLocation = '{real_exe},0'
                $sc.WorkingDirectory = '{target_dir}'
                $sc.Save()
            }}
        }}
        """
        try:
            subprocess.run(['powershell', '-NoProfile', '-Command', ps_code], capture_output=True)
            print("  [OK] Desktop shortcuts restored to original Antigravity.exe.")
        except Exception:
            pass

    @classmethod
    def deploy_permanent_engine(cls, target_dir: str, install_shortcuts: bool = False):
        """Deploys patcher engine files to AppData and target installation resources."""
        if sys.platform != "win32":
            return
        norm = target_dir.lower().replace('\\', '/')
        if os.environ.get("PYTEST_CURRENT_TEST") or "tmp" in norm or "temp" in norm or "mock" in norm:
            return

        core_dir = os.path.dirname(os.path.abspath(__file__))
        pkg_dir = os.path.dirname(core_dir)       # .../src/antigravity_rtl
        src_dir = os.path.dirname(pkg_dir)        # .../src
        root_dir = os.path.dirname(src_dir) if os.path.basename(src_dir).lower() == "src" else src_dir

        files_to_copy = [
            (os.path.join(src_dir, "patcher.py"), "patcher.py"),
            (os.path.join(src_dir, "patcher.js"), "patcher.js"),
            (os.path.join(src_dir, "antigravity-chat-rtl.css"), "antigravity-chat-rtl.css"),
            (os.path.join(root_dir, "patch.bat"), "patch.bat")
        ]

        target_dirs = [
            os.path.join(os.environ.get("APPDATA", ""), "Antigravity", "rtl-patch"),
            os.path.join(target_dir, "resources", "rtl-patch")
        ]

        for tdir in target_dirs:
            try:
                os.makedirs(tdir, exist_ok=True)
                for src_f, fname in files_to_copy:
                    if os.path.isfile(src_f):
                        shutil.copy2(src_f, os.path.join(tdir, fname))
                # Copy entire package directory
                dest_pkg = os.path.join(tdir, "antigravity_rtl")
                if os.path.isdir(pkg_dir):
                    shutil.copytree(pkg_dir, dest_pkg, dirs_exist_ok=True)
            except Exception:
                pass

        launcher_src = os.path.join(src_dir, "AntigravityLauncher.exe")
        if not os.path.isfile(launcher_src):
            launcher_src = os.path.join(root_dir, "AntigravityLauncher.exe")

        if os.path.isfile(launcher_src) and install_shortcuts:
            cls.setup_shortcuts(target_dir, launcher_src)

    @classmethod
    def wait_for_update_then_patch(cls, patcher_instance):
        """Watches for background updater execution and reapplies patch once update finishes."""
        target_dir = patcher_instance.target_dir
        asar_path = patcher_instance.asar_path
        init_mtime = os.path.getmtime(asar_path) if os.path.isfile(asar_path) else 0

        for _ in range(45):
            time.sleep(2)
            try:
                res = subprocess.run(['tasklist'], capture_output=True, text=True)
                out = res.stdout.lower()
                if 'installer.exe' in out or 'setup.exe' in out:
                    for _ in range(60):
                        time.sleep(2)
                        res2 = subprocess.run(['tasklist'], capture_output=True, text=True)
                        if 'installer.exe' not in res2.stdout.lower() and 'setup.exe' not in res2.stdout.lower():
                            break
                    break
                if os.path.isfile(asar_path):
                    curr_mtime = os.path.getmtime(asar_path)
                    if curr_mtime != init_mtime:
                        break
            except Exception:
                pass

        time.sleep(3)
        patcher_instance.patch(kill=False, install_shortcuts=False)

    @classmethod
    def sync_live_window(cls, action: str = "restore") -> bool:
        """DevTools CDP live evaluation helper."""
        try:
            appdata = os.environ.get("APPDATA", "")
            port_file = os.path.join(appdata, "Antigravity", "DevToolsActivePort")
            if not os.path.isfile(port_file):
                return False

            with open(port_file, "r", encoding="utf-8") as f:
                port = f.readline().strip()

            import urllib.request
            import json

            req = urllib.request.Request(f"http://127.0.0.1:{port}/json")
            with urllib.request.urlopen(req, timeout=1.5) as resp:
                targets = json.loads(resp.read().decode("utf-8"))

            pages = [p for p in targets if p.get("type") == "page" and "webSocketDebuggerUrl" in p]
            if not pages:
                return False

            if action == "restore":
                js_code = """(() => {
                    let override = document.getElementById('ag-rtl-disable-override');
                    if (!override) {
                        override = document.createElement('style');
                        override.id = 'ag-rtl-disable-override';
                        document.head.appendChild(override);
                    }
                    override.textContent = `
                        #ag-appearance-menu-container,
                        #ag-appearance-menu-btn,
                        #ag-appearance-popover {
                            display: none !important;
                            visibility: hidden !important;
                            pointer-events: none !important;
                        }
                    `;
                    const c = document.getElementById('ag-appearance-menu-container');
                    if (c) c.remove();
                    const btn = document.getElementById('ag-appearance-menu-btn');
                    if (btn) btn.remove();
                    const pop = document.getElementById('ag-appearance-popover');
                    if (pop) pop.remove();
                    const style = document.getElementById('antigravity-chat-rtl-style');
                    if (style) style.remove();
                    document.documentElement.classList.remove('ag-rtl-enabled');
                    document.documentElement.classList.add('ag-rtl-disabled');
                    document.querySelectorAll('[dir="rtl"]').forEach(el => el.removeAttribute('dir'));
                    return true;
                })()"""
            else:
                from .injector import CodeInjector
                js_code = CodeInjector.get_client_injection()

            try:
                import asyncio
                import websockets

                async def eval_page(ws_url, code):
                    async with websockets.connect(ws_url, max_size=None) as ws:
                        msg = {
                            "id": 1,
                            "method": "Runtime.evaluate",
                            "params": {"expression": code, "returnByValue": True}
                        }
                        await ws.send(json.dumps(msg))
                        await ws.recv()

                for page in pages:
                    asyncio.run(eval_page(page["webSocketDebuggerUrl"], js_code))
                return True
            except Exception:
                return False
        except Exception:
            return False
