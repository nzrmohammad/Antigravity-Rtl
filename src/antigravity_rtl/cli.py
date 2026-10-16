#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Antigravity Smart RTL & Modern Appearance Engine
Unified CLI Orchestrator & Entrypoint (PEP 517/621 Compliant)
"""

import sys
import logging

from .constants import logger
from .core.detector import PlatformDetector
from .core.process import ProcessManager
from .core.patcher import AntigravityPatcher
from .core.shield import AutoShieldManager
from .ui.terminal import TerminalUI
from .ui.menu import InteractiveMenu


def setup_logging(verbose: bool = False):
    """Configures minimal standard-library logging."""
    level = logging.DEBUG if verbose else logging.WARNING
    logging.basicConfig(
        level=level,
        format="[%(asctime)s] [%(levelname)s] %(name)s: %(message)s",
        datefmt="%H:%M:%S"
    )
    logger.setLevel(level)


def main():
    """Main CLI execution flow."""
    # Terminal UTF-8 reconfigure
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        except Exception as e:
            logger.debug("Failed reconfiguring stdout in cli.py: %s", e)
    if hasattr(sys.stderr, "reconfigure"):
        try:
            sys.stderr.reconfigure(encoding="utf-8", errors="replace")
        except Exception as e:
            logger.debug("Failed reconfiguring stderr in cli.py: %s", e)

    TerminalUI.enable_windows_ansi()

    # Parse verbose flag early
    verbose = any(x in sys.argv for x in ["--verbose", "-v"])
    setup_logging(verbose)

    # Help flag
    if any(x in sys.argv for x in ["--help", "-h"]):
        TerminalUI.print_banner()
        print("""Usage: antigravity-rtl [OPTIONS]

Options:
  -a, --apply              Apply Smart RTL patch and typography suite
  -r, --restore            Restore official unpatched pristine state
  -d, --diagnostics        Run deep health check and integrity diagnostics (--diag)
  --dry-run                Simulate patching without modifying files
  -v, --verbose            Enable detailed debug logging
  -p, --path <DIR>         Specify custom Antigravity installation directory
  -s, --shortcuts          Install anti-reversion auto-shield launcher & shortcuts
                           (alias: --install-shortcuts)
  -y, --silent, --yes      Run non-interactively without interactive prompts
  --check-only             Output 1 if patched, 0 if unpatched, then exit immediately
  --wait-for-update        Daemon mode: monitor updater execution and reapply patch
  --no-kill                Do not terminate Antigravity before patching
  --kill                   Force terminate Antigravity before patching
  --launch                 Launch Antigravity after patching/restoring
  -h, --help               Show this help message and exit
""")
        sys.exit(0)

    # Parse dry-run flag
    dry_run = "--dry-run" in sys.argv

    custom_path = None
    for i, arg in enumerate(sys.argv):
        if arg in ["--path", "-p"] and i + 1 < len(sys.argv):
            custom_path = sys.argv[i + 1]

    if "--wait-for-update" in sys.argv:
        target = PlatformDetector.find_installation(custom_path)
        if target:
            patcher = AntigravityPatcher(target)
            AutoShieldManager.wait_for_update_then_patch(patcher)
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
            except Exception as e:
                logger.debug("Manual input interrupted: %s", e)

    if not target_dir:
        print("[-] Error: Cannot proceed without a valid Antigravity installation path.")
        sys.exit(1)

    patcher = AntigravityPatcher(target_dir)

    if any(x in sys.argv for x in ["4", "--diagnostics", "--diag"]):
        TerminalUI.print_banner()
        print(f"[OK] Detected Antigravity path:\n     {target_dir}\n")
        menu = InteractiveMenu(patcher)
        menu.show_diagnostics()
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

    if dry_run:
        TerminalUI.print_banner()
        print(f"[OK] Detected Antigravity path:\n     {target_dir}\n")
        patcher.patch(kill=False, install_shortcuts=install_shortcuts, dry_run=True)
        return

    is_apply = any(x in sys.argv for x in ["1", "--apply", "-a", "--no-kill"]) or is_option_3 or is_silent
    if is_apply or not sys.stdin.isatty():
        TerminalUI.print_banner()
        print(f"[OK] Detected Antigravity path:\n     {target_dir}\n")
        success = patcher.patch(kill=kill, install_shortcuts=install_shortcuts, dry_run=False)
        if success and "--launch" in sys.argv:
            ProcessManager.launch(target_dir)
        return

    menu = InteractiveMenu(patcher)
    menu.run()


if __name__ == "__main__":
    main()
