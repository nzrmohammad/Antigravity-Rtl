#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Antigravity Smart RTL & Modern Appearance Engine
CLI Entrypoint (Modular Object-Oriented Architecture)
"""

import os
import sys

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
if hasattr(sys.stderr, "reconfigure"):
    try:
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

# Ensure antigravity_rtl package is on sys.path
_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if _SCRIPT_DIR not in sys.path:
    sys.path.insert(0, _SCRIPT_DIR)
_PARENT_DIR = os.path.dirname(_SCRIPT_DIR)
if _PARENT_DIR not in sys.path:
    sys.path.insert(0, _PARENT_DIR)

from antigravity_rtl.constants import VERSION, APP_NAME, CLR_RESET, CLR_GREEN, CLR_WHITE
from antigravity_rtl.core.asar import AsarArchive
from antigravity_rtl.core.detector import PlatformDetector
from antigravity_rtl.core.process import ProcessManager
from antigravity_rtl.core.injector import CodeInjector
from antigravity_rtl.core.shield import AutoShieldManager
from antigravity_rtl.core.patcher import AntigravityPatcher
from antigravity_rtl.ui.terminal import TerminalUI
from antigravity_rtl.ui.menu import InteractiveMenu


# --- Backward-Compatibility Facade Functions ---
def find_antigravity_path(custom_path=None):
    return PlatformDetector.find_installation(custom_path)

def is_antigravity_running():
    return ProcessManager.is_running()

def close_antigravity():
    return ProcessManager.close()

def launch_antigravity(target_dir):
    return ProcessManager.launch(target_dir)

def do_patch(antigravity_dir, interactive=False, kill=False, install_shortcuts=False):
    patcher = AntigravityPatcher(antigravity_dir)
    return patcher.patch(kill=kill, install_shortcuts=install_shortcuts)

def do_restore(antigravity_dir, kill=False):
    patcher = AntigravityPatcher(antigravity_dir)
    return patcher.restore(kill=kill)

def extract_file_from_asar(asar_path, inner_path):
    return AsarArchive(asar_path).extract_file(inner_path)

def get_asar_metadata(asar_path):
    return AsarArchive(asar_path).get_metadata()

def print_banner():
    TerminalUI.print_banner()

def show_diagnostics(target_dir):
    patcher = AntigravityPatcher(target_dir)
    menu = InteractiveMenu(patcher)
    menu.show_diagnostics()

def wait_for_update_then_patch(target_dir):
    patcher = AntigravityPatcher(target_dir)
    AutoShieldManager.wait_for_update_then_patch(patcher)


# --- CLI Entry Point ---
def main():
    TerminalUI.enable_windows_ansi()

    custom_path = None
    for i, arg in enumerate(sys.argv):
        if arg in ["--path", "-p"] and i + 1 < len(sys.argv):
            custom_path = sys.argv[i + 1]

    if "--wait-for-update" in sys.argv:
        target = PlatformDetector.find_installation(custom_path)
        if target:
            wait_for_update_then_patch(target)
        sys.exit(0)

    if "--check-only" in sys.argv:
        target = PlatformDetector.find_installation(custom_path)
        if target:
            patcher = AntigravityPatcher(target)
            is_patched, _ = patcher.get_status()
            print("1" if is_patched else "0")
        else:
            print("0")
        sys.exit(0)

    target_dir = PlatformDetector.find_installation(custom_path)
    if not target_dir:
        if sys.stdin.isatty():
            TerminalUI.print_banner()
            print("[-] Antigravity installation path could not be detected automatically.")
            try:
                inp = input("Please enter Antigravity installation directory manually (or press Enter to exit): ").strip()
                if inp:
                    target_dir = PlatformDetector.find_installation(inp)
            except Exception:
                pass

    if not target_dir:
        print("[-] Error: Cannot proceed without a valid Antigravity installation path.")
        sys.exit(1)

    patcher = AntigravityPatcher(target_dir)

    if any(x in sys.argv for x in ["4", "--diagnostics", "--diag"]):
        TerminalUI.print_banner()
        print(f"[OK] Detected Antigravity path:\n     {target_dir}\n")
        show_diagnostics(target_dir)
        return

    is_option_3 = "3" in sys.argv
    install_shortcuts = any(x in sys.argv for x in ["--install-shortcuts", "--shortcuts", "-s"]) or is_option_3
    no_kill = "--no-kill" in sys.argv
    kill = ("--kill" in sys.argv) and not no_kill
    is_silent = any(x in sys.argv for x in ["-y", "--yes", "--silent"])

    if any(x in sys.argv for x in ["2", "--restore", "-r"]):
        TerminalUI.print_banner()
        print(f"[OK] Detected Antigravity path:\n     {target_dir}\n")
        patcher.restore(kill=kill)
        if "--launch" in sys.argv:
            ProcessManager.launch(target_dir)
        return

    is_apply = any(x in sys.argv for x in ["1", "--apply", "-a", "--no-kill"]) or is_option_3 or is_silent
    if is_apply or not sys.stdin.isatty():
        TerminalUI.print_banner()
        print(f"[OK] Detected Antigravity path:\n     {target_dir}\n")
        success = patcher.patch(kill=kill, install_shortcuts=install_shortcuts)
        if success and "--launch" in sys.argv:
            ProcessManager.launch(target_dir)
        return

    menu = InteractiveMenu(patcher)
    menu.run()


if __name__ == "__main__":
    main()
