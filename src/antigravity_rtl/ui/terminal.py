#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Antigravity RTL - Terminal UI Engine (OOP)
Handles ANSI color terminal rendering, gradient logos, and glassmorphic shadow cards.
"""

import os
import sys
import ctypes
from ..constants import (
    CLR_RESET, CLR_BOLD, CLR_DIM, CLR_CYAN,
    CLR_GREEN, CLR_YELLOW, CLR_RED, CLR_WHITE, CLR_GRAY,
    APP_NAME
)


class TerminalUI:
    """
    Object-Oriented UI manager for terminal output, banners, and shadow cards.
    """

    _ansi_enabled = False

    @classmethod
    def enable_windows_ansi(cls):
        """Enable Virtual Terminal Processing and UTF-8 encoding on consoles."""
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

        if cls._ansi_enabled:
            return
        if sys.platform == "win32":
            try:
                kernel32 = ctypes.windll.kernel32
                hStdOut = kernel32.GetStdHandle(-11)
                mode = ctypes.c_ulong()
                kernel32.GetConsoleMode(hStdOut, ctypes.byref(mode))
                mode.value |= 4  # ENABLE_VIRTUAL_TERMINAL_PROCESSING
                kernel32.SetConsoleMode(hStdOut, mode)
                cls._ansi_enabled = True
            except Exception:
                pass
        else:
            cls._ansi_enabled = True

    @staticmethod
    def clear_screen():
        """Clears terminal screen."""
        os.system('cls' if os.name == 'nt' else 'clear')

    @staticmethod
    def render_shadow_card(title: str, lines: list, width: int = 94, border_color: str = "\033[38;2;0;242;254m") -> str:
        """
        Renders a glowing, shadowed card box in ANSI terminal.
        Auto-computes width from line content so text NEVER sticks out or overflows.
        """
        import re
        def visible_len(s):
            return len(re.sub(r'\x1b\[[0-9;]*m', '', s))

        c_bord = border_color
        c_title = "\033[97;1m"
        c_dim = "\033[90m"
        c_reset = CLR_RESET

        # Calculate max content length across all lines and title
        max_content_len = max([visible_len(line) for line in lines] + [len(title) + 4, 86])
        # Guarantee card is wide enough for content + padding + borders with breathing room
        computed_width = max(width, max_content_len + 8)

        inner_w = computed_width - 4
        title_disp = f" {title} " if title else ""
        rem_top = max(0, inner_w - len(title_disp))
        l_top = rem_top // 2
        r_top = rem_top - l_top

        top_border = f"{c_bord}┌{'─' * l_top}{c_title}{title_disp}{c_bord}{'─' * r_top}┐{c_reset}"
        bot_border = f"{c_bord}└{'─' * inner_w}┘{c_reset}"

        res = [top_border]
        for line in lines:
            v_len = visible_len(line)
            pad = max(0, inner_w - 2 - v_len)
            res.append(f"{c_bord}│{c_reset}  {line}{' ' * pad}{c_bord}│{c_dim}▒{c_reset}")

        res.append(bot_border + f"{c_dim}▒{c_reset}")
        res.append(f"  {c_dim}{'▀' * inner_w} {c_reset}")
        return "\n".join(res)

    @staticmethod
    def get_gradient_logo() -> str:
        """Generates a cyberpunk gradient ASCII art logo."""
        raw_logo = r"""
     █████╗ ███╗   ██╗████████╗██╗ ██████╗ ██████╗  █████╗ ██╗   ██╗██╗████████╗██╗   ██╗
    ██╔══██╗████╗  ██║╚══██╔══╝██║██╔════╝ ██╔══██╗██╔══██╗██║   ██║██║╚══██╔══╝╚██╗ ██╔╝
    ███████║██╔██╗ ██║   ██║   ██║██║  ███╗██████╔╝███████║██║   ██║██║   ██║    ╚████╔╝ 
    ██╔══██║██║╚██╗██║   ██║   ██║██║   ██║██╔══██╗██╔══██║╚██╗ ██╔╝██║   ██║     ╚██╔╝  
    ██║  ██║██║ ╚████║   ██║   ██║╚██████╔╝██║  ██║██║  ██║ ╚████╔╝ ██║   ██║      ██║   
    ╚═╝  ╚═╝╚═╝  ╚═══╝   ╚═╝   ╚═╝ ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝  ╚═══╝  ╚═╝   ╚═╝      ╚═╝   
        """
        stops = [
            (0, 242, 254),    # Cyan
            (79, 172, 254),   # Neon Sky Blue
            (114, 9, 183),    # Deep Violet
            (247, 37, 133)    # Neon Magenta
        ]

        def interpolate(s, t):
            t = max(0.0, min(1.0, t))
            idx = t * (len(s) - 1)
            i = int(idx)
            if i >= len(s) - 1:
                return s[-1]
            sub = idx - i
            c1, c2 = s[i], s[i + 1]
            return (
                int(c1[0] + (c2[0] - c1[0]) * sub),
                int(c1[1] + (c2[1] - c1[1]) * sub),
                int(c1[2] + (c2[2] - c1[2]) * sub)
            )

        lines = raw_logo.strip('\n').split('\n')
        max_w = max(len(l) for l in lines)
        out = []
        for line in lines:
            line_chars = []
            for col, ch in enumerate(line):
                if ch == ' ':
                    line_chars.append(' ')
                else:
                    t = col / max(1, max_w - 1)
                    r, g, b = interpolate(stops, t)
                    line_chars.append(f"\033[38;2;{r};{g};{b};1m{ch}")
            line_chars.append(CLR_RESET)
            out.append(''.join(line_chars))
        return '\n'.join(out)

    @classmethod
    def print_banner(cls):
        """Prints the main styled banner."""
        cls.enable_windows_ansi()
        try:
            print(cls.get_gradient_logo())
        except Exception:
            print(f"\n{CLR_CYAN}=== {APP_NAME} ==={CLR_RESET}\n")
        try:
            print(f"  {CLR_GRAY}{'─' * 90}{CLR_RESET}")
            print(f"         {CLR_WHITE}{CLR_BOLD}:::  {APP_NAME}  :::{CLR_RESET}\n")
        except Exception:
            print(f"{APP_NAME}\n")

    @staticmethod
    def info(msg: str):
        print(f"  {CLR_CYAN}[*]{CLR_RESET} {msg}")

    @staticmethod
    def success(msg: str):
        print(f"  {CLR_GREEN}[✓]{CLR_RESET} {msg}")

    @staticmethod
    def warning(msg: str):
        print(f"  {CLR_YELLOW}[!]{CLR_RESET} {msg}")

    @staticmethod
    def error(msg: str):
        print(f"  {CLR_RED}[-]{CLR_RESET} {msg}")

    @staticmethod
    def pause(msg: str = "Press Enter to return to main menu..."):
        try:
            input(f"\n{CLR_DIM}{msg}{CLR_RESET}")
        except (KeyboardInterrupt, EOFError):
            pass
