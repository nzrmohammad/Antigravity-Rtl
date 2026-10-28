# 🚀 Antigravity Smart RTL & Offline Typography Suite

<div align="center">

[![Version: v1.2.0](https://img.shields.io/badge/Version-v1.2.0-blue.svg?style=for-the-badge)](pyproject.toml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg?style=for-the-badge)](LICENSE)
[![Platform: Windows | macOS | Linux](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-0078D6?style=for-the-badge&logo=windows)](https://microsoft.com)
[![Tested on: Antigravity v2.28.0+](https://img.shields.io/badge/Antigravity-v2.28.0+%20Verified-00C853?style=for-the-badge&logo=google)](https://deepmind.google)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Offline Fonts](https://img.shields.io/badge/Embedded%20Fonts-100%25%20Offline-FF6B6B?style=for-the-badge)](fonts/)

**Professional, intelligent bidirectional text direction (RTL/LTR) engine with fully offline embedded Persian typography, modular Object-Oriented architecture, and zero-reflow layout for Google Antigravity IDE.**

---

</div>

## Overview

**Antigravity Smart RTL** transforms the text presentation experience in Google DeepMind's Antigravity IDE. It delivers enterprise-grade right-to-left (RTL) typography for Persian, Arabic, and bilingual environments while rigorously preserving left-to-right (LTR) orientation for source code, terminals, tool panels, thoughts, and technical identifiers.

Engineered for performance and resilience, it features a modular Object-Oriented Architecture (OOP), 100% offline embedded Persian fonts (Vazirmatn, Arad, B Nazanin, Shabnam, Sahel, Samim) and English developer typography (JetBrains Mono, Inter), live hot-reloading via the Chrome DevTools Protocol (CDP), official Electron ASAR binary specification compliance with SHA-256 block integrity verification, and non-destructive shortcut handling.

---

## 📖 Table of Contents

- [Overview](#overview)
- [Prerequisites & System Requirements](#prerequisites--system-requirements)
- [Key Features & Highlights](#key-features--highlights)
  - [Intelligent Bidirectional Engine (Smart RTL)](#-intelligent-bidirectional-engine-smart-rtl-with-70-letter-ratio)
  - [100% Offline Embedded Typography](#-100-offline-embedded-typography-free--open-source)
  - [Custom Font Support & Commercial Font Licensing](#-custom-font-support--commercial-font-licensing)
  - [Persian vs. English Digits Toggle](#-persian-vs-english-digits-toggle-۰-۹-vs-0-9)
  - [Dedicated Monospace Code & Terminal Font Selector](#-dedicated-monospace-code--terminal-font-selector)
  - [Ironclad Technical Isolation](#-ironclad-technical-isolation)
  - [Interactive In-App Appearance Control Center](#-interactive-in-app-appearance-control-center)
  - [Electron 20+ ASAR Binary Compliance & Block SHA-256](#-electron-20-asar-binary-compliance--block-sha-256-integrity)
  - [Live Sync via Chrome DevTools Protocol (CDP)](#-live-sync-via-chrome-devtools-protocol-cdp)
  - [Anti-Sanction & Proxy Shield (Zero-TUN Geo-Bypass)](#-anti-sanction--proxy-shield-zero-tun-geo-bypass--real-time-port-tester)
  - [Safe by Default: Preserved Windows Shortcuts](#-safe-by-default-preserved-windows-shortcuts)
- [Architecture & Project Structure](#architecture--project-structure)
- [Quick Start & Installation](#quick-start--installation)
  - [Option A: Windows (One-Click or CLI)](#option-a-windows-one-click-or-cli)
  - [Option B: macOS & Linux (Shell or Python 3)](#option-b-macos--linux-terminal-script-or-python-3)
  - [Option C: Cross-Platform Node.js](#option-c-cross-platform-nodejs-zero-dependency)
  - [The Interactive Command Center](#the-interactive-command-center)
- [CLI Flags & Options Reference](#cli-flags--options-reference)
- [Keyboard Shortcuts & In-App Controls](#keyboard-shortcuts--in-app-controls)
- [🛡️ Anti-Sanction & Proxy Shield Guide](#-anti-sanction--proxy-shield-bypass-regional-restrictions--400403-errors)
  - [The Problem: Geo-Blocking & Child Process Bypassing](#the-problem-geo-blocking--child-process-bypassing)
  - [The Solution: Native Process-Level DLL Proxying](#the-solution-native-process-level-dll-proxying)
  - [Key Differences from Upstream & Security Hardening](#-key-differences-from-upstream--security-hardening)
  - [What Happens During Updates? (IDE & Proxy Updates)](#-what-happens-during-updates-ide--proxy-updates)
  - [Step-by-Step Usage Guide (In-App GUI, Terminal Menu, CLI)](#step-by-step-usage-guide)
  - [Troubleshooting & FAQ](#troubleshooting--faq)
- [🔄 Does the Patch Apply Automatically After Official Updates?](#-does-the-patch-apply-automatically-after-official-ide-updates)
  - [Default Safe Mode (Manual Re-Patch)](#1-default-safe-mode-manual-re-patch-in-2-seconds)
  - [Auto-Shield Mode (Automated Background Self-Healing)](#2-auto-shield-mode-100-automated-background-self-healing)
- [🔍 Modification & Security Audit Manifest](#-modification--security-audit-manifest)
- [Technical Documentation & ASAR Specification](#technical-documentation--asar-specification)
- [License](#license)

---

## Prerequisites & System Requirements

Before running the patcher, ensure your system meets the following requirements:

| Requirement | Specification | Notes |
|---|---|---|
| **Target Application** | **Google Antigravity IDE (v2.28.0+)** | Verified on modern v2.x builds |
| **Operating System** | Windows 10 / 11 (64-bit), macOS 11+, or Linux | Cross-platform directory & process handling |
| **Runtime Environment** | **Python 3.8+** *OR* **Node.js 16+** | Pure standard library — zero external dependencies |
| **Network** | **100% Offline** | Zero CDN dependencies; all fonts & assets embedded locally |
| **Permissions** | Standard User | Run as standard user without elevated administrative rights |

---

## Key Features & Highlights

### 🎯 Intelligent Bidirectional Engine (Smart RTL with 70% Letter Ratio)
- **Letter-Only Density Ratio**: Strips punctuation, symbols, and digits to analyze purely alphabetical characters. Lines are rendered LTR only if Latin letters constitute $\ge 70\%$ of all letters, guaranteeing that Persian sentences with English terms, package names, or commands remain perfectly aligned to the right.
- **Flawless Bilingual Rendering**: Persian sentences align to the right with proper punctuation placement, while English technical phrases, inline code, and symbols remain perfectly oriented.

### 📦 100% Offline Embedded Typography (Free & Open-Source)
- **Zero Internet / Zero CDN Dependency**: High-quality WOFF2 Persian fonts are embedded directly via Base64 data URIs inside the engine.
- **Bundled Fonts**:
  - **Vazirmatn** (Regular 400, Medium 500, Bold 700) — Default modern sans-serif (OFL)
  - **Arad** (Regular 400, Medium 500, Bold 700) — Modern geometric Persian font (successor to Shabnam, SIL OFL)
  - **B Nazanin** (Regular 400, Bold 700) — Classic standard book typeface
  - **Shabnam** (Regular 400, Bold 700) — Clean geometric typeface (OFL)
  - **Sahel** (Regular 400, Bold 700) — Soft curved modern typeface (OFL)
  - **Samim** (Regular 400, Bold 700) — Friendly open typeface (OFL)
- **Instantaneous Rendering**: Eliminates Flash of Unstyled Text (FOUT), CDN latency, and DNS lookup delays entirely. Works in completely air-gapped or restricted offline environments.

### 🎨 Custom Font Support & Commercial Font Licensing

This suite features a flexible **Custom Font** mechanism that leverages your operating system's locally installed fonts (Windows, macOS, or Linux).

#### 💡 Respecting Commercial Font Licenses & Clean Open-Source:
Popular commercial Persian fonts such as **IRANSans**, **IRANYekan**, and **Dana** are proprietary licensed software. Distributing raw font binaries inside a public open-source repository violates foundry licensing. The **Custom Font** architecture resolves this legally and ethically:
- No proprietary binaries are distributed in the repository.
- If you have legally purchased and installed these fonts on your computer, the engine detects and renders them directly from your local OS font store (`C:\Windows\Fonts`, `/Library/Fonts`, etc.).
- The engine includes built-in alias resolution for common commercial fonts (e.g. typing `IRANSansX`, `IRANYekan`, or `Dana` automatically resolves full font stacks and fallbacks).

#### 🚀 Step-by-Step Custom Font Setup:
1. **Install Font Locally:** Install your licensed font file (`.ttf` or `.otf`) in your OS (e.g., right-click on the font file in Windows and click **Install** or **Install for all users**).
2. **Open Appearance Menu:** In Antigravity's top bar, click the **Appearance** button.
3. **Select Custom Font:** In the `Font Family` dropdown, select **Custom Font...**.
4. **Enter Font Name:** In the input box, type the exact English font name as installed on your system; for example:
   - `Dana`
   - `IRANSansX` or `IRANSans`
   - `IRANYekanX` or `IRANYekan`
   - `B Titr`
   - `Peyda`
   - Or any corporate or custom brand font.
5. **Instant Live Preview & Persistence:** The typography updates instantly in real time and is persistently saved to `localStorage`. If a custom font is unavailable on another machine, the engine gracefully falls back to `Vazirmatn` (Safe Fallback).

### 🔢 Persian vs. English Digits Toggle (۰-۹ vs 0-9)
- **Developer-Friendly Numeral Control**: In coding and bilingual technical environments, keeping numbers in Latin/English digits (`0-9`) is essential to prevent version strings (e.g., `v2.17.0`), port numbers (`localhost:8080`), Git commits, and issue IDs (`#102`) from becoming distorted.
- **One-Click Numeral Switching**: For users preferring pure Persian typography in documentation or chat discussions, toggling **Persian Digits** ON transforms numbers into Persian numerals (`۰-۹`) using standard OpenType stylistic sets (`"ss01"`).

### 💻 Dedicated Monospace Code & Terminal Font Selector
- Enforces strict LTR technical isolation while allowing developers to independently customize the monospace font used in syntax-highlighted code blocks, tool calls, and terminal buffers:
  - **JetBrains Mono** (bundled offline OFL / default developer font)
  - **Consolas** (Windows standard developer monospace)
  - **Fira Code** (renders if installed on system; supports programming ligatures)
  - **Cascadia Code** (Windows built-in / Terminal font)
  - **Vazir Code** (bundled bilingual Persian/English monospace)
  - **Custom Monospace...** (e.g., `Hack`, `Source Code Pro`, `Inconsolata`)
  *(Note: Built-in options indicate availability with `● Bundled`, `● Installed`, or `○ Not installed`.)*

### 🛡️ Ironclad Technical Isolation
- **Preserved Coding Environments**: Strict LTR isolation enforced on:
  - Monaco Editor instances & syntax-highlighted code blocks
  - Integrated terminal buffers and command logs
  - Agent Thought streams, tool invocation cards, and execution metadata
  - Numerical metrics, tabular data, JSON payloads, and Git diffs

### ⚙️ Interactive In-App Appearance Control Center
- **Floating Glassmorphism Toolbar Menu**: Directly accessible from the Antigravity IDE top bar (`Appearance`).
- **Quick Keyboard Shortcut (`Alt+R`)**: Instantly toggle Smart RTL on/off anywhere with an on-screen visual toast HUD.
- **Real-Time Customization**:
  - Toggle Smart RTL on/off in real-time
  - Toggle Persian digits (۰-۹) vs Latin digits (0-9)
  - Toggle Smart Paragraph Justify (`Justify Text`) with natural edge anchoring
  - Live Font Availability Indicators: View immediately which fonts are `● Bundled`, `● Installed`, or `○ Not installed`, with dynamic live feedback badges for custom typed fonts
  - Select between Vazirmatn, Inter, IRANSans, IRANYekan, Dana, Arad, B Nazanin, Shabnam, Sahel, Samim, Tahoma, System, or Custom Font
  - Customize code block monospace typography independently
  - Adjust typography font size (`12px` – `24px`) with instant visual feedback
  - Adjust line height (`Compact 1.5`, `Normal 1.75`, `Relaxed 2.0`)
- **Persistent Preferences**: Automatically saved to `localStorage` and restored across window refreshes and IDE restarts.

### 🔒 Electron 20+ ASAR Binary Compliance & Block SHA-256 Integrity
- High-performance, pure Python binary parser and builder for Electron ASAR format archives.
- Implements the exact 16-byte Electron C++ header specification and automatic 4MB chunked SHA-256 integrity block hashes (`node["integrity"]`), ensuring 100% stability and zero Electron crash loops.
- Automatically preserves an untouched pristine factory backup (`app.asar.original_backup`).
- Version-aware metadata guards and single-click 100% factory revert.

### ⚡ Live Sync via Chrome DevTools Protocol (CDP)
- Detects running Antigravity IDE instances and synchronizes CSS/DOM modifications live into open editor windows without requiring an application restart.

### 🛡️ Anti-Sanction & Proxy Shield (Zero-TUN Geo-Bypass & Real-Time Port Tester)
- **Eliminates HTTP 400 & 403 Sanction Errors**: Seamlessly routes `Antigravity.exe`, `language_server.exe`, and background `node.exe` processes through your local proxy.
- **No TUN Mode & No Admin Privileges Needed**: Uses verified process-level DLL interception (`version.dll`), completely avoiding complicated network adapter configurations or system-wide routing rules.
- **Live Connection & Port Tester**: Test whether your proxy software (Clash, v2rayN, Sing-box) is active on that port right from the UI with real-time millisecond latency measurement.
- **Instant One-Click Presets**: Immediate setup for Clash (`7890`), Clash Meta (`7897`), v2rayN (`10808` / `10809`), and Sing-box (`2080`).

### 🛡️ Safe by Default: Preserved Windows Shortcuts
- **Non-Destructive Execution**: By default, the patcher never modifies your Windows Desktop or Start Menu shortcuts.
- **Opt-in Auto-Shield**: Users who desire automatic background re-patching after official IDE updates can easily opt in using the `--install-shortcuts` flag or interactive menu option 3.

---

## Architecture & Project Structure

The project is structured following clean **Object-Oriented Programming (OOP)** design:

```
antigravity-rtl/
├── fonts/                             # Canonical offline WOFF2 webfonts
│   ├── Vazirmatn-*.woff2
│   ├── Arad-*.woff2                   # Modern geometric font (by MDarvishi5124)
│   ├── IRANSans-*.woff2 & IRANYekan-*.woff2
│   ├── Dana-*.woff2 & B-Nazanin.woff2
│   ├── Shabnam.woff2 & Shabnam-Bold.woff2
│   ├── Sahel.woff2 & Sahel-Bold.woff2
│   └── Samim.woff2 & Samim-Bold.woff2
├── scripts/
│   └── bundle.py                      # Asset bundler (CSS & base64 font synchronizer)
├── src/
│   ├── antigravity_rtl/               # Modular Object-Oriented Package
│   │   ├── bin/                       # Verified native helper binaries & templates
│   │   │   ├── version.dll            # Anti-sanction interception DLL (64-bit C++17)
│   │   │   └── config.template.json   # Process interception schema & targets
│   │   ├── core/
│   │   │   ├── asar.py                # AsarArchive: Electron ASAR parser, builder & SHA256 integrity
│   │   │   ├── detector.py            # PlatformDetector: Cross-platform installation locator
│   │   │   ├── process.py             # ProcessManager: Process lifecycle, launch & safe restart
│   │   │   ├── proxy.py               # ProxyManager: Proxy Shield orchestrator & port tester
│   │   │   ├── injector.py            # CodeInjector: Client-side JS & updater hook generator
│   │   │   ├── shield.py              # AutoShieldManager: Shortcut protection & update daemon
│   │   │   └── patcher.py             # AntigravityPatcher: Core patch orchestrator & restore logic
│   │   ├── ui/
│   │   │   ├── terminal.py            # TerminalUI: Cyberpunk banners & dynamic glowing shadow cards
│   │   │   └── menu.py                # InteractiveMenu: Live telemetry dashboard & command menu
│   │   ├── assets.py                  # Embedded CSS & Base64 offline fonts
│   │   └── constants.py               # Global constants, ANSI colors & default appearance
│   ├── antigravity-chat-rtl.css       # Standalone stylesheet with embedded Base64 fonts
│   ├── patcher.py                     # Backward-compatible Python CLI facade & entrypoint
│   ├── patcher.js                     # Zero-dependency Node.js patch engine
│   ├── AntigravityLauncher.exe        # Optional Auto-Shield background launcher (Windows)
│   └── launcher/                      # Open-source C++ launcher source code & README
├── patch.bat                          # Universal Windows launcher
└── patch.sh                           # Universal macOS & Linux launcher
```

---

## Quick Start & Installation

### Option A: Windows (One-Click or CLI)

**1. One-Click Launcher:**  
Double-click `patch.bat` or run in CMD / PowerShell:
```cmd
patch.bat
```

**2. Modern Python / pipx CLI (Recommended):**  
```bash
# Direct install via pipx (isolated global tool)
pipx install .

# Or editable install in development:
pip install -e .

# Run anywhere in your terminal:
antigravity-rtl
```

**3. Direct Python Script Execution:**  
```powershell
# Standard safe install (shortcuts preserved)
python src/patcher.py

# Safe dry-run simulation (no files modified)
python src/patcher.py --dry-run

# Opt-in: Install with Auto-Shield shortcuts
python src/patcher.py --install-shortcuts

# Restore 100% factory original state
python src/patcher.py --restore

# System health diagnostics
python src/patcher.py --diagnostics
```

---

### Option B: macOS & Linux (Terminal Script or Python 3)

**1. Universal Shell Launcher:**  
Open Terminal in the project root directory and run:
```bash
chmod +x patch.sh
./patch.sh
```

**2. Python 3 CLI:**  
```bash
# Standard safe install
python3 src/patcher.py

# If Antigravity is installed in system directories (e.g. /Applications or /opt):
sudo python3 src/patcher.py

# Restore 100% factory original state
python3 src/patcher.py --restore

# Target custom installation path explicitly
python3 src/patcher.py --path "/Applications/Antigravity.app"
```

---

### Option C: Cross-Platform Node.js (Zero-Dependency)

If you prefer using Node.js on any platform:
```bash
# Standard safe install
node src/patcher.js

# On macOS/Linux with system-wide installs:
sudo node src/patcher.js

# Restore original factory state
node src/patcher.js --restore
```

---

### The Interactive Command Center

When launched in interactive mode, the dashboard displays:
```text
┌───────────────────────────────────── ACTIONS & COMMANDS ─────────────────────────────────────┐
│                                                                                              │▒
│      1     Install Smart RTL (Safe Default - Shortcuts Preserved)   >> [SAFE INSTALL]        │▒
│                                                                                              │▒
│      2     Restore 100% Factory Original State                      << [FACTORY REVERT]      │▒
│                                                                                              │▒
│      3     Install Smart RTL + Auto-Shield Shortcuts (Opt-in)       ++ [SHIELD & SHORTCUTS]  │▒
│                                                                                              │▒
│      4     System Diagnostics & Health Check                        == [HEALTH CHECK]        │▒
│                                                                                              │▒
│      5     Anti-Sanction & Proxy Shield (Test & Configure)          ** [PROXY SHIELD]        │▒
│                                                                                              │▒
│      0     Exit Patcher                                             -- [EXIT]                │▒
│                                                                                              │▒
└──────────────────────────────────────────────────────────────────────────────────────────────┘▒
```

Simply press `Enter` (or type `1`) to apply the patch, or type `5` to open the Proxy Shield setup.

---

## CLI Flags & Options Reference

| Flag | Shorthand | Description |
|---|---|---|
| `--dry-run` | | **Simulation mode**: Validates paths, calculates SHA-256 blocks and prints the exact patch manifest without modifying any files on disk. |
| `--verbose` | `-v` | Enables detailed standard-library debug logs and stack traces for troubleshooting. |
| `--install-shortcuts` | `--shortcuts`, `-s`, `3` | **Opt-in**: Protects desktop & start menu shortcuts using `AntigravityLauncher.exe` for automatic update healing. Default is disabled (safe mode). |
| `--restore` | `-r`, `2` | Fully restores `app.asar` from original factory backup, reverts shortcuts, and uninstalls proxy shield. |
| `--proxy [PORT]` | | **Anti-Sanction Shield**: Enables native DLL proxying and configures host/port (defaults to `10808` or custom `[HOST:]PORT`). |
| `--disable-proxy` | | Disables Proxy Shield and removes `version.dll` and `config.json` from the installation directory. |
| `--test-proxy [PORT]` | | Tests TCP socket connectivity & real-time latency to your local proxy port (exits `0` if active, `1` if closed). |
| `--diagnostics` | `--diag`, `4` | Displays system telemetry, patch status, proxy shield state, live CDP port, and installation health check. |
| `--path <dir>` | `-p <dir>` | Explicitly targets an Antigravity installation path. |
| `--no-kill` | | Applies the patch without closing running Antigravity processes; synchronizes via live CDP. |
| `--kill` | | Forces closing Antigravity IDE processes before patching. |
| `--launch` | | Automatically launches Antigravity IDE upon successful patching. |
| `--check-only` | | Silent check: returns `1` if patched, `0` if original. |
| `--yes` | `-y`, `--silent` | Non-interactive mode: automatically applies patch without prompting. Ideal for CI/CD. |
| `--wait-for-update` | | Background daemon mode: monitors updater processes and re-patches automatically. |

---

## Keyboard Shortcuts & In-App Controls

| Shortcut / Action | Trigger | Functionality |
|---|---|---|
| **Toggle Smart RTL** | `Alt + R` | Instantly switches between Smart RTL and stock LTR mode with visual toast HUD |
| **Appearance Menu** | Top Bar Button (`Appearance`) | Opens floating customization popover for all appearance and typography controls |
| **Proxy Shield Toggle** | In Popover Switch | Enables/disables process-level proxy routing for AI & language servers |
| **Test Connection** | In Popover Button (`⚡ Test`) | Real-time TCP port listening verification with millisecond latency HUD |
| **Proxy Quick Presets** | In Popover Chips | 1-click port selection for Clash (7890/7897), v2rayN (10808/10809), and Sing-box (2080) |
| **Justify Text Toggle** | In Popover Switch | Smart two-sided paragraph alignment (`text-align: justify`) with anchored terminal line edges |
| **Persian Digits Toggle** | In Popover Switch | Toggle between Eastern Arabic/Persian numerals (`۰-۹`) and Latin/English digits (`0-9`) |
| **Font Family** | In Popover Dropdown | Select from Vazirmatn, Inter, Arad, B Nazanin, Shabnam, Sahel, Samim, Tahoma, System, or Custom |
| **Code & Terminal Font** | In Popover Dropdown | Customize code block and terminal monospace font (JetBrains Mono, Consolas, Fira Code, Cascadia Code, Vazir Code, or Custom) |
| **Reset to Default** | In Popover Footer | Instantly restore typography settings to factory default values |

---

## 🛡️ Anti-Sanction & Proxy Shield (Bypass Regional Restrictions & 400/403 Errors)

### The Problem: Geo-Blocking & Child Process Bypassing
Developers working in sanctioned or restricted regions (such as Iran, Russia, China, etc.) routinely encounter blocking and failure modes when communicating with Google AI servers:
* `HTTP 400 Bad Request` or `HTTP 403 Forbidden` errors during model generation or chat queries.
* "Failed to connect to language server" or dead agent thought streams.
* Standard system proxies, PAC files, or browser extensions **fail to resolve the issue** because Google Antigravity spawns background binaries (`language_server.exe`, `agy.exe`, and worker `node.exe`) as detached child processes that bypass Windows WinINet / Internet Options system proxies unless run through an invasive whole-system TUN virtual adapter.

---

### The Solution: Native Process-Level DLL Proxying
Antigravity RTL incorporates an optional, strictly **opt-in** process-level interception shield (modeled after and upstream-verified from the open-source [yuaotian/antigravity-proxy](https://github.com/yuaotian/antigravity-proxy) project, written in C++17 with MinHook and MIT license).

#### How it Works:
1. **DLL Proxying (`version.dll`)**: A 64-bit helper DLL named `version.dll` is placed in Antigravity's root folder right next to `Antigravity.exe`.
2. **Cryptographically Verified (`SHA-256`)**: Before installation, the binary's SHA-256 hash is checked (`e7b991d65611cac615d756d6be4f55f0e3856a0d37e98cc8fb4a19ebc655e7cc`). Any tampered or corrupted binary is immediately rejected.
3. **Strict Opt-In**: The standard RTL typography installation (`Option 1`) **never** touches or copies `version.dll`. It is only deployed when explicitly requested.
4. **Smart Config Merge & Safe Backups**: When enabling or modifying the proxy, existing custom rules (`target_processes`, `proxy_rules`, etc.) are preserved, and an automatic backup (`config.json.bak`) is created before any changes.
5. **Real Protocol Handshake Verification**: The built-in tester performs an authentic SOCKS5 client greeting (`0x05 0x01 0x00`) or HTTP request to verify the actual proxy service rather than assuming an open port is a working proxy.
6. **Transparent Process Interception**: The shield intercepts WinSock TCP/IP socket connections and routes language server and AI requests through your local proxy client (SOCKS5 or HTTP).
7. **Zero Administrative Rights & Zero TUN Requirement**: Does not require Windows Administrator privileges and leaves your regular network adapters untouched.
8. **Completely Removable**: Simply turn off the toggle in the Appearance menu, run `antigravity-rtl --disable-proxy`, or run `antigravity-rtl --restore` to wipe all files cleanly.

---

### 🛡️ Key Differences from Upstream & Security Hardening

The bundled Proxy Shield is based on the open-source [yuaotian/antigravity-proxy](https://github.com/yuaotian/antigravity-proxy) project (MIT License), but has been **extensively sanitized, localized, and security-hardened** specifically for the Antigravity Smart RTL suite:

| Feature / Aspect | Original Upstream Binary | Antigravity Smart RTL Enhanced Version |
|---|---|---|
| **UI Localization** | Hardcoded Chinese dialogs (`MessageBoxW`) | **100% English Localized**: Dialog title and messages rewritten in clear English. |
| **Startup Behavior** | Shows modal dialog box on initial launch (`ui.load_notify: "once"`) | **Silent by Default**: Configured to `ui.load_notify: "none"` so it operates quietly in the background without interrupting the developer. |
| **Supply-Chain Security** | Distributed third-party update mirrors (`wget.la`, `fastgit.cc`) with `allow_insecure_mirrors: true` | **Sanitized & Neutralized**: Auto-updates from remote mirrors disabled (`updates.enabled: false`, `allow_insecure_mirrors: false`, `mirrors: []`) to eliminate supply-chain attack risks. |
| **Default Port Consistency**| Inconsistent defaults across tools (`7890` vs `10808`) | **Unified Port 10808**: Standardized across CLI, interactive menus, config templates, and in-app UI. |
| **Connection Testing** | Simple TCP port probe | **Active Protocol Handshake**: Verifies genuine SOCKS5 greeting negotiation (`0x05 0x01 0x00`) and HTTP proxy response with millisecond latency HUD and visual toast feedback. |
| **Binary Verification** | Unverified file copy | **Cryptographic SHA-256 Pinning**: Strict hash check before copying (`e7b991d65611cac615d756d6be4f55f0e3856a0d37e98cc8fb4a19ebc655e7cc`); tampered files are rejected. |
| **Config Preservation** | Overwritten upon installation | **Smart Non-Destructive Merge**: Automatically creates `config.json.bak` and deep-merges user-defined rules and processes. |
| **Installation Policy** | Often deployed implicitly | **Strictly Opt-In**: Never copied or installed during normal RTL typography patching. |

---

### 🔄 What Happens During Updates? (IDE & Proxy Updates)

#### 1. Official Google Antigravity IDE Updates:
* **Does an IDE update break Proxy Shield?**
  Google Antigravity's official NSIS updater updates `Antigravity.exe` and replaces `resources/app.asar`. 
  Because `config.json` is a user configuration file in the root application folder, **your proxy settings are preserved across updates**.
* If an official installer replaces or removes `version.dll`, simply re-run `antigravity-rtl --proxy` (or toggle Proxy Shield in the in-app Appearance menu). The engine verifies the binary integrity and restores the shield without altering your custom configuration.

#### 2. Upstream Proxy Shield Updates:
* **Why is remote auto-updating disabled?**
  In the original upstream project, automatic updating downloaded binaries from third-party mirrors in China (`wget.la`, `fastgit.cc`). We intentionally neutralized this feature (`updates.enabled: false`) to ensure **zero unexpected remote code execution** or supply-chain contamination on your machine.
* **How are Proxy Shield updates delivered safely?**
  All future improvements, upstream bug fixes, and security enhancements to Proxy Shield are vetted, English-localized, cryptographically hashed, and released through official **Antigravity Smart RTL** releases.
* **Are your custom rules safe when updating?**
  **Yes.** `ProxyManager.install()` uses a non-destructive smart merge: it reads your existing `config.json`, creates a dated backup (`config.json.bak`), and preserves all your custom routing rules (`proxy_rules`), excluded processes (`child_injection_exclude`), and custom ports while updating the core binary.

---

### Step-by-Step Usage Guide

#### Method 1: Using the In-App GUI (Recommended)
1. **Start Your Local Proxy Client**:
   Ensure your local proxy software (e.g., **v2rayN**, **Clash / Mihomo**, **NekoBox**, or **Sing-box**) is running on your machine.
2. **Open Appearance Menu**:
   In Antigravity IDE, click the **Appearance** button in the top title bar.
3. **Enable Proxy Shield**:
   In the **🛡️ Proxy Shield** section, click the toggle switch to **Enabled**. The configuration panel will expand.
4. **Select Protocol & Port**:
   - Choose **SOCKS5 (Best)** (recommended for stability and performance) or **HTTP**.
   - Enter your local proxy host (default: `127.0.0.1`) and port, or simply click one of the **Quick Presets**:
     | Preset Name | Protocol | Host & Port | Common Client |
     |---|---|---|---|
     | **Clash** | SOCKS5 | `127.0.0.1:7890` | Clash for Windows, Mihomo Party, Clash Verge |
     | **Clash Meta** | SOCKS5 | `127.0.0.1:7897` | Clash Verge Rev (Meta default port) |
     | **v2rayN** | SOCKS5 | `127.0.0.1:10808` | v2rayN SOCKS5 inbound (default) |
     | **v2rayN HTTP** | HTTP | `127.0.0.1:10809` | v2rayN HTTP inbound (default) |
     | **Sing-box** | SOCKS5 | `127.0.0.1:2080` | Sing-box GUI / NekoBox |
5. **Test Your Connection (Real-Time Port Check)**:
   Click the **⚡ Test** button. The engine immediately performs a live TCP handshake:
   - ✅ **Active (Green)**: `● Proxy active on 127.0.0.1:10808 (0.4ms)` — Your local proxy is responding and ready.
   - ❌ **Refused (Red)**: `○ Connection refused: No proxy app on port ... (offline)` — Your proxy software is either closed or listening on a different port.
6. **Restart / Reload Antigravity IDE**:
   Changes take effect on application start. All AI communication now routes through your proxy with zero sanction blocks!

---

#### Method 2: Using the Interactive Terminal Menu
1. Launch the patcher:
   ```bash
   antigravity-rtl
   ```
   (or `python src/patcher.py` / double-click `patch.bat`).
2. Type `5` and press `Enter` to access **Anti-Sanction & Proxy Shield**.
3. Use the interactive options:
   - `1` — **Test Proxy Connection**: Tests connectivity to the currently configured host/port with real-time latency feedback.
   - `2` — **Enable / Install Proxy Shield**: Custom configuration for host, port, and protocol.
   - `3` — **Select Quick Preset**: 1-click preset setup for Clash, v2rayN, or Sing-box.
   - `4` — **Disable / Uninstall Proxy Shield**: Removes `version.dll` and `config.json`.
   - `0` — Return to the main menu.

---

#### Method 3: Using Direct CLI Commands
You can test and configure the proxy directly from terminal scripts:
```bash
# 1. Test whether your local proxy is listening on port 10808 (or custom host:port)
antigravity-rtl --test-proxy 10808

# 2. Enable Proxy Shield and configure SOCKS5 on 127.0.0.1:10808
antigravity-rtl --proxy 10808

# 3. Enable Proxy Shield on a custom host and port:
antigravity-rtl --proxy 127.0.0.1:7890

# 4. Disable and remove Proxy Shield:
antigravity-rtl --disable-proxy
```

---

### Troubleshooting & FAQ

#### Q: The connection test reports "Connection refused: No proxy app on port ..."?
* **Cause**: No application on your computer is listening on that port.
* **Fix**: Ensure your VPN/proxy client (v2rayN, Clash, Sing-box) is actively running and connected. Verify the inbound port in your client's settings (e.g. in v2rayN bottom status bar: `SOCKS: 10808, HTTP: 10809`).

#### Q: Does Proxy Shield require administrative privileges?
* **No**. `version.dll` resides directly within your user-level application folder (`%LOCALAPPDATA%\Programs\antigravity`). It does not install drivers, services, or registry hooks.

#### Q: How do I completely uninstall Proxy Shield?
* Simply toggle the switch to **Disabled** in the in-app menu, run `antigravity-rtl --disable-proxy`, or perform a full factory reset with `antigravity-rtl --restore`. Both `version.dll` and `config.json` will be deleted cleanly.

---

## 🔄 Does the Patch Apply Automatically After Official IDE Updates?

A common question is how the patch behaves when Google Antigravity IDE installs an official update. The system offers two clean modes depending on your workflow:

### 1. Default Safe Mode (Manual Re-Patch in 2 Seconds)
* **What happens during an official update?**
  When Antigravity IDE auto-updates, the Electron installer completely replaces the internal `resources/app.asar` archive with a fresh, stock binary. Consequently, the injected RTL scripts are replaced by the factory files.
* **Are your customizations lost?**
  **No.** All your personalized settings (chosen Persian and monospace code fonts, font size, line spacing, Persian digits, and Justify alignment) are permanently stored in your OS user profile via `localStorage`. They are never wiped by official application updates.
* **How to re-enable:**
  Simply re-run the patcher once after the update completes:
  ```bash
  python -m antigravity_rtl.cli
  ```
  or double-click `patch.bat`. The engine verifies the new version, creates a fresh pristine backup, and re-applies the full RTL suite in under 2 seconds.

### 2. Auto-Shield Mode (100% Automated Background Self-Healing)
If you prefer zero maintenance and want the patch to **automatically survive every update without running commands manually**, enable **Auto-Shield**:

* **How to enable:**
  Run the CLI with `--install-shortcuts` (or select Option `3` in the interactive menu):
  ```bash
  python -m antigravity_rtl.cli --install-shortcuts
  ```
* **How it works:**
  1. **Persistent Engine Deployment:** The patcher core, scripts, and font assets are mirrored to your user profile directory (`%APPDATA%\Antigravity\rtl-patch`), keeping them safe from application uninstalls or version upgrades.
  2. **Lightweight Native C++ Launcher:** A zero-window binary (`AntigravityLauncher.exe`) is placed in the installation directory, and your Desktop / Start Menu shortcuts are cleanly redirected to it.
  3. **Silent Self-Healing on Launch:** Whenever you launch Antigravity, the launcher instantly checks if an official update has replaced `app.asar`. If an unpatched binary is detected, it quietly applies the patch in the background without terminal popups or interruption, then starts the IDE with your full RTL typography ready to go.

---

## 🔍 Modification & Security Audit Manifest

Because this tool patches internal application packages, total operational transparency and user data integrity are core design priorities. Below is an exhaustive audit of every file read, created, or modified during the patching lifecycle:

1. **Factory Pristine Backup (`resources/app.asar.original_backup`)**:
   Prior to modifying any bytes on disk, an untouched, bit-for-bit identical copy of the official factory `app.asar` archive is created inside the application's `resources` directory. This backup file is never overwritten by subsequent patch runs, guaranteeing a foolproof and complete one-click restoration path back to the stock state at any time via `--restore`.

2. **Preload Script Client Injection (`dist/preload.js` inside ASAR)**:
   This is the primary runtime script modified within the ASAR archive. The lightweight Smart RTL observer, bundled offline WOFF2 base64 CSS, and the glassmorphism `Appearance` toolbar button are appended to the end of this script in a sandbox-isolated closure (`/* __ANTIGRAVITY_RTL_INJECTED__ */`).

3. **Background Auto-Shield Updater Hooks (inside ASAR)**:
   To ensure your typography and RTL configuration survive official Google Antigravity IDE auto-updates, non-destructive hooks are injected into `dist/updater.js` and `node_modules/electron-updater/out/BaseUpdater.js` / `NsisUpdater.js` around the `quitAndInstall()` lifecycle method. When an official update installs, a background helper quietly reapplies the patch to the new version once the installer completes.

4. **User-Data Engine Storage (`%APPDATA%/Antigravity/rtl-patch`)**:
   On Windows (`%APPDATA%\Antigravity\rtl-patch`), macOS (`~/Library/Application Support/Antigravity/rtl-patch`), and Linux (`~/.config/Antigravity/rtl-patch`), a local cached copy of the patcher engine and bundled fonts is deployed for automatic background re-patching. Running `--restore` purges this directory completely.

5. **Desktop & Start Menu Shortcuts (Preserved by Default)**:
   By default, existing application shortcuts remain 100% untouched. Only when explicitly opted in via the `--install-shortcuts` (or `-s`) flag does the patcher redirect shortcuts to `AntigravityLauncher.exe` to intercept IDE launches and protect against unannounced update reversions.

6. **Anti-Sanction & Proxy Shield Binaries (`version.dll` & `config.json` next to `Antigravity.exe`)**:
   When Proxy Shield is explicitly enabled (strictly **Opt-In**; never installed during standard RTL typography patching), a cryptographically verified, English-localized 64-bit DLL proxy (`version.dll`, SHA-256: `e7b991d65611cac615d756d6be4f55f0e3856a0d37e98cc8fb4a19ebc655e7cc`) and `config.json` are placed in the application root next to `Antigravity.exe` to intercept socket traffic for language server and worker processes. Existing custom configurations are automatically backed up to `config.json.bak` and merged non-destructively. Both files are completely removed whenever Proxy Shield is disabled or when running `--restore`. Detailed binary metadata, attribution, and build instructions are documented in [src/antigravity_rtl/bin/README.md](src/antigravity_rtl/bin/README.md).

---

## Technical Documentation & ASAR Specification

For deep-dive documentation on the Electron ASAR binary layout, 16-byte header packing, padding rules, and cryptographic SHA-256 block hash verification, see:
- [docs/ASAR_SPEC.md](docs/ASAR_SPEC.md)

---

## License

This project is licensed under the [MIT License](LICENSE). Built for the developer community with focus on performance, typography elegance, and zero-compromise stability.
