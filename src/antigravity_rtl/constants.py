#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Antigravity RTL - Global Constants & Terminal Color Definitions
"""

import logging

VERSION = "1.2.0"
APP_NAME = "Smart RTL & Modern Appearance Engine for Antigravity"

# Standard Library Logger for Antigravity RTL
logger = logging.getLogger("antigravity_rtl")

# ANSI Terminal Color Codes
CLR_RESET = "\033[0m"
CLR_BOLD = "\033[1m"
CLR_DIM = "\033[2m"
CLR_CYAN = "\033[96m"
CLR_GREEN = "\033[92m"
CLR_YELLOW = "\033[93m"
CLR_RED = "\033[91m"
CLR_WHITE = "\033[97m"
CLR_GRAY = "\033[90m"

# Default UI Appearance Settings
DEFAULT_SETTINGS = {
    "rtlEnabled": True,
    "fontFamily": "Vazirmatn",
    "customFont": "",
    "fontSize": 15,
    "lineHeight": 1.75,
    "persianDigits": False,
    "justifyText": False,
    "codeFont": "JetBrains Mono",
    "customCodeFont": "",
    "proxyEnabled": False,
    "proxyType": "socks5",
    "proxyHost": "127.0.0.1",
    "proxyPort": 10808
}

# Proxy Shield Security & Configuration Constants
DEFAULT_PROXY_PORT = 10808
DEFAULT_PROXY_HOST = "127.0.0.1"
DEFAULT_PROXY_TYPE = "socks5"
PROXY_VERSION_DLL_SHA256 = "e7b991d65611cac615d756d6be4f55f0e3856a0d37e98cc8fb4a19ebc655e7cc"

