#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Antigravity RTL - Comprehensive Object-Oriented RTL & Persian Typography Engine
"""

from .constants import VERSION, APP_NAME
from .core.asar import AsarArchive
from .core.detector import PlatformDetector
from .core.process import ProcessManager
from .core.injector import CodeInjector
from .core.shield import AutoShieldManager
from .core.patcher import AntigravityPatcher
from .ui.terminal import TerminalUI
from .ui.menu import InteractiveMenu

__version__ = VERSION
__all__ = [
    "VERSION",
    "APP_NAME",
    "AsarArchive",
    "PlatformDetector",
    "ProcessManager",
    "CodeInjector",
    "AutoShieldManager",
    "AntigravityPatcher",
    "TerminalUI",
    "InteractiveMenu"
]
