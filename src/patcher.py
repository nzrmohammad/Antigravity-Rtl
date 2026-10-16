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
    except (OSError, ValueError):
        pass
if hasattr(sys.stderr, "reconfigure"):
    try:
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except (OSError, ValueError):
        pass

# Ensure antigravity_rtl package is on sys.path
_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if _SCRIPT_DIR not in sys.path:
    sys.path.insert(0, _SCRIPT_DIR)
_PARENT_DIR = os.path.dirname(_SCRIPT_DIR)
if _PARENT_DIR not in sys.path:
    sys.path.insert(0, _PARENT_DIR)

from antigravity_rtl.core.asar import AsarArchive
from antigravity_rtl.core.detector import PlatformDetector
from antigravity_rtl.core.process import ProcessManager
from antigravity_rtl.core.shield import AutoShieldManager
from antigravity_rtl.core.patcher import AntigravityPatcher
from antigravity_rtl.ui.terminal import TerminalUI
from antigravity_rtl.ui.menu import InteractiveMenu


from antigravity_rtl.cli import main as cli_main

# --- Backward-Compatibility Facade Functions ---
def find_antigravity_path(custom_path=None):
    return PlatformDetector.find_installation(custom_path)

def is_antigravity_running():
    return ProcessManager.is_running()

def close_antigravity():
    return ProcessManager.close()

def launch_antigravity(target_dir):
    return ProcessManager.launch(target_dir)

def do_patch(antigravity_dir, interactive=False, kill=False, install_shortcuts=False, dry_run=False):
    patcher = AntigravityPatcher(antigravity_dir)
    return patcher.patch(kill=kill, install_shortcuts=install_shortcuts, dry_run=dry_run)

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


def main():
    cli_main()


if __name__ == "__main__":
    main()
