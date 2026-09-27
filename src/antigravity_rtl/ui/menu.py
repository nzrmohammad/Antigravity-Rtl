#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Antigravity RTL - Interactive Terminal Menu (OOP)
Presents telemetry dashboards, handles user input, and triggers patching operations.
"""

import os
import sys
import time
from typing import Optional

from .terminal import TerminalUI
from ..constants import (
    CLR_RESET, CLR_BOLD, CLR_DIM, CLR_CYAN,
    CLR_GREEN, CLR_YELLOW, CLR_RED, CLR_WHITE, CLR_GRAY
)
from ..core.patcher import AntigravityPatcher
from ..core.process import ProcessManager


class InteractiveMenu:
    """
    Object-Oriented Interactive Console CLI for Antigravity RTL.
    """

    def __init__(self, patcher: AntigravityPatcher):
        self.patcher = patcher

    def show_diagnostics(self):
        """Displays system health and diagnostics card."""
        diag = self.patcher.diagnostics()
        target_dir = diag["target_dir"]
        short_p = target_dir if len(target_dir) <= 40 else "..." + target_dir[-37:]

        diag_lines = [
            "",
            f"  \033[44;97;1m PATH \033[0m   Installation   : \033[37m{short_p}\033[0m",
            f"  \033[42;30;1m ASAR \033[0m   Package State  : \033[92;1m{'Found & Valid' if diag['asar_exists'] else 'Not Found'}\033[0m",
            f"  \033[46;30;1m BACK \033[0m   Factory Backup : \033[96;1m{'Healthy (app.asar.original_backup)' if diag['backup_exists'] else 'Not Found'}\033[0m",
            f"  \033[45;97;1m RTL  \033[0m   Patch Engine   : \033[95;1m{'ACTIVE (Patched)' if diag['is_patched'] else 'INACTIVE (Original)'}\033[0m",
            f"  \033[42;30;1m SHLD \033[0m   Auto-Shield    : \033[92;1m{'ACTIVE (Protected against updates)' if diag['shield_active'] else 'INACTIVE'}\033[0m",
            f"  \033[43;30;1m PROC \033[0m   Process State  : \033[93;1m{'RUNNING' if diag['is_running'] else 'CLOSED'}\033[0m",
            f"  \033[47;30;1m SYNC \033[0m   DevTools CDP   : \033[97;1m{'Connected (Ready)' if diag['cdp_active'] else 'Inactive (restart Antigravity to enable)'}\033[0m",
            ""
        ]
        print()
        print(TerminalUI.render_shadow_card("DIAGNOSTICS & SYSTEM HEALTH", diag_lines, width=98, border_color="\033[38;2;0;242;254m"))

    def run(self):
        """Runs the main interactive menu loop."""
        while True:
            TerminalUI.clear_screen()
            TerminalUI.print_banner()

            is_patched, is_running = self.patcher.get_status()

            if is_patched:
                status_pill = "\033[42;30;1m PATCHED \033[0m   RTL Engine    : \033[92;1mActive (Smart RTL & Persian Typography)\033[0m"
            else:
                status_pill = "\033[43;30;1m ORIGINAL \033[0m  RTL Engine    : \033[93;1mStock (Standard LTR Mode)\033[0m"

            if is_running:
                proc_pill = "\033[46;30;1m ONLINE \033[0m    Process State : \033[96;1mRunning\033[0m"
            else:
                proc_pill = "\033[100;37;1m CLOSED \033[0m    Process State : \033[90mOffline (Changes apply on start)\033[0m"

            target_dir = self.patcher.target_dir
            short_dir = target_dir if len(target_dir) <= 46 else "..." + target_dir[-43:]
            path_pill = f"\033[44;97;1m TARGET \033[0m    Install Path  : \033[90m{short_dir}\033[0m"

            status_lines = [
                "",
                f"  {status_pill}",
                f"  {proc_pill}",
                f"  {path_pill}",
                ""
            ]

            action_lines = [
                "",
                f"  \033[42;30;1m  1  \033[0m   \033[97;1mInstall Smart RTL (Safe Default - Shortcuts Preserved)\033[0m   \033[96m>> [SAFE INSTALL]\033[0m",
                "",
                f"  \033[43;30;1m  2  \033[0m   \033[97;1mRestore 100% Factory Original State\033[0m                      \033[93m<< [FACTORY REVERT]\033[0m",
                "",
                f"  \033[44;97;1m  3  \033[0m   \033[97;1mInstall Smart RTL + Auto-Shield Shortcuts (Opt-in)\033[0m       \033[94m++ [SHIELD & SHORTCUTS]\033[0m",
                "",
                f"  \033[45;97;1m  4  \033[0m   \033[97;1mSystem Diagnostics & Health Check\033[0m                        \033[95m== [HEALTH CHECK]\033[0m",
                "",
                f"  \033[41;97;1m  0  \033[0m   \033[97;1mExit Patcher\033[0m                                             \033[90m-- [EXIT]\033[0m",
                ""
            ]

            print(TerminalUI.render_shadow_card("SYSTEM TELEMETRY", status_lines, width=98, border_color="\033[38;2;0;242;254m"))
            print(TerminalUI.render_shadow_card("ACTIONS & COMMANDS", action_lines, width=98, border_color="\033[38;2;0;242;254m"))
            print()

            try:
                choice = input(f"  \033[38;2;0;242;254m-->\033[0m {CLR_WHITE}Select action [1, 2, 3, 4, 0] (Default: 1 - Safe Install): {CLR_RESET}").strip().replace('\ufeff', '')
                for p_digit, e_digit in [('۰', '0'), ('۱', '1'), ('۲', '2'), ('۳', '3'), ('۴', '4'), ('۵', '5'), ('۶', '6')]:
                    choice = choice.replace(p_digit, e_digit)
                if not choice:
                    choice = "1"
            except (KeyboardInterrupt, EOFError):
                print(f"\n{CLR_GREEN}Operation cancelled.{CLR_RESET}\n")
                break
            except Exception:
                choice = "1"

            restart_app = False
            if is_running and choice in ["1", "2", "3"]:
                print(f"\n  {CLR_YELLOW}[!] Antigravity is currently running.{CLR_RESET}")
                try:
                    ans = input(f"  {CLR_WHITE}Restart Antigravity now to apply changes immediately? [y/N]: {CLR_RESET}").strip().lower()
                    restart_app = ans in ["y", "yes"]
                except (KeyboardInterrupt, EOFError):
                    restart_app = False

                if restart_app:
                    ProcessManager.close()

            if choice == "1":
                print(f"\n{CLR_CYAN}[*] Installing Smart RTL (Safe Mode - Preserving shortcuts)...{CLR_RESET}")
                self.patcher.patch(kill=False, install_shortcuts=False)
                if restart_app:
                    ProcessManager.launch(self.patcher.target_dir)
                TerminalUI.pause()
            elif choice == "2":
                print(f"\n{CLR_YELLOW}[*] Restoring 100% factory original state and removing shield...{CLR_RESET}")
                self.patcher.restore(kill=False)
                if restart_app:
                    ProcessManager.launch(self.patcher.target_dir)
                TerminalUI.pause()
            elif choice == "3":
                print(f"\n{CLR_CYAN}[*] Installing Smart RTL + Auto-Shield & Desktop Shortcuts...{CLR_RESET}")
                self.patcher.patch(kill=False, install_shortcuts=True)
                if restart_app:
                    ProcessManager.launch(self.patcher.target_dir)
                TerminalUI.pause()
            elif choice == "4":
                self.show_diagnostics()
                TerminalUI.pause()
            elif choice in ["0", "exit", "quit", "q"]:
                print(f"\n{CLR_GREEN}Goodbye!{CLR_RESET}\n")
                break
            else:
                print(f"{CLR_RED}Invalid choice.{CLR_RESET}")
                time.sleep(1)
