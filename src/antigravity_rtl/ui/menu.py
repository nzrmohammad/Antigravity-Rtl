#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Antigravity RTL - Interactive Terminal Menu (OOP)
Presents telemetry dashboards, handles user input, and triggers patching operations.
"""

import time

from .terminal import TerminalUI
from ..constants import (
    CLR_RESET, CLR_CYAN,
    CLR_GREEN, CLR_YELLOW, CLR_RED, CLR_WHITE,
    logger
)
from ..core.patcher import AntigravityPatcher
from ..core.process import ProcessManager
from ..core.proxy import ProxyManager


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

        p_inst = diag.get("proxy_installed", False)
        p_cfg = diag.get("proxy_config") or {}
        p_obj = p_cfg.get("proxy", {})
        p_desc = f"{p_obj.get('type', 'socks5').upper()} {p_obj.get('host', '127.0.0.1')}:{p_obj.get('port', 10808)}" if p_inst else "Not Installed"

        diag_lines = [
            "",
            f"  \033[44;97;1m PATH \033[0m   Installation   : \033[37m{short_p}\033[0m",
            f"  \033[42;30;1m ASAR \033[0m   Package State  : \033[92;1m{'Found & Valid' if diag['asar_exists'] else 'Not Found'}\033[0m",
            f"  \033[46;30;1m BACK \033[0m   Factory Backup : \033[96;1m{'Healthy (app.asar.original_backup)' if diag['backup_exists'] else 'Not Found'}\033[0m",
            f"  \033[45;97;1m RTL  \033[0m   Patch Engine   : \033[95;1m{'ACTIVE (Patched)' if diag['is_patched'] else 'INACTIVE (Original)'}\033[0m",
            f"  \033[42;30;1m SHLD \033[0m   Auto-Shield    : \033[92;1m{'ACTIVE (Protected against updates)' if diag['shield_active'] else 'INACTIVE'}\033[0m",
            f"  \033[44;97;1m PROX \033[0m   Proxy Shield   : \033[96;1m{'ACTIVE (' + p_desc + ')' if p_inst else 'NOT INSTALLED'}\033[0m",
            f"  \033[43;30;1m PROC \033[0m   Process State  : \033[93;1m{'RUNNING' if diag['is_running'] else 'CLOSED'}\033[0m",
            f"  \033[47;30;1m SYNC \033[0m   DevTools CDP   : \033[97;1m{'Connected (Ready)' if diag['cdp_active'] else 'Inactive (restart Antigravity to enable)'}\033[0m",
            ""
        ]
        print()
        print(TerminalUI.render_shadow_card("DIAGNOSTICS & SYSTEM HEALTH", diag_lines, width=98, border_color="\033[38;2;0;242;254m"))

    def handle_proxy_menu(self):
        """Interactive proxy configuration and port test wizard."""
        target_dir = self.patcher.target_dir
        is_inst = ProxyManager.is_installed(target_dir)
        cfg = ProxyManager.read_config(target_dir) or {}
        p_info = cfg.get("proxy", {})
        cur_host = p_info.get("host", "127.0.0.1")
        cur_port = p_info.get("port", 10808)
        cur_type = p_info.get("type", "socks5")

        while True:
            TerminalUI.clear_screen()
            TerminalUI.print_banner()

            status_txt = f"\033[92;1mInstalled\033[0m ({cur_type.upper()} {cur_host}:{cur_port})" if is_inst else "\033[90mNot Installed (version.dll absent)\033[0m"
            card_lines = [
                "",
                f"  Current Status : {status_txt}",
                f"  Target Endpoint: {cur_host}:{cur_port} ({cur_type.upper()})",
                "",
                "  \033[42;30;1m 1 \033[0m  \033[97;1mTest Proxy Connection (Port Listening Check & Latency)\033[0m",
                "  \033[44;97;1m 2 \033[0m  \033[97;1mEnable / Install Proxy Shield (version.dll + config.json)\033[0m",
                "  \033[46;30;1m 3 \033[0m  \033[97;1mSelect Quick Preset (Clash 7890/7897, v2rayN 10808/10809, Sing-box 2080)\033[0m",
                "  \033[41;97;1m 4 \033[0m  \033[97;1mDisable / Uninstall Proxy Shield\033[0m",
                "  \033[100;37;1m 0 \033[0m  \033[90mBack to Main Menu\033[0m",
                ""
            ]
            print(TerminalUI.render_shadow_card("ANTI-SANCTION & PROXY SHIELD", card_lines, width=98, border_color="\033[38;2;0;242;254m"))
            print()

            try:
                sub = input(f"  \033[38;2;0;242;254m-->\033[0m {CLR_WHITE}Select option [1-4, 0] (Default: 1 - Test Port): {CLR_RESET}").strip()
            except (KeyboardInterrupt, EOFError):
                break

            if not sub or sub == "1":
                print(f"\n{CLR_CYAN}[*] Testing connection to {cur_host}:{cur_port} ({cur_type.upper()})...{CLR_RESET}")
                ok, lat, msg = ProxyManager.test_connection(cur_host, cur_port, proxy_type=cur_type)
                if ok:
                    print(f"  \033[92;1m[OK] {msg}\033[0m")
                else:
                    print(f"  \033[91;1m[-] {msg}\033[0m")
                TerminalUI.pause()
            elif sub == "2":
                try:
                    h = input(f"  Enter Proxy Host [Default: {cur_host}]: ").strip() or cur_host
                    p_raw = input(f"  Enter Proxy Port [Default: {cur_port}]: ").strip()
                    p = int(p_raw) if p_raw.isdigit() else cur_port
                    t = input(f"  Enter Proxy Type (socks5/http) [Default: {cur_type}]: ").strip().lower() or cur_type
                except (KeyboardInterrupt, EOFError):
                    continue

                print(f"\n{CLR_CYAN}[*] Installing Proxy Shield into {target_dir}...{CLR_RESET}")
                if ProxyManager.install(target_dir, host=h, port=p, proxy_type=t):
                    print("  \033[92;1m[OK] Proxy Shield installed successfully!\033[0m")
                    is_inst = True
                    cur_host, cur_port, cur_type = h, p, t
                    ok, lat, msg = ProxyManager.test_connection(h, p, proxy_type=t)
                    print(f"  {'[OK]' if ok else '[-]'} {msg}")
                else:
                    print("  \033[91;1m[-] Failed installing Proxy Shield.\033[0m")
                TerminalUI.pause()
            elif sub == "3":
                print("\n  Available Presets:")
                print("    1) Clash / Mihomo (SOCKS5: 127.0.0.1:7890)")
                print("    2) Clash Meta (SOCKS5: 127.0.0.1:7897)")
                print("    3) v2rayN (SOCKS5: 127.0.0.1:10808)")
                print("    4) v2rayN HTTP (HTTP: 127.0.0.1:10809)")
                print("    5) Sing-box (SOCKS5: 127.0.0.1:2080)")
                try:
                    choice_p = input("  Select preset [1-5]: ").strip()
                except (KeyboardInterrupt, EOFError):
                    continue

                preset_map = {
                    "1": ("127.0.0.1", 7890, "socks5"),
                    "2": ("127.0.0.1", 7897, "socks5"),
                    "3": ("127.0.0.1", 10808, "socks5"),
                    "4": ("127.0.0.1", 10809, "http"),
                    "5": ("127.0.0.1", 2080, "socks5"),
                }
                if choice_p in preset_map:
                    h, p, t = preset_map[choice_p]
                    cur_host, cur_port, cur_type = h, p, t
                    ProxyManager.install(target_dir, host=h, port=p, proxy_type=t)
                    is_inst = True
                    print(f"\n  \033[92;1m[OK] Configured for {h}:{p} ({t.upper()})\033[0m")
                    ok, lat, msg = ProxyManager.test_connection(h, p, proxy_type=t)
                    print(f"  {'[OK]' if ok else '[-]'} {msg}")
                TerminalUI.pause()
            elif sub == "4":
                ProxyManager.uninstall(target_dir)
                is_inst = False
                print("\n  \033[92;1m[OK] Proxy Shield uninstalled.\033[0m")
                TerminalUI.pause()
            elif sub in ["0", "b", "back", "exit"]:
                break

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

            target_dir = self.patcher.target_dir
            proxy_installed = ProxyManager.is_installed(target_dir)
            if proxy_installed:
                cfg = ProxyManager.read_config(target_dir) or {}
                p_info = cfg.get("proxy", {})
                p_str = f"{p_info.get('type', 'socks5').upper()} {p_info.get('host', '127.0.0.1')}:{p_info.get('port', 10808)}"
                proxy_pill = f"\033[42;30;1m PROXY \033[0m    Proxy Shield  : \033[92;1mActive ({p_str})\033[0m"
            else:
                proxy_pill = "\033[100;37;1m PROXY \033[0m    Proxy Shield  : \033[90mNot Installed (Opt-in)\033[0m"

            if is_running:
                proc_pill = "\033[46;30;1m ONLINE \033[0m    Process State : \033[96;1mRunning\033[0m"
            else:
                proc_pill = "\033[100;37;1m CLOSED \033[0m    Process State : \033[90mOffline (Changes apply on start)\033[0m"

            short_dir = target_dir if len(target_dir) <= 46 else "..." + target_dir[-43:]
            path_pill = f"\033[44;97;1m TARGET \033[0m    Install Path  : \033[90m{short_dir}\033[0m"

            status_lines = [
                "",
                f"  {status_pill}",
                f"  {proxy_pill}",
                f"  {proc_pill}",
                f"  {path_pill}",
                ""
            ]

            action_lines = [
                "",
                "  \033[42;30;1m  1  \033[0m   \033[97;1mInstall Smart RTL (Safe Default - Shortcuts Preserved)\033[0m   \033[96m>> [SAFE INSTALL]\033[0m",
                "",
                "  \033[43;30;1m  2  \033[0m   \033[97;1mRestore 100% Factory Original State\033[0m                      \033[93m<< [FACTORY REVERT]\033[0m",
                "",
                "  \033[44;97;1m  3  \033[0m   \033[97;1mInstall Smart RTL + Auto-Shield Shortcuts (Opt-in)\033[0m       \033[94m++ [SHIELD & SHORTCUTS]\033[0m",
                "",
                "  \033[45;97;1m  4  \033[0m   \033[97;1mSystem Diagnostics & Health Check\033[0m                        \033[95m== [HEALTH CHECK]\033[0m",
                "",
                "  \033[46;30;1m  5  \033[0m   \033[97;1mAnti-Sanction & Proxy Shield (Test & Configure)\033[0m        \033[96m** [PROXY SHIELD]\033[0m",
                "",
                "  \033[41;97;1m  0  \033[0m   \033[97;1mExit Patcher\033[0m                                             \033[90m-- [EXIT]\033[0m",
                ""
            ]

            print(TerminalUI.render_shadow_card("SYSTEM TELEMETRY", status_lines, width=98, border_color="\033[38;2;0;242;254m"))
            print(TerminalUI.render_shadow_card("ACTIONS & COMMANDS", action_lines, width=98, border_color="\033[38;2;0;242;254m"))
            print()

            try:
                choice = input(f"  \033[38;2;0;242;254m-->\033[0m {CLR_WHITE}Select action [1-5, 0] (Default: 1 - Safe Install): {CLR_RESET}").strip().replace('\ufeff', '')
                for p_digit, e_digit in [('۰', '0'), ('۱', '1'), ('۲', '2'), ('۳', '3'), ('۴', '4'), ('۵', '5'), ('۶', '6')]:
                    choice = choice.replace(p_digit, e_digit)
                if not choice:
                    choice = "1"
            except (KeyboardInterrupt, EOFError):
                print(f"\n{CLR_GREEN}Goodbye!{CLR_RESET}\n")
                break
            except Exception as e:
                logger.debug("Menu choice input error: %s", e)
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
            elif choice == "5":
                self.handle_proxy_menu()
            elif choice in ["0", "exit", "quit", "q"]:
                print(f"\n{CLR_GREEN}Goodbye!{CLR_RESET}\n")
                break
            else:
                print(f"{CLR_RED}Invalid choice.{CLR_RESET}")
                time.sleep(1)
