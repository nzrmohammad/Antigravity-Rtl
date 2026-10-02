# Antigravity Smart RTL & Offline Typography Suite 🚀

<div align="center">

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg?style=for-the-badge)](LICENSE)
[![Platform: Windows | macOS | Linux](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-0078D6?style=for-the-badge&logo=windows)](https://microsoft.com)
[![Tested on: Antigravity v2.19.1](https://img.shields.io/badge/Antigravity-v2.19.1%20Verified-00C853?style=for-the-badge&logo=google)](https://deepmind.google)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Node.js 16+](https://img.shields.io/badge/Node.js-16+-339933?style=for-the-badge&logo=node.js&logoColor=white)](https://nodejs.org)
[![Offline Fonts](https://img.shields.io/badge/Persian%20Fonts-100%25%20Offline-FF6B6B?style=for-the-badge)](fonts/)

**Professional, intelligent bidirectional text direction (RTL/LTR) engine with fully offline embedded Persian typography, modular Object-Oriented architecture, and zero-reflow layout for Google Antigravity IDE.**

---

</div>

## Overview

**Antigravity Smart RTL** transforms the text presentation experience in Google DeepMind's Antigravity IDE. It delivers enterprise-grade right-to-left (RTL) typography for Persian, Arabic, and bilingual environments while rigorously preserving left-to-right (LTR) orientation for source code, terminals, tool panels, thoughts, and technical identifiers.

Engineered for performance and resilience, it features a modular Object-Oriented Architecture (OOP), 100% offline embedded Persian fonts, live hot-reloading via the Chrome DevTools Protocol (CDP), official Electron ASAR binary specification compliance with SHA-256 block integrity verification, and safe non-destructive shortcut handling by default.

---

## Prerequisites & System Requirements

Before running the patcher, ensure your system meets the following requirements:

| Requirement | Specification | Notes |
|---|---|---|
| **Target Application** | **Google Antigravity IDE (v2.19.1)** | Fully tested & verified on **v2.19.1** build |
| **Operating System** | Windows 10 / 11 (64-bit), macOS 11+, or Linux | Windows is fully automated via `patch.bat` |
| **Runtime Environment** | **Python 3.8+** *OR* **Node.js 16+** | Pure standard library — zero external pip/npm packages required |
| **Network** | **100% Offline** | Zero CDN dependencies; all fonts and assets are embedded locally |
| **Permissions** | Standard User | Run as standard user (elevated rights not required for user-level installs) |

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
  - **Default Monospace** (System default monospace)
  - **Consolas** (Windows standard developer monospace)
  - **Fira Code** (renders if installed on system; supports programming ligatures)
  - **JetBrains Mono** (renders if installed on system)
  - **Cascadia Code** (Windows built-in / Terminal font)
  - **Vazir Code** (bundled bilingual Persian/English monospace)
  - **Custom Monospace...** (e.g., `Hack`, `Source Code Pro`, `Inconsolata`)
  *(Note: Third-party developer fonts like Fira Code or JetBrains Mono utilize your locally installed OS fonts, gracefully falling back to Consolas if not installed.)*

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
  - Select between Vazirmatn, Arad, B Nazanin, Shabnam, Sahel, Samim, Tahoma, System, or Custom Font
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
│   │   ├── core/
│   │   │   ├── asar.py                # AsarArchive: Electron ASAR parser, builder & SHA256 integrity
│   │   │   ├── detector.py            # PlatformDetector: Cross-platform installation locator
│   │   │   ├── process.py             # ProcessManager: Process lifecycle, launch & safe restart
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

**2. Python CLI:**  
```powershell
# Standard safe install (shortcuts preserved)
python src/patcher.py

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
│      0     Exit Patcher                                             -- [EXIT]                │▒
│                                                                                              │▒
└──────────────────────────────────────────────────────────────────────────────────────────────┘▒
```

Simply press `Enter` (or type `1`) to apply the patch.

---

## CLI Flags & Options Reference

| Flag | Shorthand | Description |
|---|---|---|
| `--install-shortcuts` | `--shortcuts`, `-s`, `3` | **Opt-in**: Protects desktop & start menu shortcuts using `AntigravityLauncher.exe` for automatic update healing. Default is disabled (safe mode). |
| `--restore` | `-r`, `2` | Fully restores `app.asar` from original factory backup and reverts shortcuts. |
| `--diagnostics` | `--diag`, `4` | Displays system telemetry, patch status, live CDP port, and installation health check. |
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
| **Persian Digits Toggle** | In Popover Switch | Toggle between Eastern Arabic/Persian numerals (`۰-۹`) and Latin/English digits (`0-9`) |
| **Font Family** | In Popover Dropdown | Select from Vazirmatn, Arad, B Nazanin, Shabnam, Sahel, Samim, Tahoma, System, or Custom Font |
| **Code & Terminal Font** | In Popover Dropdown | Customize code block and terminal monospace font (Default, Consolas, Fira Code, JetBrains Mono, Cascadia Code, Vazir Code, or Custom) |
| **Font Size** | In Popover Slider / `+` / `-` | Dynamically adjust font scale between `12px` and `24px` |
| **Line Spacing** | In Popover Buttons | Set line height to `1.5` (Compact), `1.75` (Standard), or `2.0` (Relaxed) |
| **Reset to Default** | In Popover Footer | Instantly restore typography settings to factory default values |

---

## License

This project is licensed under the [MIT License](LICENSE). Built for the developer community with focus on performance, typography elegance, and zero-compromise stability.
