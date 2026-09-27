#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Antigravity RTL - Main Patcher Orchestrator (OOP)
Coordinates ASAR inspection, backup retention, code injection, and persistent deployment.
"""

import os
import shutil
from typing import Tuple, Dict, Any, Optional

from .detector import PlatformDetector
from .process import ProcessManager
from .asar import AsarArchive
from .injector import CodeInjector
from .shield import AutoShieldManager


class AntigravityPatcher:
    """
    Main patcher controller for applying and restoring Antigravity Smart RTL.
    """

    def __init__(self, target_dir: str):
        self.target_dir = target_dir
        self.resources_dir = PlatformDetector.resolve_resources_dir(target_dir)
        self.asar_path = os.path.join(self.resources_dir, "app.asar")
        self.backup_path = os.path.join(self.resources_dir, "app.asar.original_backup")
        self.temp_asar = os.path.join(self.resources_dir, "app.asar.patching.tmp")

    def get_status(self) -> Tuple[bool, bool]:
        """Returns (is_patched, is_running)."""
        is_patched = False
        if os.path.isfile(self.asar_path):
            asar = AsarArchive(self.asar_path)
            preload = asar.extract_file("dist/preload.js")
            is_patched = "__ANTIGRAVITY_RTL_INJECTED__" in (preload or "")
        is_running = ProcessManager.is_running()
        return is_patched, is_running

    def patch(self, kill: bool = False, install_shortcuts: bool = False) -> bool:
        """
        Applies Smart RTL patch to target installation.
        """
        if not os.path.isfile(self.asar_path):
            print(f"[-] Error: app.asar not found in {self.asar_path}")
            return False

        if kill and ProcessManager.is_running():
            ProcessManager.close()

        # 1. Metadata check and pristine backup retention
        current_archive = AsarArchive(self.asar_path)
        asar_meta = current_archive.get_metadata()
        backup_archive = AsarArchive(self.backup_path) if os.path.isfile(self.backup_path) else None
        backup_meta = backup_archive.get_metadata() if backup_archive else None

        is_official_update = False
        if asar_meta and not asar_meta["is_patched"]:
            if not backup_meta:
                is_official_update = True
            elif asar_meta["version_tuple"] > backup_meta["version_tuple"]:
                is_official_update = True
            elif asar_meta["version_tuple"] == backup_meta["version_tuple"] and asar_meta["mtime"] > backup_meta["mtime"]:
                is_official_update = True

        if (asar_meta and not asar_meta["is_patched"]) and (is_official_update or not os.path.isfile(self.backup_path)):
            ver_info = f" (v{asar_meta['version_str']})" if asar_meta else ""
            print(f"[*] Updating factory backup with official pristine build{ver_info}...")
            try:
                shutil.copy2(self.asar_path, self.backup_path)
                print(f"  [OK] Factory backup successfully saved:\n      {self.backup_path}")
            except Exception as e:
                print(f"[-] Error creating factory backup: {e}")
                return False
            source_asar = self.backup_path
        elif os.path.isfile(self.backup_path):
            print("  [i] Pristine factory backup already exists.")
            source_asar = self.backup_path
        else:
            source_asar = self.asar_path

        # 2. Extract and prepare replacements
        source_archive = AsarArchive(source_asar)
        preload_code = source_archive.extract_file("dist/preload.js")
        updater_code = source_archive.extract_file("dist/updater.js")
        nsis_code = source_archive.extract_file("node_modules/electron-updater/out/NsisUpdater.js")
        base_code = source_archive.extract_file("node_modules/electron-updater/out/BaseUpdater.js")

        if not preload_code:
            print("[-] Error extracting dist/preload.js from archive.")
            return False

        injection_snippet = CodeInjector.get_client_injection()
        if "/* __ANTIGRAVITY_RTL_INJECTED__ */" in preload_code:
            preload_code = preload_code.split("/* __ANTIGRAVITY_RTL_INJECTED__ */")[0]

        patched_preload = preload_code + "\n" + injection_snippet
        replacements = {"dist/preload.js": patched_preload}

        # 3. Add auto-updater hooks
        hook_body = CodeInjector.get_updater_hook()

        if updater_code and "/* __ANTIGRAVITY_UPDATE_HOOK__ */" not in updater_code:
            replacements["dist/updater.js"] = updater_code.replace(
                "quitAndInstall() {",
                "quitAndInstall() {" + hook_body
            )

        if nsis_code and "/* __ANTIGRAVITY_UPDATE_HOOK__ */" not in nsis_code:
            replacements["node_modules/electron-updater/out/NsisUpdater.js"] = nsis_code.replace(
                "quitAndInstall(",
                "quitAndInstall(isSilent = false, isForceRunAfter = false) {" + hook_body + " return super.quitAndInstall("
            )

        if base_code and "/* __ANTIGRAVITY_UPDATE_HOOK__ */" not in base_code:
            replacements["node_modules/electron-updater/out/BaseUpdater.js"] = base_code.replace(
                "install(isSilent = false, isForceRunAfter = false) {",
                "install(isSilent = false, isForceRunAfter = false) {" + hook_body
            )

        # 4. Reconstruct ASAR
        print("\n[*] Rebuilding and replacing application package (app.asar)...")
        try:
            source_archive.patch_files(self.temp_asar, replacements)
            try:
                shutil.move(self.temp_asar, self.asar_path)
            except Exception:
                with open(self.temp_asar, "rb") as tf:
                    data = tf.read()
                with open(self.asar_path, "r+b") as out:
                    out.seek(0)
                    out.write(data)
                    out.truncate()
                if os.path.exists(self.temp_asar):
                    os.remove(self.temp_asar)

            # Deploy permanent engine and shortcuts
            AutoShieldManager.deploy_permanent_engine(self.target_dir, install_shortcuts=install_shortcuts)

            print("\n" + "=" * 68)
            print("[OK] Smart RTL Successfully Installed!")
            print("=" * 68)
            print("  * Intelligent auto-direction (Persian: RTL | English: LTR)")
            print("  * Modern typography & Appearance menu integrated into top bar")
            print("  * Engine deployed permanently to Antigravity directory")
            if install_shortcuts:
                print("  * Auto-Shield active: Windows shortcuts protected & launcher installed")
            else:
                print("  * Shortcuts preserved: Original Windows shortcuts remain untouched")
            print("=" * 68)

            if ProcessManager.is_running():
                live_ok = AutoShieldManager.sync_live_window("apply")
                if live_ok:
                    print("  [OK] Changes synchronized live into open Antigravity window.")
                else:
                    print("  [!] Restart Antigravity to reflect changes in current window.")

            return True
        except Exception as e:
            print(f"[-] Patch error: {e}")
            if os.path.exists(self.temp_asar):
                try:
                    os.remove(self.temp_asar)
                except Exception:
                    pass
            return False

    def restore(self, kill: bool = False) -> bool:
        """
        Restores 100% factory original state from backup.
        """
        backup_path = self.backup_path
        if not os.path.isfile(backup_path):
            alt_backup = os.path.join(self.resources_dir, "app.asar.backup")
            if os.path.isfile(alt_backup):
                backup_path = alt_backup

        if not os.path.isfile(backup_path):
            print(f"[-] Backup file not found: {backup_path}")
            return False

        current_archive = AsarArchive(self.asar_path) if os.path.isfile(self.asar_path) else None
        asar_meta = current_archive.get_metadata() if current_archive else None
        backup_archive = AsarArchive(backup_path)
        backup_meta = backup_archive.get_metadata()

        if asar_meta and backup_meta:
            if asar_meta["version_tuple"] > backup_meta["version_tuple"]:
                print("[-] Warning: The backup belongs to an older version of Antigravity.")
                print(f"    Current application: v{asar_meta['version_str']}")
                print(f"    Outdated backup:     v{backup_meta['version_str']}")
                return False

        if kill and ProcessManager.is_running():
            ProcessManager.close()

        print("[*] Restoring app.asar from factory backup...")
        try:
            try:
                shutil.copy2(backup_path, self.asar_path)
            except Exception:
                with open(backup_path, "rb") as bf:
                    data = bf.read()
                with open(self.asar_path, "r+b") as out:
                    out.seek(0)
                    out.write(data)
                    out.truncate()

            print("\n" + "=" * 65)
            print("[OK] Successfully restored to 100% factory original state.")
            print("=" * 65)

            AutoShieldManager.restore_shortcuts(self.target_dir)

            try:
                launcher_exe = os.path.join(self.target_dir, "AntigravityLauncher.exe")
                if os.path.isfile(launcher_exe):
                    os.remove(launcher_exe)
                res_patch = os.path.join(self.target_dir, "resources", "rtl-patch")
                if os.path.isdir(res_patch):
                    shutil.rmtree(res_patch, ignore_errors=True)
                appdata_patch = os.path.join(os.environ.get("APPDATA", ""), "Antigravity", "rtl-patch")
                if os.path.isdir(appdata_patch):
                    shutil.rmtree(appdata_patch, ignore_errors=True)
            except Exception:
                pass

            if ProcessManager.is_running():
                live_ok = AutoShieldManager.sync_live_window("restore")
                if live_ok:
                    print("  [OK] Changes synchronized live into open Antigravity window.")
                else:
                    print("  [!] Restart Antigravity to reflect changes in current window.")
            return True
        except Exception as e:
            print(f"[-] Restore error: {e}")
            return False

    def diagnostics(self) -> Dict[str, Any]:
        """Gathers system health and telemetry diagnostics."""
        is_patched, is_running = self.get_status()
        port_file = os.path.join(os.environ.get("APPDATA", ""), "Antigravity", "DevToolsActivePort")
        patch_dir_ok = os.path.isdir(os.path.join(os.environ.get("APPDATA", ""), "Antigravity", "rtl-patch"))
        shield_ok = os.path.isfile(os.path.join(self.target_dir, "AntigravityLauncher.exe"))

        return {
            "target_dir": self.target_dir,
            "asar_exists": os.path.isfile(self.asar_path),
            "backup_exists": os.path.isfile(self.backup_path),
            "is_patched": is_patched,
            "is_running": is_running,
            "shield_active": shield_ok and patch_dir_ok,
            "cdp_active": os.path.isfile(port_file)
        }
