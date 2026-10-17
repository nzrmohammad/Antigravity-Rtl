#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Antigravity RTL - Client Code Injector (OOP)
Generates client-side preload scripts, appearance menus, smart direction engine, and updater hooks.
"""

from typing import Optional
from ..assets import get_effective_css


class CodeInjector:
    """
    Builds injection scripts for dist/preload.js and electron-updater files.
    """

    @classmethod
    def get_client_injection(cls, css_code: Optional[str] = None) -> str:
        """
        Builds the JavaScript injection snippet for dist/preload.js.
        """
        raw_css = css_code if css_code is not None else get_effective_css()
        clean_css = raw_css.replace('\\', '\\\\').replace('`', '\\`')

        return f"""
/* __ANTIGRAVITY_RTL_INJECTED__ */
try {{
(function() {{
    const rtlCSS = `{clean_css}`;

    function applyRTL() {{
        try {{
            if (typeof electron_1 !== 'undefined' && electron_1.webFrame && electron_1.webFrame.insertCSS) {{
                electron_1.webFrame.insertCSS(rtlCSS);
            }}
        }} catch(e) {{}}

        function injectTag() {{
            if (!document.head) {{
                setTimeout(injectTag, 20);
                return;
            }}
            let s = document.getElementById('antigravity-chat-rtl-style');
            if (!s) {{
                s = document.createElement('style');
                s.id = 'antigravity-chat-rtl-style';
                document.head.appendChild(s);
            }}
            s.textContent = rtlCSS;
        }}

        if (document.readyState === 'loading') {{
            document.addEventListener('DOMContentLoaded', injectTag);
        }} else {{
            injectTag();
        }}
    }}

    applyRTL();

    // --- Settings & Appearance Subsystem ---
    const STORAGE_KEY = 'antigravity_appearance_settings';
    const DEFAULT_SETTINGS = {{
        rtlEnabled: true,
        fontFamily: 'Vazirmatn',
        customFont: '',
        fontSize: 15,
        lineHeight: 1.75,
        persianDigits: false,
        justifyText: false,
        codeFont: 'JetBrains Mono',
        customCodeFont: '',
        proxyEnabled: false,
        proxyType: 'socks5',
        proxyHost: '127.0.0.1',
        proxyPort: 10808
    }};

    function getSettings() {{
        try {{
            const raw = localStorage.getItem(STORAGE_KEY);
            if (raw) {{
                const parsed = JSON.parse(raw);
                if (parsed && typeof parsed === 'object') {{
                    if (parsed.codeFont === 'default' || !parsed.codeFont) {{
                        parsed.codeFont = 'JetBrains Mono';
                    }}
                    if (typeof parsed.justifyText !== 'boolean') {{
                        parsed.justifyText = false;
                    }}
                    if (typeof parsed.proxyEnabled !== 'boolean') {{
                        parsed.proxyEnabled = false;
                    }}
                    if (!parsed.proxyType) {{
                        parsed.proxyType = 'socks5';
                    }}
                    if (!parsed.proxyHost) {{
                        parsed.proxyHost = '127.0.0.1';
                    }}
                    if (!parsed.proxyPort) {{
                        parsed.proxyPort = 10808;
                    }}
                    return Object.assign({{}}, DEFAULT_SETTINGS, parsed);
                }}
            }}
        }} catch(e) {{}}
        return Object.assign({{}}, DEFAULT_SETTINGS);
    }}

    function saveSettings(s) {{
        try {{
            localStorage.setItem(STORAGE_KEY, JSON.stringify(s));
        }} catch(e) {{}}
    }}

    let nodeNet = null;
    let nodeFs = null;
    let nodePath = null;
    try {{
        if (typeof require === 'function') {{
            nodeNet = require('net');
            nodeFs = require('fs');
            nodePath = require('path');
        }}
    }} catch(e) {{}}

    function getAppInstallDir() {{
        try {{
            if (typeof process !== 'undefined' && process.execPath && nodePath) {{
                return nodePath.dirname(process.execPath);
            }}
        }} catch(e) {{}}
        return null;
    }}

    function syncProxyConfigToFile(s) {{
        try {{
            const appDir = getAppInstallDir();
            if (!appDir || !nodeFs || !nodePath) return;
            const cfgPath = nodePath.join(appDir, 'config.json');
            const dllPath = nodePath.join(appDir, 'version.dll');

            if (s.proxyEnabled) {{
                if (!nodeFs.existsSync(dllPath)) {{
                    const candidateSources = [
                        nodePath.join(appDir, 'resources', 'rtl-patch', 'antigravity_rtl', 'bin', 'version.dll'),
                        nodePath.join(process.env.APPDATA || '', 'Antigravity', 'rtl-patch', 'antigravity_rtl', 'bin', 'version.dll')
                    ];
                    for (const cand of candidateSources) {{
                        try {{
                            if (nodeFs.existsSync(cand)) {{
                                nodeFs.copyFileSync(cand, dllPath);
                                break;
                            }}
                        }} catch(ex) {{}}
                    }}
                }}

                let cfg = {{
                    "child_injection_mode": "filtered",
                    "fake_ip": {{ "cidr": "198.18.0.0/15", "enabled": true }},
                    "traffic_logging": false,
                    "timeout": {{ "connect": 5000, "recv": 5000, "send": 5000 }},
                    "diagnostics": {{ "agent_ip_probe": false }},
                    "_version": "2.4",
                    "_comment": "Antigravity-Proxy Configuration",
                    "log_level": "info",
                    "child_injection": true,
                    "proxy_rules": {{
                        "routing": {{
                            "default_action": "proxy",
                            "priority_mode": "order",
                            "rules": [],
                            "use_default_private": true,
                            "enabled": true
                        }},
                        "allowed_ports": [80, 443],
                        "udp_mode": "auto",
                        "ipv6_mode": "proxy",
                        "udp_fallback": "block",
                        "dns_mode": "direct"
                    }},
                    "child_injection_exclude": [],
                    "updates": {{
                        "enabled": false,
                        "allow_insecure_mirrors": false,
                        "check_delay_ms": 15000,
                        "timeout_ms": 5000,
                        "notify_once": false,
                        "mirrors": []
                    }},
                    "target_processes": [
                        "agy.exe",
                        "language_server.exe",
                        "language_server_windows",
                        "Antigravity.exe",
                        "Antigravity IDE.exe",
                        "node.exe"
                    ]
                }};

                if (nodeFs.existsSync(cfgPath)) {{
                    try {{
                        const raw = nodeFs.readFileSync(cfgPath, 'utf-8');
                        const existing = JSON.parse(raw);
                        if (existing && typeof existing === 'object') {{
                            try {{ nodeFs.copyFileSync(cfgPath, cfgPath + '.bak'); }} catch(eBak) {{}}
                            cfg = Object.assign(cfg, existing);
                        }}
                    }} catch(ex) {{}}
                }}

                cfg.child_injection = true;
                if (!cfg.updates) cfg.updates = {{}};
                cfg.updates.enabled = false;
                cfg.updates.allow_insecure_mirrors = false;
                cfg.updates.mirrors = [];
                cfg.proxy = {{
                    "type": (s.proxyType || 'socks5').toLowerCase().trim(),
                    "host": (s.proxyHost || '127.0.0.1').trim(),
                    "port": parseInt(s.proxyPort) || 10808
                }};
                nodeFs.writeFileSync(cfgPath, JSON.stringify(cfg, null, 2), 'utf-8');
            }} else {{
                if (nodeFs.existsSync(cfgPath)) {{
                    try {{
                        try {{ nodeFs.copyFileSync(cfgPath, cfgPath + '.bak'); }} catch(eBak) {{}}
                        const raw = nodeFs.readFileSync(cfgPath, 'utf-8');
                        const data = JSON.parse(raw);
                        data.child_injection = false;
                        if (data.proxy) data.proxy.type = 'direct';
                        nodeFs.writeFileSync(cfgPath, JSON.stringify(data, null, 2), 'utf-8');
                    }} catch(ex) {{
                        try {{ nodeFs.unlinkSync(cfgPath); }} catch(e2) {{}}
                    }}
                }}
                if (nodeFs.existsSync(dllPath)) {{
                    try {{ nodeFs.unlinkSync(dllPath); }} catch(e2) {{}}
                }}
            }}
        }} catch(e) {{}}
    }}

    function testProxyConnection(host, port, proxyType = 'socks5', timeoutMs = 2000) {{
        return new Promise((resolve) => {{
            const targetHost = (host || '127.0.0.1').trim();
            const targetPort = parseInt(port) || 10808;
            const ptype = (proxyType || 'socks5').toLowerCase().trim();
            const start = Date.now();

            if (nodeNet && typeof nodeNet.Socket === 'function') {{
                const socket = new nodeNet.Socket();
                let finished = false;
                socket.setTimeout(timeoutMs);

                socket.on('connect', () => {{
                    if (finished) return;
                    if (ptype === 'socks5') {{
                        socket.write(Buffer.from([0x05, 0x01, 0x00]));
                    }} else if (ptype === 'http') {{
                        socket.write(Buffer.from('HEAD http://www.gstatic.com/generate_204 HTTP/1.1\\r\\nHost: www.gstatic.com\\r\\nConnection: close\\r\\n\\r\\n'));
                    }} else {{
                        finished = true;
                        const latency = Date.now() - start;
                        socket.destroy();
                        resolve({{ ok: true, latency: latency, msg: `Port ${{targetPort}} reachable (${{latency}}ms)` }});
                    }}
                }});

                socket.on('data', (chunk) => {{
                    if (finished) return;
                    finished = true;
                    const latency = Date.now() - start;
                    socket.destroy();
                    if (ptype === 'socks5') {{
                        if (chunk.length >= 2 && chunk[0] === 0x05 && chunk[1] === 0x00) {{
                            resolve({{ ok: true, latency: latency, msg: `SOCKS5 active & verified (${{latency}}ms)` }});
                        }} else if (chunk.length >= 2 && chunk[0] === 0x05) {{
                            resolve({{ ok: true, latency: latency, msg: `SOCKS5 active (${{latency}}ms)` }});
                        }} else {{
                            resolve({{ ok: false, latency: latency, msg: 'Port open, but failed SOCKS5 handshake' }});
                        }}
                    }} else if (ptype === 'http') {{
                        if (chunk.toString().indexOf('HTTP/') !== -1) {{
                            resolve({{ ok: true, latency: latency, msg: `HTTP proxy active & verified (${{latency}}ms)` }});
                        }} else {{
                            resolve({{ ok: false, latency: latency, msg: 'Port open, but invalid HTTP response' }});
                        }}
                    }}
                }});

                socket.on('timeout', () => {{
                    if (!finished) {{
                        finished = true;
                        socket.destroy();
                        resolve({{ ok: false, latency: timeoutMs, msg: 'Connection timed out' }});
                    }}
                }});

                socket.on('error', (err) => {{
                    if (!finished) {{
                        finished = true;
                        socket.destroy();
                        const latency = Date.now() - start;
                        const msg = (err.code === 'ECONNREFUSED')
                            ? `Connection refused: No proxy app on port ${{targetPort}}`
                            : (err.code || 'Unreachable');
                        resolve({{ ok: false, latency: latency, msg: msg }});
                    }}
                }});

                try {{
                    socket.connect(targetPort, targetHost);
                }} catch(e) {{
                    resolve({{ ok: false, latency: 0, msg: e.message || 'Socket error' }});
                }}
                return;
            }}

            const controller = new AbortController();
            const timer = setTimeout(() => controller.abort(), timeoutMs);
            fetch(`http://${{targetHost}}:${{targetPort}}/`, {{ method: 'HEAD', mode: 'no-cors', signal: controller.signal }})
                .then(() => {{
                    clearTimeout(timer);
                    const latency = Date.now() - start;
                    resolve({{ ok: true, latency: latency, msg: `Port ${{targetPort}} is open & reachable (${{latency}}ms)` }});
                }})
                .catch((err) => {{
                    clearTimeout(timer);
                    const latency = Date.now() - start;
                    if (err.name === 'AbortError') {{
                        resolve({{ ok: false, latency: latency, msg: `Port ${{targetPort}} timed out (${{timeoutMs}}ms)` }});
                    }} else {{
                        resolve({{ ok: false, latency: latency, msg: `Connection refused on port ${{targetPort}} (offline)` }});
                    }}
                }});
        }});
    }}

    let currentSettings = getSettings();

    function getFontFamilyValue(fontName, customName) {{
        switch(fontName) {{
            case 'IRANSans':
                return "'IRANSans', 'IRANSansX', 'IRAN Sans', 'IranSans', sans-serif";
            case 'IRANYekan':
                return "'IRANYekan', 'IRANYekanX', 'IRAN Yekan', 'IranYekan', sans-serif";
            case 'Dana':
                return "'Dana', 'dana', sans-serif";
            case 'Inter':
                return "'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif";
            case 'Arad':
                return "'Arad', sans-serif";
            case 'BNazanin':
                return "'B Nazanin', 'BNazanin', 'B-Nazanin', serif, sans-serif";
            case 'Shabnam':
                return "'Shabnam', 'Vazirmatn', sans-serif";
            case 'Sahel':
                return "'Sahel', 'Vazirmatn', sans-serif";
            case 'Samim':
                return "'Samim', 'Vazirmatn', sans-serif";
            case 'Tahoma':
                return "'Tahoma', 'Vazirmatn', -apple-system, sans-serif";
            case 'System':
                return "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif";
            case 'Custom':
                if (customName) {{
                    const c = customName.trim();
                    if (/^iransans/i.test(c)) return `'${{c}}', 'IRANSansX', 'IRANSans', 'IRAN Sans', 'IranSans', sans-serif`;
                    if (/^iranyekan/i.test(c)) return `'${{c}}', 'IRANYekanX', 'IRANYekan', 'IRAN Yekan', 'IranYekan', sans-serif`;
                    if (/^dana/i.test(c)) return `'${{c}}', 'Dana', 'dana', sans-serif`;
                    return `'${{c}}', 'Vazirmatn', sans-serif`;
                }}
                return "'Vazirmatn', sans-serif";
            case 'Vazirmatn':
            default:
                return "'Vazirmatn', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif";
        }}
    }}

    function getCodeFontValue(codeFont, customCodeFont) {{
        switch(codeFont) {{
            case 'JetBrains Mono':
                return "'JetBrains Mono', Consolas, 'Courier New', monospace";
            case 'Consolas':
                return "'Consolas', 'Courier New', monospace";
            case 'Fira Code':
                return "'Fira Code', Consolas, 'Courier New', monospace";
            case 'Cascadia Code':
                return "'Cascadia Code', 'Cascadia Mono', Consolas, monospace";
            case 'Vazirmatn':
            case 'Vazir Code':
                return "'Vazirmatn', 'Vazir Code', Consolas, monospace";
            case 'Custom':
                return (customCodeFont ? `'${{customCodeFont}}', ` : "") + "Consolas, monospace";
            case 'default':
            default:
                return "'JetBrains Mono', Consolas, 'Courier New', Menlo, Monaco, monospace";
        }}
    }}

    function isFontBundled(fontName) {{
        if (!fontName) return false;
        const bundled = [
            'Vazirmatn', 'Inter', 'JetBrains Mono', 'Arad',
            'B Nazanin', 'BNazanin', 'Shabnam', 'Sahel', 'Samim', 'System'
        ];
        return bundled.includes(fontName);
    }}

    function isFontAvailable(fontName) {{
        if (!fontName) return false;
        if (isFontBundled(fontName)) return true;

        const candidates = [fontName];
        if (fontName === 'IRANSans') candidates.push('IRANSansX', 'IRAN Sans', 'IranSans');
        if (fontName === 'IRANYekan') candidates.push('IRANYekanX', 'IRAN Yekan', 'IranYekan');
        if (fontName === 'Dana') candidates.push('dana', 'DanaFaNum');
        if (fontName === 'Fira Code') candidates.push('FiraCode', 'FiraCode-Regular');
        if (fontName === 'Cascadia Code') candidates.push('Cascadia Mono');

        try {{
            const testStr = "abcdefghijklmnopqrstuvwxyz0123456789\\u0627\\u0644\\u0641\\u0628\\u0627";
            const canvas = document.createElement("canvas");
            const ctx = canvas.getContext("2d");
            if (!ctx) return false;

            ctx.font = "72px monospace";
            const baseMono = ctx.measureText(testStr).width;
            ctx.font = "72px sans-serif";
            const baseSans = ctx.measureText(testStr).width;

            for (let i = 0; i < candidates.length; i++) {{
                const name = candidates[i];
                ctx.font = `72px "${{name}}", monospace`;
                const testMono = ctx.measureText(testStr).width;
                ctx.font = `72px "${{name}}", sans-serif`;
                const testSans = ctx.measureText(testStr).width;

                if ((testMono !== baseMono) || (testSans !== baseSans)) {{
                    return true;
                }}
            }}
            return false;
        }} catch(e) {{
            return false;
        }}
    }}

    function getFontStatus(fontName) {{
        if (!fontName) return 'missing';
        if (isFontBundled(fontName)) return 'bundled';
        return isFontAvailable(fontName) ? 'installed' : 'missing';
    }}

    function applySettings(s) {{
        if (!document.documentElement) return;
        const root = document.documentElement;
        root.style.setProperty('--ag-font-size', s.fontSize + 'px');
        root.style.setProperty('--ag-line-height', s.lineHeight.toString());
        root.style.setProperty('--ag-font-family', getFontFamilyValue(s.fontFamily, s.customFont));
        root.style.setProperty('--ag-code-font', getCodeFontValue(s.codeFont, s.customCodeFont));
        root.style.setProperty('--ag-font-features', s.persianDigits ? '"ss01" 1' : 'normal');

        if (!document.body) return;
        if (s.justifyText) {{
            document.body.classList.add('ag-text-justify');
        }} else {{
            document.body.classList.remove('ag-text-justify');
        }}

        if (s.rtlEnabled) {{
            document.body.classList.remove('ag-rtl-disabled');
            processAllSmartRTL(document.body);
        }} else {{
            document.body.classList.add('ag-rtl-disabled');
        }}
    }}

    // --- Smart Direction Subsystem (70% Latin Threshold & Letter-Only Counting) ---
    function detectSmartDirection(text, fallbackDir) {{
        if (!text) return null;
        const trimmed = text.trim();
        if (!trimmed) return null;

        const latinMatches = trimmed.match(/[a-zA-Z]/g);
        const latinCount = latinMatches ? latinMatches.length : 0;

        const persianMatches = trimmed.match(/[؀-ۿݐ-ݿࢠ-ࣿﭐ-﷿ﹰ-﻿]/g);
        const persianCount = persianMatches ? persianMatches.length : 0;

        const totalLetters = latinCount + persianCount;
        if (totalLetters === 0) {{
            return fallbackDir !== undefined ? fallbackDir : 'rtl';
        }}

        if (persianCount === 0) return 'ltr';
        if (latinCount === 0) return 'rtl';

        // If the first alphabetic letter is Persian, it is always a Persian sentence (RTL)
        const firstLetterMatch = trimmed.match(/[a-zA-Z؀-ۿݐ-ݿࢠ-ࣿﭐ-﷿ﹰ-﻿]/);
        if (firstLetterMatch && /[؀-ۿݐ-ݿࢠ-ࣿﭐ-﷿ﹰ-﻿]/.test(firstLetterMatch[0])) {{
            return 'rtl';
        }}

        // When starting with Latin or symbols: only LTR if Latin letters are >= 70% of all letters
        const latinRatio = latinCount / totalLetters;
        if (latinRatio >= 0.7) {{
            return 'ltr';
        }}

        return 'rtl';
    }}

    function isInsideTechnicalContainer(node) {{
        if (!node || node.nodeType !== 1) return false;
        return !!node.closest(
            'pre, code, kbd, samp, var, ' +
            '.monaco-editor, .monaco-diff-editor, ' +
            '.terminal, .xterm, .integrated-terminal, ' +
            '[class*="terminal"], [class*="console"], ' +
            '.debug-console, ' +
            '.suggest-widget, .parameter-hints-widget, ' +
            '.suggest-details, ' +
            '[data-testid="terminal"], [data-testid="interactive-terminal"], ' +
            '[data-testid="code-block"], [data-testid="monaco-editor"], ' +
            '[data-mode-id], ' +
            'span.duration, div.duration, span[class*="duration"], div[class*="duration"], ' +
            'span[class*="elapsed"], div[class*="elapsed"], ' +
            'div[data-testid="status-bar"], ' +
            '#ag-appearance-popover'
        );
    }}

    function applySmartDirectionToElement(el) {{
        if (!el || el.nodeType !== 1) return;
        if (document.body && document.body.classList.contains('ag-rtl-disabled')) return;
        if (isInsideTechnicalContainer(el)) return;

        if (el.getAttribute('data-testid') === 'conversation-row-sidebar' || (el.closest && el.closest('[data-testid="conversation-row-sidebar"]'))) {{
            const row = el.getAttribute('data-testid') === 'conversation-row-sidebar' ? el : el.closest('[data-testid="conversation-row-sidebar"]');
            const dir = detectSmartDirection(row.textContent || '');
            if (dir) {{
                row.setAttribute('dir', dir);
                const spans = row.querySelectorAll('span, .truncate');
                for (let i = 0; i < spans.length; i++) spans[i].setAttribute('dir', dir);
            }}
            return;
        }}

        if (el.tagName === 'P' && el.closest && el.closest('div[data-lexical-editor="true"], #antigravity\\.agentSidePanelInputBox [contenteditable="true"]')) {{
            const dir = detectSmartDirection(el.textContent || '');
            if (dir) el.setAttribute('dir', dir);
            return;
        }}

        if (el.tagName === 'INPUT' || el.tagName === 'TEXTAREA') {{
            if (/[؀-ۿ]/.test(el.value || '')) el.setAttribute('dir', 'rtl');
            else el.setAttribute('dir', 'ltr');
            return;
        }}

        if (el.getAttribute('contenteditable') === 'true') {{
            if (/[؀-ۿ]/.test(el.textContent || '')) el.setAttribute('dir', 'rtl');
            else el.setAttribute('dir', 'ltr');
            return;
        }}

        if (el.classList && el.classList.contains('artifact-card')) {{
            const desc = el.querySelector('.text-secondary-foreground, span.line-clamp-3');
            if (desc) {{
                const dir = detectSmartDirection(desc.textContent || '');
                if (dir) desc.setAttribute('dir', dir);
            }}
            return;
        }}

        if ((el.classList && el.classList.contains('line-clamp-3')) || (el.classList && el.classList.contains('text-secondary-foreground'))) {{
            if (el.closest('.artifact-card')) {{
                const dir = detectSmartDirection(el.textContent || '');
                if (dir) el.setAttribute('dir', dir);
                return;
            }}
        }}

        if (el.tagName === 'TABLE') {{
            const dir = detectSmartDirection(el.textContent || '');
            if (dir) {{
                el.setAttribute('dir', dir);
                const cells = el.querySelectorAll('th, td');
                for (let i = 0; i < cells.length; i++) {{
                    const cellDir = detectSmartDirection(cells[i].textContent || '', dir);
                    if (cellDir) cells[i].setAttribute('dir', cellDir);
                }}
            }}
            return;
        }}

        if (el.tagName === 'LI') {{
            const dir = detectSmartDirection(el.textContent || '');
            if (dir) {{
                el.setAttribute('dir', dir);
                const ps = el.querySelectorAll('p');
                for (let i = 0; i < ps.length; i++) {{
                    const pDir = detectSmartDirection(ps[i].textContent || '', dir);
                    if (pDir) ps[i].setAttribute('dir', pDir);
                }}
            }}
            return;
        }}

        if (el.tagName === 'P') {{
            const dir = detectSmartDirection(el.textContent || '');
            if (dir) el.setAttribute('dir', dir);
            return;
        }}

        if (/^H[1-6]$/.test(el.tagName)) {{
            const dir = detectSmartDirection(el.textContent || '');
            if (dir) el.setAttribute('dir', dir);
            return;
        }}

        if (el.tagName === 'BLOCKQUOTE') {{
            const dir = detectSmartDirection(el.textContent || '');
            if (dir) el.setAttribute('dir', dir);
            return;
        }}

        if (el.tagName === 'DIV') {{
            const isChatMessage = el.getAttribute('data-testid') === 'chat-message' ||
                                 (el.className && typeof el.className === 'string' &&
                                  (el.className.includes('chat-message') || el.className.includes('prose')));
            if (isChatMessage) {{
                const dir = detectSmartDirection(el.textContent || '');
                if (dir) el.setAttribute('dir', dir);
            }}
        }}
    }}

    function processAllSmartRTL(root) {{
        if (!root || !root.querySelectorAll) return;
        if (document.body && document.body.classList.contains('ag-rtl-disabled')) return;

        const base = (root.nodeType === 9 || root === document.body) ? document : root;
        const selector = 'p, h1, h2, h3, h4, h5, h6, li, blockquote, table, ' +
                         'div.artifact-card, div.artifact-card .text-secondary-foreground, ' +
                         '[data-testid="conversation-row-sidebar"], [data-testid="conversation-row-sidebar"] span, [data-testid="conversation-row-sidebar"] .truncate, ' +
                         'div[data-lexical-editor="true"] p, #antigravity\\.agentSidePanelInputBox [contenteditable="true"] p, ' +
                         'input, textarea, [contenteditable="true"]';
        try {{
            const elements = base.querySelectorAll(selector);
            for (let i = 0; i < elements.length; i++) {{
                applySmartDirectionToElement(elements[i]);
            }}
        }} catch(e) {{}}
    }}

    // --- Menubar Button & Settings Popover ---
    let popoverInstance = null;

    function initAppearanceMenu() {{
        const bar = document.querySelector('[data-testid="title-menu-bar"]');
        if (!bar) return;

        let container = document.getElementById('ag-appearance-menu-container');
        if (!container) {{
            container = document.createElement('div');
            container.id = 'ag-appearance-menu-container';
            container.className = 'relative';
            container.style.appRegion = 'no-drag';
            bar.appendChild(container);
        }}

        let btn = document.getElementById('ag-appearance-menu-btn');
        if (btn) return;

        btn = document.createElement('button');
        btn.id = 'ag-appearance-menu-btn';
        btn.className = 'inline-flex items-center font-medium transition-colors select-none outline-none cursor-pointer justify-center disabled:opacity-50 bg-secondary/80 hover:bg-secondary text-foreground h-7 text-xs rounded-md gap-1.5 px-3 border border-border/40 select-none';
        btn.setAttribute('data-testid', 'title-menu-bar-item');
        btn.title = 'Appearance & Smart RTL Settings';
        btn.style.cssText = 'font-size: 12.5px; font-weight: 600; font-family: inherit; display: inline-flex; align-items: center; gap: 6px; cursor: pointer;';
        btn.innerHTML = `
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" style="opacity:0.9; color:#60a5fa;">
                <circle cx="12" cy="12" r="3"></circle>
                <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"></path>
            </svg>
            <span>Appearance</span>
        `;
        container.appendChild(btn);
        if (window.__ag_appearance_interval__) {{
            clearInterval(window.__ag_appearance_interval__);
            window.__ag_appearance_interval__ = null;
        }}

        function closePopover() {{
            if (popoverInstance) {{
                popoverInstance.remove();
                popoverInstance = null;
                btn.classList.remove('bg-secondary', 'text-foreground');
            }}
        }}

        function openPopover() {{
            if (popoverInstance) {{
                closePopover();
                return;
            }}

            btn.classList.add('bg-secondary', 'text-foreground');
            const rect = btn.getBoundingClientRect();

            popoverInstance = document.createElement('div');
            popoverInstance.id = 'ag-appearance-popover';
            popoverInstance.style.cssText = `
                position: fixed;
                top: ${{rect.bottom + 6}}px;
                left: ${{Math.min(rect.left, window.innerWidth - 365)}}px;
                width: 350px;
                max-height: 85vh;
                overflow-y: auto;
                background: rgba(22, 22, 26, 0.96);
                backdrop-filter: blur(20px);
                -webkit-backdrop-filter: blur(20px);
                border: 1px solid rgba(255, 255, 255, 0.15);
                color: #f4f4f5;
                font-family: 'Vazirmatn', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                direction: ltr;
                text-align: left;
                padding: 16px;
                border-radius: 14px;
                box-shadow: 0 25px 60px -10px rgba(0, 0, 0, 0.8), 0 0 0 1px rgba(255, 255, 255, 0.08);
                z-index: 999999;
                user-select: none;
                scrollbar-width: thin;
                scrollbar-color: rgba(255, 255, 255, 0.2) transparent;
            `;

            popoverInstance.innerHTML = `
                <div style="display: flex; align-items: center; justify-content: space-between; border-bottom: 1px solid rgba(255,255,255,0.1); padding-bottom: 12px; margin-bottom: 14px;">
                    <div style="display: flex; align-items: center; gap: 8px;">
                        <span style="font-size: 15px; font-weight: 700; color: #fff; letter-spacing: 0.2px;">Appearance & Smart RTL</span>
                    </div>
                    <span style="font-size: 11px; padding: 2px 8px; background: rgba(59, 130, 246, 0.22); color: #60a5fa; border: 1px solid rgba(59, 130, 246, 0.35); border-radius: 5px; font-weight: 600;">v1.2</span>
                </div>

                <!-- RTL Toggle -->
                <div style="display: flex; align-items: center; justify-content: space-between; background: rgba(255,255,255,0.04); padding: 11px 14px; border-radius: 10px; margin-bottom: 12px; border: 1px solid rgba(255,255,255,0.08);">
                    <div>
                        <div style="font-size: 13.5px; font-weight: 600; color: #fff; display: flex; align-items: center; gap: 7px;">
                            <span>Smart RTL</span>
                            <span id="ag-rtl-status-badge" style="font-size: 11px; padding: 2px 7px; border-radius: 4px; font-weight: 600; background: ${{currentSettings.rtlEnabled ? 'rgba(34, 197, 94, 0.22)' : 'rgba(161, 161, 170, 0.2)'}}; color: ${{currentSettings.rtlEnabled ? '#4ade80' : '#a1a1aa'}};">${{currentSettings.rtlEnabled ? 'Enabled' : 'Disabled'}}</span>
                        </div>
                        <div style="font-size: 11.5px; color: #a1a1aa; margin-top: 3px;">Auto-direction & Persian fonts (Alt+R)</div>
                    </div>
                    <div id="ag-toggle-rtl" style="width: 46px; height: 26px; background: ${{currentSettings.rtlEnabled ? '#3b82f6' : '#3f3f46'}}; border-radius: 13px; position: relative; cursor: pointer; transition: background .2s; box-shadow: inset 0 2px 4px rgba(0,0,0,0.3); flex-shrink: 0;">
                        <div id="ag-toggle-knob" style="position: absolute; width: 20px; height: 20px; background: white; border-radius: 50%; top: 3px; left: ${{currentSettings.rtlEnabled ? '22px' : '4px'}}; transition: left .2s; box-shadow: 0 2px 4px rgba(0,0,0,0.3);"></div>
                    </div>
                </div>

                <!-- Persian Digits Toggle -->
                <div style="display: flex; align-items: center; justify-content: space-between; background: rgba(255,255,255,0.04); padding: 11px 14px; border-radius: 10px; margin-bottom: 12px; border: 1px solid rgba(255,255,255,0.08);">
                    <div>
                        <div style="font-size: 13.5px; font-weight: 600; color: #fff; display: flex; align-items: center; gap: 7px;">
                            <span>Persian Digits</span>
                            <span id="ag-digits-status-badge" style="font-size: 11px; padding: 2px 7px; border-radius: 4px; font-weight: 600; background: ${{currentSettings.persianDigits ? 'rgba(34, 197, 94, 0.22)' : 'rgba(161, 161, 170, 0.2)'}}; color: ${{currentSettings.persianDigits ? '#4ade80' : '#a1a1aa'}};">${{currentSettings.persianDigits ? '۰-۹ (Farsi)' : '0-9 (Latin)'}}</span>
                        </div>
                        <div style="font-size: 11.5px; color: #a1a1aa; margin-top: 3px;">Toggle Persian numerals vs Latin digits</div>
                    </div>
                    <div id="ag-toggle-digits" style="width: 46px; height: 26px; background: ${{currentSettings.persianDigits ? '#3b82f6' : '#3f3f46'}}; border-radius: 13px; position: relative; cursor: pointer; transition: background .2s; box-shadow: inset 0 2px 4px rgba(0,0,0,0.3); flex-shrink: 0;">
                        <div id="ag-digits-knob" style="position: absolute; width: 20px; height: 20px; background: white; border-radius: 50%; top: 3px; left: ${{currentSettings.persianDigits ? '22px' : '4px'}}; transition: left .2s; box-shadow: 0 2px 4px rgba(0,0,0,0.3);"></div>
                    </div>
                </div>

                <!-- Justify Text Toggle -->
                <div style="display: flex; align-items: center; justify-content: space-between; background: rgba(255,255,255,0.04); padding: 11px 14px; border-radius: 10px; margin-bottom: 12px; border: 1px solid rgba(255,255,255,0.08);">
                    <div>
                        <div style="font-size: 13.5px; font-weight: 600; color: #fff; display: flex; align-items: center; gap: 7px;">
                            <span>Justify Text</span>
                            <span id="ag-justify-status-badge" style="font-size: 11px; padding: 2px 7px; border-radius: 4px; font-weight: 600; background: ${{currentSettings.justifyText ? 'rgba(34, 197, 94, 0.22)' : 'rgba(161, 161, 170, 0.2)'}}; color: ${{currentSettings.justifyText ? '#4ade80' : '#a1a1aa'}};">${{currentSettings.justifyText ? 'Enabled' : 'Disabled'}}</span>
                        </div>
                        <div style="font-size: 11.5px; color: #a1a1aa; margin-top: 3px;">Smart paragraph justification with natural edge anchoring</div>
                    </div>
                    <div id="ag-toggle-justify" style="width: 46px; height: 26px; background: ${{currentSettings.justifyText ? '#3b82f6' : '#3f3f46'}}; border-radius: 13px; position: relative; cursor: pointer; transition: background .2s; box-shadow: inset 0 2px 4px rgba(0,0,0,0.3); flex-shrink: 0;">
                        <div id="ag-justify-knob" style="position: absolute; width: 20px; height: 20px; background: white; border-radius: 50%; top: 3px; left: ${{currentSettings.justifyText ? '22px' : '4px'}}; transition: left .2s; box-shadow: 0 2px 4px rgba(0,0,0,0.3);"></div>
                    </div>
                </div>

                <!-- Anti-Sanction & Proxy Shield Card -->
                <div style="background: rgba(255,255,255,0.04); border: 1px solid rgba(255,255,255,0.08); border-radius: 10px; padding: 12px 14px; margin-bottom: 14px;">
                    <div style="display: flex; align-items: center; justify-content: space-between;">
                        <div>
                            <div style="font-size: 13.5px; font-weight: 600; color: #fff; display: flex; align-items: center; gap: 7px;">
                                <span>🛡️ Proxy Shield</span>
                                <span id="ag-proxy-status-badge" style="font-size: 11px; padding: 2px 7px; border-radius: 4px; font-weight: 600; background: ${{currentSettings.proxyEnabled ? 'rgba(34, 197, 94, 0.22)' : 'rgba(161, 161, 170, 0.2)'}}; color: ${{currentSettings.proxyEnabled ? '#4ade80' : '#a1a1aa'}};">${{currentSettings.proxyEnabled ? 'Enabled' : 'Disabled'}}</span>
                            </div>
                            <div style="font-size: 11.5px; color: #a1a1aa; margin-top: 3px;">Bypass geo-restrictions & sanction errors (400/403)</div>
                        </div>
                        <div id="ag-toggle-proxy" style="width: 46px; height: 26px; background: ${{currentSettings.proxyEnabled ? '#3b82f6' : '#3f3f46'}}; border-radius: 13px; position: relative; cursor: pointer; transition: background .2s; box-shadow: inset 0 2px 4px rgba(0,0,0,0.3); flex-shrink: 0;">
                            <div id="ag-proxy-knob" style="position: absolute; width: 20px; height: 20px; background: white; border-radius: 50%; top: 3px; left: ${{currentSettings.proxyEnabled ? '22px' : '4px'}}; transition: left .2s; box-shadow: 0 2px 4px rgba(0,0,0,0.3);"></div>
                        </div>
                    </div>

                    <!-- Collapsible Proxy Configuration Details -->
                    <div id="ag-proxy-panel" style="display: ${{currentSettings.proxyEnabled ? 'block' : 'none'}}; margin-top: 11px; padding-top: 11px; border-top: 1px solid rgba(255,255,255,0.08);">
                        <!-- Protocol Selector -->
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 9px;">
                            <label style="font-size: 12px; font-weight: 600; color: #e4e4e7;">Protocol:</label>
                            <div style="display: flex; gap: 6px;">
                                <button type="button" id="ag-proto-socks5" class="ag-proto-btn" style="background: ${{currentSettings.proxyType === 'socks5' ? '#3b82f6' : '#27272a'}}; border: 1px solid ${{currentSettings.proxyType === 'socks5' ? '#3b82f6' : 'rgba(255,255,255,0.14)'}}; color: ${{currentSettings.proxyType === 'socks5' ? '#fff' : '#d4d4d8'}}; font-size: 11px; font-weight: 600; border-radius: 5px; padding: 3px 9px; cursor: pointer;">SOCKS5 (Best)</button>
                                <button type="button" id="ag-proto-http" class="ag-proto-btn" style="background: ${{currentSettings.proxyType === 'http' ? '#3b82f6' : '#27272a'}}; border: 1px solid ${{currentSettings.proxyType === 'http' ? '#3b82f6' : 'rgba(255,255,255,0.14)'}}; color: ${{currentSettings.proxyType === 'http' ? '#fff' : '#d4d4d8'}}; font-size: 11px; font-weight: 600; border-radius: 5px; padding: 3px 9px; cursor: pointer;">HTTP</button>
                            </div>
                        </div>

                        <!-- Host, Port, and Live Test Button -->
                        <div style="display: flex; gap: 8px; align-items: flex-end; margin-bottom: 9px;">
                            <div style="flex: 1.3;">
                                <label style="font-size: 11px; font-weight: 500; color: #a1a1aa; display: block; margin-bottom: 3px;">Host:</label>
                                <input type="text" id="ag-proxy-host-input" value="${{currentSettings.proxyHost || '127.0.0.1'}}" style="width: 100%; background: #27272a; color: #fff; border: 1px solid rgba(255,255,255,0.16); border-radius: 6px; padding: 5px 8px; font-size: 12px; outline: none; box-sizing: border-box; font-family: monospace;">
                            </div>
                            <div style="flex: 1;">
                                <label style="font-size: 11px; font-weight: 500; color: #a1a1aa; display: block; margin-bottom: 3px;">Port:</label>
                                <input type="number" id="ag-proxy-port-input" value="${{currentSettings.proxyPort || 10808}}" min="1" max="65535" style="width: 100%; background: #27272a; color: #fff; border: 1px solid rgba(255,255,255,0.16); border-radius: 6px; padding: 5px 8px; font-size: 12px; outline: none; box-sizing: border-box; font-family: monospace;">
                            </div>
                            <div>
                                <button type="button" id="ag-proxy-test-btn" style="background: rgba(59, 130, 246, 0.2); border: 1px solid rgba(59, 130, 246, 0.45); color: #60a5fa; padding: 5px 11px; border-radius: 6px; font-size: 12px; font-weight: 600; cursor: pointer; white-space: nowrap; height: 30px; display: flex; align-items: center; gap: 4px; transition: all .15s;">
                                    <span>⚡ Test</span>
                                </button>
                            </div>
                        </div>

                        <!-- Live Test Status Banner -->
                        <div id="ag-proxy-test-result" style="display: none; padding: 6px 10px; border-radius: 6px; font-size: 11.5px; margin-bottom: 9px; align-items: center; justify-content: space-between;">
                            <span id="ag-proxy-test-msg" style="font-weight: 500;"></span>
                            <span id="ag-proxy-test-latency" style="font-weight: 700; font-family: monospace; font-size: 11px;"></span>
                        </div>

                        <!-- Quick Presets -->
                        <div>
                            <div style="font-size: 10.5px; font-weight: 600; color: #71717a; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 5px;">Quick Presets:</div>
                            <div style="display: flex; flex-wrap: wrap; gap: 5px;">
                                <button type="button" class="ag-proxy-preset-btn" data-type="socks5" data-port="7890" style="background: #27272a; border: 1px solid rgba(255,255,255,0.12); color: #d4d4d8; font-size: 10.5px; padding: 3px 7px; border-radius: 5px; cursor: pointer;">Clash (7890)</button>
                                <button type="button" class="ag-proxy-preset-btn" data-type="socks5" data-port="7897" style="background: #27272a; border: 1px solid rgba(255,255,255,0.12); color: #d4d4d8; font-size: 10.5px; padding: 3px 7px; border-radius: 5px; cursor: pointer;">Clash Meta (7897)</button>
                                <button type="button" class="ag-proxy-preset-btn" data-type="socks5" data-port="10808" style="background: #27272a; border: 1px solid rgba(255,255,255,0.12); color: #d4d4d8; font-size: 10.5px; padding: 3px 7px; border-radius: 5px; cursor: pointer;">v2rayN (10808)</button>
                                <button type="button" class="ag-proxy-preset-btn" data-type="http" data-port="10809" style="background: #27272a; border: 1px solid rgba(255,255,255,0.12); color: #d4d4d8; font-size: 10.5px; padding: 3px 7px; border-radius: 5px; cursor: pointer;">v2rayN HTTP (10809)</button>
                                <button type="button" class="ag-proxy-preset-btn" data-type="socks5" data-port="2080" style="background: #27272a; border: 1px solid rgba(255,255,255,0.12); color: #d4d4d8; font-size: 10.5px; padding: 3px 7px; border-radius: 5px; cursor: pointer;">Sing-box (2080)</button>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Font Family Selection -->
                <div style="margin-bottom: 14px;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 7px;">
                        <label style="font-size: 13px; font-weight: 600; color: #e4e4e7;">Font Family:</label>
                        <span id="ag-font-family-badge" style="font-size: 11px; padding: 2px 7px; border-radius: 4px; font-weight: 600;"></span>
                    </div>
                    <select id="ag-font-family-select" style="width: 100%; background: #27272a; color: #f4f4f5; border: 1px solid rgba(255,255,255,0.18); border-radius: 8px; padding: 7px 11px; font-size: 13px; font-weight: 500; outline: none; font-family: inherit; cursor: pointer; transition: border-color .15s;">
                        <option value="Vazirmatn" ${{currentSettings.fontFamily === 'Vazirmatn' ? 'selected' : ''}}>Vazirmatn</option>
                        <option value="Inter" ${{currentSettings.fontFamily === 'Inter' ? 'selected' : ''}}>Inter</option>
                        <option value="IRANSans" ${{currentSettings.fontFamily === 'IRANSans' ? 'selected' : ''}}>IRANSans</option>
                        <option value="IRANYekan" ${{currentSettings.fontFamily === 'IRANYekan' ? 'selected' : ''}}>IRANYekan</option>
                        <option value="Dana" ${{currentSettings.fontFamily === 'Dana' ? 'selected' : ''}}>Dana</option>
                        <option value="BNazanin" ${{currentSettings.fontFamily === 'BNazanin' ? 'selected' : ''}}>B Nazanin</option>
                        <option value="Arad" ${{currentSettings.fontFamily === 'Arad' ? 'selected' : ''}}>Arad</option>
                        <option value="Shabnam" ${{currentSettings.fontFamily === 'Shabnam' ? 'selected' : ''}}>Shabnam</option>
                        <option value="Sahel" ${{currentSettings.fontFamily === 'Sahel' ? 'selected' : ''}}>Sahel</option>
                        <option value="Samim" ${{currentSettings.fontFamily === 'Samim' ? 'selected' : ''}}>Samim</option>
                        <option value="Tahoma" ${{currentSettings.fontFamily === 'Tahoma' ? 'selected' : ''}}>Tahoma</option>
                        <option value="System" ${{currentSettings.fontFamily === 'System' ? 'selected' : ''}}>System Font</option>
                        <option value="Custom" ${{currentSettings.fontFamily === 'Custom' ? 'selected' : ''}}>Custom Font...</option>
                    </select>
                    <div id="ag-custom-font-container" style="display: ${{currentSettings.fontFamily === 'Custom' ? 'block' : 'none'}}; margin-top: 7px;">
                        <input type="text" id="ag-custom-font-input" placeholder="Font name (e.g. IRANSansX, Dana, B Titr)" value="${{currentSettings.customFont || ''}}" style="width: 100%; background: #1f1f23; color: #fff; border: 1px solid rgba(59,130,246,0.5); border-radius: 8px; padding: 7px 10px; font-size: 12.5px; outline: none; box-sizing: border-box;">
                    </div>
                </div>

                <!-- Code & Terminal Font Selection -->
                <div style="margin-bottom: 14px;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 7px;">
                        <label style="font-size: 13px; font-weight: 600; color: #e4e4e7;">Code & Terminal Font:</label>
                        <span id="ag-code-font-badge" style="font-size: 11px; padding: 2px 7px; border-radius: 4px; font-weight: 600;"></span>
                    </div>
                    <select id="ag-code-font-select" style="width: 100%; background: #27272a; color: #f4f4f5; border: 1px solid rgba(255,255,255,0.18); border-radius: 8px; padding: 7px 11px; font-size: 13px; font-weight: 500; outline: none; font-family: inherit; cursor: pointer; transition: border-color .15s;">
                        <option value="JetBrains Mono" ${{(currentSettings.codeFont === 'JetBrains Mono' || currentSettings.codeFont === 'default') ? 'selected' : ''}}>JetBrains Mono</option>
                        <option value="Consolas" ${{currentSettings.codeFont === 'Consolas' ? 'selected' : ''}}>Consolas</option>
                        <option value="Fira Code" ${{currentSettings.codeFont === 'Fira Code' ? 'selected' : ''}}>Fira Code</option>
                        <option value="Cascadia Code" ${{currentSettings.codeFont === 'Cascadia Code' ? 'selected' : ''}}>Cascadia Code</option>
                        <option value="Vazirmatn" ${{currentSettings.codeFont === 'Vazirmatn' ? 'selected' : ''}}>Vazir Code</option>
                        <option value="Custom" ${{currentSettings.codeFont === 'Custom' ? 'selected' : ''}}>Custom Monospace...</option>
                    </select>
                    <div id="ag-custom-code-font-container" style="display: ${{currentSettings.codeFont === 'Custom' ? 'block' : 'none'}}; margin-top: 7px;">
                        <input type="text" id="ag-custom-code-font-input" placeholder="Monospace font name (e.g. Hack, Source Code Pro)" value="${{currentSettings.customCodeFont || ''}}" style="width: 100%; background: #1f1f23; color: #fff; border: 1px solid rgba(59,130,246,0.5); border-radius: 8px; padding: 7px 10px; font-size: 12.5px; outline: none; box-sizing: border-box;">
                    </div>
                </div>

                <!-- Font Size Stepper & Slider -->
                <div style="margin-bottom: 14px;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 7px;">
                        <span style="font-size: 13px; font-weight: 600; color: #e4e4e7;">Font Size:</span>
                        <span id="ag-font-size-badge" style="font-size: 12.5px; font-weight: 700; color: #60a5fa; background: rgba(59, 130, 246, 0.18); border: 1px solid rgba(59,130,246,0.3); padding: 2px 9px; border-radius: 5px;">${{currentSettings.fontSize}}px</span>
                    </div>
                    <div style="display: flex; align-items: center; gap: 9px;">
                        <button id="ag-font-dec" style="width: 34px; height: 30px; background: #27272a; border: 1px solid rgba(255,255,255,0.15); color: #fff; border-radius: 7px; cursor: pointer; font-size: 16px; font-weight: 700; transition: background .15s;">-</button>
                        <input type="range" id="ag-font-size-slider" min="12" max="24" value="${{currentSettings.fontSize}}" step="1" style="flex: 1; accent-color: #3b82f6; cursor: pointer; height: 6px;">
                        <button id="ag-font-inc" style="width: 34px; height: 30px; background: #27272a; border: 1px solid rgba(255,255,255,0.15); color: #fff; border-radius: 7px; cursor: pointer; font-size: 16px; font-weight: 700; transition: background .15s;">+</button>
                    </div>
                </div>

                <!-- Line Height -->
                <div style="margin-bottom: 16px;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 7px;">
                        <span style="font-size: 13px; font-weight: 600; color: #e4e4e7;">Line Spacing:</span>
                    </div>
                    <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 7px;">
                        <button class="ag-lh-btn" data-lh="1.5" style="background: ${{currentSettings.lineHeight === 1.5 ? '#3b82f6' : '#27272a'}}; border: 1px solid ${{currentSettings.lineHeight === 1.5 ? '#3b82f6' : 'rgba(255,255,255,0.12)'}}; color: ${{currentSettings.lineHeight === 1.5 ? '#fff' : '#d4d4d8'}}; border-radius: 7px; padding: 6px 0; font-size: 12px; font-weight: 600; cursor: pointer; font-family: inherit; transition: all .15s;">Compact (1.5)</button>
                        <button class="ag-lh-btn" data-lh="1.75" style="background: ${{currentSettings.lineHeight === 1.75 ? '#3b82f6' : '#27272a'}}; border: 1px solid ${{currentSettings.lineHeight === 1.75 ? '#3b82f6' : 'rgba(255,255,255,0.12)'}}; color: ${{currentSettings.lineHeight === 1.75 ? '#fff' : '#d4d4d8'}}; border-radius: 7px; padding: 6px 0; font-size: 12px; font-weight: 600; cursor: pointer; font-family: inherit; transition: all .15s;">Normal (1.75)</button>
                        <button class="ag-lh-btn" data-lh="2.0" style="background: ${{currentSettings.lineHeight === 2.0 ? '#3b82f6' : '#27272a'}}; border: 1px solid ${{currentSettings.lineHeight === 2.0 ? '#3b82f6' : 'rgba(255,255,255,0.12)'}}; color: ${{currentSettings.lineHeight === 2.0 ? '#fff' : '#d4d4d8'}}; border-radius: 7px; padding: 6px 0; font-size: 12px; font-weight: 600; cursor: pointer; font-family: inherit; transition: all .15s;">Relaxed (2.0)</button>
                    </div>
                </div>

                <!-- Footer Actions -->
                <div style="display: flex; justify-content: space-between; align-items: center; border-top: 1px solid rgba(255,255,255,0.1); padding-top: 12px;">
                    <button id="ag-reset-defaults" style="background: transparent; border: none; color: #a1a1aa; font-size: 12px; font-weight: 500; cursor: pointer; padding: 5px 8px; border-radius: 6px; display: flex; align-items: center; gap: 5px; font-family: inherit; transition: color .15s;">
                        <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"/><path d="M3 3v5h5"/></svg>
                        <span>Reset Defaults</span>
                    </button>
                    <button id="ag-close-popover" style="background: #27272a; border: 1px solid rgba(255,255,255,0.18); color: #f4f4f5; font-size: 12px; font-weight: 600; cursor: pointer; padding: 6px 16px; border-radius: 7px; font-family: inherit; transition: background .15s;">
                        Close
                    </button>
                </div>
            `;

            document.body.appendChild(popoverInstance);

            const toggleBtn = popoverInstance.querySelector('#ag-toggle-rtl');
            const knob = popoverInstance.querySelector('#ag-toggle-knob');
            const statusBadge = popoverInstance.querySelector('#ag-rtl-status-badge');
            toggleBtn.onclick = () => {{
                currentSettings.rtlEnabled = !currentSettings.rtlEnabled;
                toggleBtn.style.background = currentSettings.rtlEnabled ? '#3b82f6' : '#3f3f46';
                knob.style.left = currentSettings.rtlEnabled ? '22px' : '4px';
                if (statusBadge) {{
                    statusBadge.style.background = currentSettings.rtlEnabled ? 'rgba(34, 197, 94, 0.2)' : 'rgba(161, 161, 170, 0.2)';
                    statusBadge.style.color = currentSettings.rtlEnabled ? '#4ade80' : '#a1a1aa';
                    statusBadge.textContent = currentSettings.rtlEnabled ? 'Enabled' : 'Disabled';
                }}
                applySettings(currentSettings);
                saveSettings(currentSettings);
            }};

            const digitsToggle = popoverInstance.querySelector('#ag-toggle-digits');
            const digitsKnob = popoverInstance.querySelector('#ag-digits-knob');
            const digitsBadge = popoverInstance.querySelector('#ag-digits-status-badge');
            digitsToggle.onclick = () => {{
                currentSettings.persianDigits = !currentSettings.persianDigits;
                digitsToggle.style.background = currentSettings.persianDigits ? '#3b82f6' : '#3f3f46';
                digitsKnob.style.left = currentSettings.persianDigits ? '22px' : '4px';
                if (digitsBadge) {{
                    digitsBadge.style.background = currentSettings.persianDigits ? 'rgba(34, 197, 94, 0.22)' : 'rgba(161, 161, 170, 0.2)';
                    digitsBadge.style.color = currentSettings.persianDigits ? '#4ade80' : '#a1a1aa';
                    digitsBadge.textContent = currentSettings.persianDigits ? '۰-۹ (Farsi)' : '0-9 (Latin)';
                }}
                applySettings(currentSettings);
                saveSettings(currentSettings);
            }};

            const justifyToggle = popoverInstance.querySelector('#ag-toggle-justify');
            const justifyKnob = popoverInstance.querySelector('#ag-justify-knob');
            const justifyBadge = popoverInstance.querySelector('#ag-justify-status-badge');
            justifyToggle.onclick = () => {{
                currentSettings.justifyText = !currentSettings.justifyText;
                justifyToggle.style.background = currentSettings.justifyText ? '#3b82f6' : '#3f3f46';
                justifyKnob.style.left = currentSettings.justifyText ? '22px' : '4px';
                if (justifyBadge) {{
                    justifyBadge.style.background = currentSettings.justifyText ? 'rgba(34, 197, 94, 0.22)' : 'rgba(161, 161, 170, 0.2)';
                    justifyBadge.style.color = currentSettings.justifyText ? '#4ade80' : '#a1a1aa';
                    justifyBadge.textContent = currentSettings.justifyText ? 'Enabled' : 'Disabled';
                }}
                applySettings(currentSettings);
                saveSettings(currentSettings);
            }};

            const proxyToggle = popoverInstance.querySelector('#ag-toggle-proxy');
            const proxyKnob = popoverInstance.querySelector('#ag-proxy-knob');
            const proxyBadge = popoverInstance.querySelector('#ag-proxy-status-badge');
            const proxyPanel = popoverInstance.querySelector('#ag-proxy-panel');
            const protoSocks5 = popoverInstance.querySelector('#ag-proto-socks5');
            const protoHttp = popoverInstance.querySelector('#ag-proto-http');
            const hostInput = popoverInstance.querySelector('#ag-proxy-host-input');
            const portInput = popoverInstance.querySelector('#ag-proxy-port-input');
            const testBtn = popoverInstance.querySelector('#ag-proxy-test-btn');
            const testResult = popoverInstance.querySelector('#ag-proxy-test-result');
            const testMsg = popoverInstance.querySelector('#ag-proxy-test-msg');
            const testLatency = popoverInstance.querySelector('#ag-proxy-test-latency');

            proxyToggle.onclick = () => {{
                currentSettings.proxyEnabled = !currentSettings.proxyEnabled;
                proxyToggle.style.background = currentSettings.proxyEnabled ? '#3b82f6' : '#3f3f46';
                proxyKnob.style.left = currentSettings.proxyEnabled ? '22px' : '4px';
                if (proxyBadge) {{
                    proxyBadge.style.background = currentSettings.proxyEnabled ? 'rgba(34, 197, 94, 0.22)' : 'rgba(161, 161, 170, 0.2)';
                    proxyBadge.style.color = currentSettings.proxyEnabled ? '#4ade80' : '#a1a1aa';
                    proxyBadge.textContent = currentSettings.proxyEnabled ? 'Enabled' : 'Disabled';
                }}
                proxyPanel.style.display = currentSettings.proxyEnabled ? 'block' : 'none';
                saveSettings(currentSettings);
                syncProxyConfigToFile(currentSettings);
                showRTLToast(currentSettings.proxyEnabled ? 'Proxy Shield: Enabled (Active on reload)' : 'Proxy Shield: Disabled');
            }};

            function updateProtoButtons(selectedType) {{
                currentSettings.proxyType = selectedType;
                if (protoSocks5 && protoHttp) {{
                    protoSocks5.style.background = (selectedType === 'socks5') ? '#3b82f6' : '#27272a';
                    protoSocks5.style.borderColor = (selectedType === 'socks5') ? '#3b82f6' : 'rgba(255,255,255,0.14)';
                    protoSocks5.style.color = (selectedType === 'socks5') ? '#fff' : '#d4d4d8';

                    protoHttp.style.background = (selectedType === 'http') ? '#3b82f6' : '#27272a';
                    protoHttp.style.borderColor = (selectedType === 'http') ? '#3b82f6' : 'rgba(255,255,255,0.14)';
                    protoHttp.style.color = (selectedType === 'http') ? '#fff' : '#d4d4d8';
                }}
                saveSettings(currentSettings);
                syncProxyConfigToFile(currentSettings);
            }}

            if (protoSocks5) protoSocks5.onclick = () => updateProtoButtons('socks5');
            if (protoHttp) protoHttp.onclick = () => updateProtoButtons('http');

            if (hostInput) {{
                hostInput.oninput = () => {{
                    currentSettings.proxyHost = hostInput.value.trim();
                    saveSettings(currentSettings);
                    syncProxyConfigToFile(currentSettings);
                }};
            }}

            if (portInput) {{
                portInput.oninput = () => {{
                    currentSettings.proxyPort = parseInt(portInput.value) || 10808;
                    saveSettings(currentSettings);
                    syncProxyConfigToFile(currentSettings);
                }};
            }}

            let testResetTimer = null;
            async function runConnectionTest() {{
                if (!testBtn || !testResult || !testMsg) return;
                const h = (hostInput ? hostInput.value : currentSettings.proxyHost) || '127.0.0.1';
                const p = parseInt(portInput ? portInput.value : currentSettings.proxyPort) || 10808;

                if (testResetTimer) clearTimeout(testResetTimer);

                testBtn.style.opacity = '0.7';
                testBtn.style.pointerEvents = 'none';
                testBtn.style.background = 'rgba(59, 130, 246, 0.2)';
                testBtn.style.borderColor = 'rgba(59, 130, 246, 0.45)';
                testBtn.style.color = '#93c5fd';
                testBtn.innerHTML = '<span>⏳ Checking...</span>';

                testResult.style.display = 'flex';
                testResult.style.background = 'rgba(59, 130, 246, 0.12)';
                testResult.style.border = '1px solid rgba(59, 130, 246, 0.3)';
                testMsg.style.color = '#93c5fd';
                testMsg.textContent = `Connecting to ${{h}}:${{p}}...`;
                testLatency.style.color = '#93c5fd';
                testLatency.textContent = '...';

                try {{
                    const testStartTime = Date.now();
                    const res = await testProxyConnection(h, p, currentSettings.proxyType, 2000);
                    const elapsed = Date.now() - testStartTime;
                    if (elapsed < 350) {{
                        await new Promise(r => setTimeout(r, 350 - elapsed));
                    }}

                    testResult.style.display = 'flex';
                    if (res.ok) {{
                        testBtn.innerHTML = '<span>✅ Active</span>';
                        testBtn.style.background = 'rgba(34, 197, 94, 0.25)';
                        testBtn.style.borderColor = 'rgba(34, 197, 94, 0.5)';
                        testBtn.style.color = '#4ade80';

                        testResult.style.background = 'rgba(34, 197, 94, 0.15)';
                        testResult.style.border = '1px solid rgba(34, 197, 94, 0.35)';
                        testMsg.style.color = '#4ade80';
                        testMsg.textContent = `● ${{res.msg}}`;
                        testLatency.style.color = '#86efac';
                        testLatency.textContent = `${{res.latency}}ms`;

                        showRTLToast(`✅ Proxy Shield: Port ${{p}} is reachable (${{res.latency}}ms)`);
                    }} else {{
                        testBtn.innerHTML = '<span>❌ Offline</span>';
                        testBtn.style.background = 'rgba(239, 68, 68, 0.25)';
                        testBtn.style.borderColor = 'rgba(239, 68, 68, 0.5)';
                        testBtn.style.color = '#f87171';

                        testResult.style.background = 'rgba(239, 68, 68, 0.15)';
                        testResult.style.border = '1px solid rgba(239, 68, 68, 0.35)';
                        testMsg.style.color = '#f87171';
                        testMsg.textContent = `○ ${{res.msg}}`;
                        testLatency.style.color = '#fca5a5';
                        testLatency.textContent = 'offline';

                        showRTLToast(`❌ Proxy Shield: Port ${{p}} is unreachable`);
                    }}
                }} catch(err) {{
                    testBtn.innerHTML = '<span>❌ Error</span>';
                    testBtn.style.background = 'rgba(239, 68, 68, 0.25)';
                    testBtn.style.borderColor = 'rgba(239, 68, 68, 0.5)';
                    testBtn.style.color = '#f87171';

                    testResult.style.display = 'flex';
                    testResult.style.background = 'rgba(239, 68, 68, 0.15)';
                    testResult.style.border = '1px solid rgba(239, 68, 68, 0.35)';
                    testMsg.style.color = '#f87171';
                    testMsg.textContent = `○ Error: ${{err.message || 'Check failed'}}`;
                    testLatency.textContent = '';

                    showRTLToast(`❌ Proxy Error: ${{err.message || 'Check failed'}}`);
                }} finally {{
                    testResetTimer = setTimeout(() => {{
                        if (testBtn) {{
                            testBtn.style.opacity = '1';
                            testBtn.style.pointerEvents = 'auto';
                            testBtn.style.background = 'rgba(59, 130, 246, 0.2)';
                            testBtn.style.borderColor = 'rgba(59, 130, 246, 0.45)';
                            testBtn.style.color = '#60a5fa';
                            testBtn.innerHTML = '<span>⚡ Test</span>';
                        }}
                    }}, 2200);
                }}
            }}

            if (testBtn) testBtn.onclick = runConnectionTest;

            popoverInstance.querySelectorAll('.ag-proxy-preset-btn').forEach(btnEl => {{
                btnEl.onclick = () => {{
                    const presetType = btnEl.getAttribute('data-type');
                    const presetPort = parseInt(btnEl.getAttribute('data-port'));
                    if (portInput) portInput.value = presetPort;
                    currentSettings.proxyPort = presetPort;
                    updateProtoButtons(presetType);
                    runConnectionTest();
                }};
            }});

            const fontSelect = popoverInstance.querySelector('#ag-font-family-select');
            const fontBadge = popoverInstance.querySelector('#ag-font-family-badge');
            const customContainer = popoverInstance.querySelector('#ag-custom-font-container');
            const customInput = popoverInstance.querySelector('#ag-custom-font-input');

            const codeSelect = popoverInstance.querySelector('#ag-code-font-select');
            const codeBadge = popoverInstance.querySelector('#ag-code-font-badge');
            const customCodeContainer = popoverInstance.querySelector('#ag-custom-code-font-container');
            const customCodeInput = popoverInstance.querySelector('#ag-custom-code-font-input');

            const FONT_BASE_LABELS = {{
                'Vazirmatn': 'Vazirmatn (Default)',
                'Inter': 'Inter',
                'IRANSans': 'IRANSans',
                'IRANYekan': 'IRANYekan',
                'Dana': 'Dana',
                'BNazanin': 'B Nazanin',
                'Arad': 'Arad',
                'Shabnam': 'Shabnam',
                'Sahel': 'Sahel',
                'Samim': 'Samim',
                'Tahoma': 'Tahoma',
                'System': 'System Font',
                'Custom': 'Custom Font...'
            }};

            const CODE_FONT_BASE_LABELS = {{
                'JetBrains Mono': 'JetBrains Mono (Default)',
                'Consolas': 'Consolas',
                'Fira Code': 'Fira Code',
                'Cascadia Code': 'Cascadia Code',
                'Vazirmatn': 'Vazir Code',
                'Custom': 'Custom Monospace...'
            }};

            function updateOptionLabels(selectEl, labelMap) {{
                if (!selectEl) return;
                Array.from(selectEl.options).forEach(opt => {{
                    const val = opt.value;
                    if (val === 'Custom') {{
                        opt.textContent = '⚙️ ' + (labelMap[val] || val);
                        return;
                    }}
                    const status = getFontStatus(val);
                    const baseLabel = labelMap[val] || val;
                    if (status === 'bundled') {{
                        opt.textContent = `● ${{baseLabel}} (Bundled)`;
                    }} else if (status === 'installed') {{
                        opt.textContent = `● ${{baseLabel}} (Installed)`;
                    }} else {{
                        opt.textContent = `○ ${{baseLabel}} (Not installed)`;
                    }}
                }});
            }}

            function updateFontBadge(badgeEl, fontVal, customVal) {{
                if (!badgeEl) return;
                const target = (fontVal === 'Custom') ? (customVal || '').trim() : fontVal;
                if (!target) {{
                    badgeEl.style.background = 'rgba(161, 161, 170, 0.2)';
                    badgeEl.style.color = '#a1a1aa';
                    badgeEl.textContent = '○ None specified';
                    return;
                }}
                const status = getFontStatus(target);
                if (status === 'bundled') {{
                    badgeEl.style.background = 'rgba(34, 197, 94, 0.22)';
                    badgeEl.style.color = '#4ade80';
                    badgeEl.textContent = '● Bundled (Ready)';
                }} else if (status === 'installed') {{
                    badgeEl.style.background = 'rgba(59, 130, 246, 0.22)';
                    badgeEl.style.color = '#60a5fa';
                    badgeEl.textContent = '● Installed on OS';
                }} else {{
                    badgeEl.style.background = 'rgba(239, 68, 68, 0.2)';
                    badgeEl.style.color = '#f87171';
                    badgeEl.textContent = '○ Not installed (Fallback)';
                }}
            }}

            updateOptionLabels(fontSelect, FONT_BASE_LABELS);
            updateOptionLabels(codeSelect, CODE_FONT_BASE_LABELS);
            updateFontBadge(fontBadge, currentSettings.fontFamily, currentSettings.customFont);
            updateFontBadge(codeBadge, currentSettings.codeFont, currentSettings.customCodeFont);

            fontSelect.onchange = () => {{
                currentSettings.fontFamily = fontSelect.value;
                if (fontSelect.value === 'Custom') {{
                    customContainer.style.display = 'block';
                    customInput.focus();
                }} else {{
                    customContainer.style.display = 'none';
                }}
                updateFontBadge(fontBadge, currentSettings.fontFamily, currentSettings.customFont);
                applySettings(currentSettings);
                saveSettings(currentSettings);
            }};

            customInput.oninput = () => {{
                currentSettings.customFont = customInput.value.trim();
                updateFontBadge(fontBadge, currentSettings.fontFamily, currentSettings.customFont);
                applySettings(currentSettings);
                saveSettings(currentSettings);
            }};

            codeSelect.onchange = () => {{
                currentSettings.codeFont = codeSelect.value;
                if (codeSelect.value === 'Custom') {{
                    customCodeContainer.style.display = 'block';
                    customCodeInput.focus();
                }} else {{
                    customCodeContainer.style.display = 'none';
                }}
                updateFontBadge(codeBadge, currentSettings.codeFont, currentSettings.customCodeFont);
                applySettings(currentSettings);
                saveSettings(currentSettings);
            }};

            customCodeInput.oninput = () => {{
                currentSettings.customCodeFont = customCodeInput.value.trim();
                updateFontBadge(codeBadge, currentSettings.codeFont, currentSettings.customCodeFont);
                applySettings(currentSettings);
                saveSettings(currentSettings);
            }};

            const sizeSlider = popoverInstance.querySelector('#ag-font-size-slider');
            const sizeBadge = popoverInstance.querySelector('#ag-font-size-badge');
            const decBtn = popoverInstance.querySelector('#ag-font-dec');
            const incBtn = popoverInstance.querySelector('#ag-font-inc');

            function updateFontSize(val) {{
                val = Math.max(12, Math.min(24, parseInt(val) || 15));
                currentSettings.fontSize = val;
                sizeSlider.value = val;
                sizeBadge.textContent = val + 'px';
                applySettings(currentSettings);
                saveSettings(currentSettings);
            }}

            sizeSlider.oninput = () => updateFontSize(sizeSlider.value);
            decBtn.onclick = () => updateFontSize(currentSettings.fontSize - 1);
            incBtn.onclick = () => updateFontSize(currentSettings.fontSize + 1);

            const lhButtons = popoverInstance.querySelectorAll('.ag-lh-btn');
            function updateLineHeightUI(lh) {{
                lhButtons.forEach(btnEl => {{
                    const isMatch = parseFloat(btnEl.getAttribute('data-lh')) === lh;
                    btnEl.style.background = isMatch ? '#3b82f6' : '#27272a';
                    btnEl.style.borderColor = isMatch ? '#3b82f6' : 'rgba(255,255,255,0.12)';
                    btnEl.style.color = isMatch ? '#fff' : '#d4d4d8';
                }});
            }}

            lhButtons.forEach(b => {{
                b.onclick = () => {{
                    const lh = parseFloat(b.getAttribute('data-lh'));
                    currentSettings.lineHeight = lh;
                    updateLineHeightUI(lh);
                    applySettings(currentSettings);
                    saveSettings(currentSettings);
                }};
            }});
            popoverInstance.querySelector('#ag-close-popover').onclick = closePopover;
            popoverInstance.querySelector('#ag-reset-defaults').onclick = () => {{
                currentSettings = Object.assign({{}}, DEFAULT_SETTINGS);
                saveSettings(currentSettings);
                applySettings(currentSettings);
                syncProxyConfigToFile(currentSettings);
                closePopover();
                openPopover();
            }};

            setTimeout(() => {{
                function onDocClick(e) {{
                    if (!popoverInstance) {{
                        document.removeEventListener('click', onDocClick);
                        return;
                    }}
                    if (!popoverInstance.contains(e.target) && !btn.contains(e.target)) {{
                        closePopover();
                        document.removeEventListener('click', onDocClick);
                    }}
                }}
                document.addEventListener('click', onDocClick);
            }}, 10);
        }}

        btn.onclick = (e) => {{
            e.stopPropagation();
            if (popoverInstance) closePopover();
            else openPopover();
        }};
    }}

    function showRTLToast(msg) {{
        let toast = document.getElementById('ag-rtl-toast');
        if (!toast) {{
            toast = document.createElement('div');
            toast.id = 'ag-rtl-toast';
            toast.style.cssText = 'position:fixed;bottom:32px;left:50%;transform:translateX(-50%);background:rgba(24,24,27,0.92);backdrop-filter:blur(16px);-webkit-backdrop-filter:blur(16px);color:#f4f4f5;border:1px solid rgba(255,255,255,0.2);padding:9px 22px;border-radius:10px;font-size:13.5px;font-weight:600;letter-spacing:0.3px;z-index:999999;box-shadow:0 12px 35px rgba(0,0,0,0.6);font-family:inherit;pointer-events:none;transition:opacity .25s ease,transform .25s ease;opacity:0;';
            document.body.appendChild(toast);
        }}
        toast.textContent = msg;
        toast.style.opacity = '1';
        toast.style.transform = 'translateX(-50%) translateY(0)';
        setTimeout(() => {{
            if (toast) {{
                toast.style.opacity = '0';
                toast.style.transform = 'translateX(-50%) translateY(6px)';
            }}
        }}, 1800);
    }}

    window.addEventListener('keydown', (e) => {{
        if (e.altKey && (e.key === 'r' || e.key === 'R' || e.code === 'KeyR')) {{
            e.preventDefault();
            currentSettings.rtlEnabled = !currentSettings.rtlEnabled;
            saveSettings(currentSettings);
            applySettings(currentSettings);
            showRTLToast(currentSettings.rtlEnabled ? 'Smart RTL: Enabled' : 'Smart RTL: Disabled');
        }}
    }});

    function initAll() {{
        const override = document.getElementById('ag-rtl-disable-override');
        if (override) override.remove();

        applySettings(currentSettings);
        syncProxyConfigToFile(currentSettings);
        initAppearanceMenu();

        if (!document.getElementById('ag-appearance-menu-btn')) {{
            let retries = 0;
            if (window.__ag_appearance_interval__) clearInterval(window.__ag_appearance_interval__);
            window.__ag_appearance_interval__ = setInterval(() => {{
                retries++;
                initAppearanceMenu();
                if (document.getElementById('ag-appearance-menu-btn') || retries > 15) {{
                    clearInterval(window.__ag_appearance_interval__);
                    window.__ag_appearance_interval__ = null;
                }}
            }}, 500);
        }}
    }}

    if (document.readyState === 'loading') {{
        document.addEventListener('DOMContentLoaded', initAll);
    }} else {{
        initAll();
    }}

    // --- Dynamic Observer for Chat Messages & Title Bar ---
    let scheduled = false;
    const pendingNodes = new Set();
    const flushPending = () => {{
        scheduled = false;
        const nodes = Array.from(pendingNodes);
        pendingNodes.clear();
        for (let i = 0; i < nodes.length; i++) {{
            const node = nodes[i];
            if (node && node.nodeType === 1) {{
                applySmartDirectionToElement(node);
                processAllSmartRTL(node);
            }}
        }}
    }};

    const observer = new MutationObserver((mutations) => {{
        if (!document.getElementById('ag-appearance-menu-btn')) {{
            initAppearanceMenu();
        }}
        if (document.body && document.body.classList.contains('ag-rtl-disabled')) return;
        for (let i = 0; i < mutations.length; i++) {{
            const mut = mutations[i];
            if (mut.type === 'childList') {{
                for (let j = 0; j < mut.addedNodes.length; j++) {{
                    const n = mut.addedNodes[j];
                    if (n && n.nodeType === 1) pendingNodes.add(n);
                }}
            }} else if (mut.type === 'characterData') {{
                const p = mut.target.parentElement;
                if (p && p.nodeType === 1) pendingNodes.add(p);
            }}
        }}
        if (!scheduled && pendingNodes.size > 0) {{
            scheduled = true;
            requestAnimationFrame(flushPending);
        }}
    }});

    function startObserver() {{
        if (document.body) {{
            observer.observe(document.body, {{ childList: true, subtree: true, characterData: true }});
            processAllSmartRTL(document.body);
        }} else {{
            setTimeout(startObserver, 50);
        }}
    }}

    startObserver();
}})();
}} catch(e) {{
    console.error("[Antigravity-RTL] Injection error:", e);
}}
"""

    @classmethod
    def get_updater_hook(cls) -> str:
        """
        Builds the hook snippet injected into dist/updater.js to survive auto-updates.
        """
        return """
    /* __ANTIGRAVITY_UPDATE_HOOK__ */
    try {
        const cp = require("child_process");
        const path = require("path");
        const fs = require("fs");
        const appData = process.env.APPDATA || "";
        const appDataPatch = path.join(appData, "Antigravity", "rtl-patch", "patcher.py");
        const resPatch = path.join(process.resourcesPath, "rtl-patch", "patcher.py");
        const patchPy = fs.existsSync(appDataPatch) ? appDataPatch : resPatch;
        const patchJs = patchPy.replace(/\\.py$/, ".js");
        const patchBat = path.join(path.dirname(patchPy), "patch.bat");

        try {
            cp.spawn("pythonw.exe", [patchPy, "--wait-for-update"], { detached: true, stdio: "ignore" }).unref();
        } catch(e1) {
            try {
                cp.spawn("node.exe", [patchJs, "--wait-for-update"], { detached: true, stdio: "ignore" }).unref();
            } catch(e2) {
                try {
                    cp.spawn(patchBat, ["--wait-for-update"], { detached: true, stdio: "ignore", shell: true }).unref();
                } catch(e3) {}
            }
        }
    } catch(e) {}
    """
