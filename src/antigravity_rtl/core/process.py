#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Antigravity RTL - Process Management Engine (OOP)
Handles detecting running instances, graceful/forceful termination, and app launching across OS platforms.
"""

import os
import sys
import time
import subprocess
from typing import Optional


class ProcessManager:
    """
    Manages Antigravity IDE OS process states and lifecycle.
    """

    PROCESS_NAME_WIN = "Antigravity.exe"
    PROCESS_NAME_POSIX = "antigravity"

    @classmethod
    def is_running(cls) -> bool:
        """Checks if Antigravity is currently running in the background."""
        if sys.platform == "win32":
            try:
                res = subprocess.run(
                    ['tasklist', '/FI', f'IMAGENAME eq {cls.PROCESS_NAME_WIN}'],
                    capture_output=True,
                    text=True
                )
                return cls.PROCESS_NAME_WIN.lower() in res.stdout.lower()
            except Exception:
                return False
        else:
            try:
                res = subprocess.run(
                    ['pgrep', '-i', cls.PROCESS_NAME_POSIX],
                    capture_output=True,
                    text=True
                )
                return res.returncode == 0
            except Exception:
                return False

    @classmethod
    def close(cls, timeout: float = 1.5) -> bool:
        """Terminates running Antigravity processes."""
        print("[*] Closing running Antigravity processes...")
        try:
            if sys.platform == "win32":
                subprocess.run(
                    ['taskkill', '/F', '/IM', cls.PROCESS_NAME_WIN, '/T'],
                    capture_output=True
                )
            else:
                subprocess.run(
                    ['pkill', '-f', '-i', cls.PROCESS_NAME_POSIX],
                    capture_output=True
                )
            time.sleep(timeout)
            return True
        except Exception as e:
            print(f"[-] Failed to terminate process: {e}")
            return False

    @classmethod
    def launch(cls, target_dir: str) -> bool:
        """Launches Antigravity IDE executable."""
        if sys.platform == "darwin":
            app_bundle = target_dir if target_dir.endswith(".app") else os.path.join(target_dir, "..", "..")
            if os.path.isdir(app_bundle):
                print("[*] Launching Antigravity IDE...")
                try:
                    subprocess.Popen(['open', app_bundle], close_fds=True)
                    return True
                except Exception as e:
                    print(f"[-] Failed to launch Antigravity: {e}")
                    return False

        exe_path = os.path.join(target_dir, cls.PROCESS_NAME_WIN if sys.platform == "win32" else cls.PROCESS_NAME_POSIX)
        if os.path.isfile(exe_path):
            print("[*] Launching Antigravity IDE...")
            try:
                subprocess.Popen([exe_path], cwd=target_dir, close_fds=True)
                return True
            except Exception as e:
                print(f"[-] Failed to launch Antigravity: {e}")
                return False

        print(f"[-] Executable not found at {exe_path}")
        return False
