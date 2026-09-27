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
        lineHeight: 1.75
    }};

    function getSettings() {{
        try {{
            const raw = localStorage.getItem(STORAGE_KEY);
            if (raw) return Object.assign({{}}, DEFAULT_SETTINGS, JSON.parse(raw));
        }} catch(e) {{}}
        return Object.assign({{}}, DEFAULT_SETTINGS);
    }}

    function saveSettings(s) {{
        try {{
            localStorage.setItem(STORAGE_KEY, JSON.stringify(s));
        }} catch(e) {{}}
    }}

    let currentSettings = getSettings();

    function getFontFamilyValue(fontName, customName) {{
        switch(fontName) {{
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
                return (customName ? `'${{customName}}', ` : "") + "'Vazirmatn', sans-serif";
            case 'Vazirmatn':
            default:
                return "'Vazirmatn', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif";
        }}
    }}

    function applySettings(s) {{
        if (!document.documentElement) return;
        const root = document.documentElement;
        root.style.setProperty('--ag-font-size', s.fontSize + 'px');
        root.style.setProperty('--ag-line-height', s.lineHeight.toString());
        root.style.setProperty('--ag-font-family', getFontFamilyValue(s.fontFamily, s.customFont));

        if (!document.body) return;
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
                left: ${{Math.min(rect.left, window.innerWidth - 345)}}px;
                width: 335px;
                background: rgba(22, 22, 26, 0.96);
                backdrop-filter: blur(20px);
                -webkit-backdrop-filter: blur(20px);
                border: 1px solid rgba(255, 255, 255, 0.15);
                color: #f4f4f5;
                font-family: 'Vazirmatn', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                direction: rtl;
                padding: 16px;
                border-radius: 14px;
                box-shadow: 0 25px 60px -10px rgba(0, 0, 0, 0.8), 0 0 0 1px rgba(255, 255, 255, 0.08);
                z-index: 999999;
                user-select: none;
            `;

            popoverInstance.innerHTML = `
                <div style="display: flex; align-items: center; justify-content: space-between; border-bottom: 1px solid rgba(255,255,255,0.1); padding-bottom: 12px; margin-bottom: 14px;">
                    <div style="display: flex; align-items: center; gap: 8px;">
                        <span style="font-size: 15px; font-weight: 700; color: #fff; letter-spacing: 0.2px;">Appearance & Smart RTL</span>
                    </div>
                    <span style="font-size: 11px; padding: 2px 8px; background: rgba(59, 130, 246, 0.22); color: #60a5fa; border: 1px solid rgba(59, 130, 246, 0.35); border-radius: 5px; font-weight: 600;">v1.0</span>
                </div>

                <!-- RTL Toggle -->
                <div style="display: flex; align-items: center; justify-content: space-between; background: rgba(255,255,255,0.04); padding: 11px 14px; border-radius: 10px; margin-bottom: 14px; border: 1px solid rgba(255,255,255,0.08);">
                    <div>
                        <div style="font-size: 13.5px; font-weight: 600; color: #fff; display: flex; align-items: center; gap: 7px;">
                            <span>Smart RTL</span>
                            <span id="ag-rtl-status-badge" style="font-size: 11px; padding: 2px 7px; border-radius: 4px; font-weight: 600; background: ${{currentSettings.rtlEnabled ? 'rgba(34, 197, 94, 0.22)' : 'rgba(161, 161, 170, 0.2)'}}; color: ${{currentSettings.rtlEnabled ? '#4ade80' : '#a1a1aa'}};">${{currentSettings.rtlEnabled ? 'Enabled' : 'Disabled'}}</span>
                        </div>
                        <div style="font-size: 11.5px; color: #a1a1aa; margin-top: 3px;">Auto-direction & Persian fonts (Alt+R)</div>
                    </div>
                    <div id="ag-toggle-rtl" style="width: 46px; height: 26px; background: ${{currentSettings.rtlEnabled ? '#3b82f6' : '#3f3f46'}}; border-radius: 13px; position: relative; cursor: pointer; transition: background .2s; box-shadow: inset 0 2px 4px rgba(0,0,0,0.3);">
                        <div id="ag-toggle-knob" style="position: absolute; width: 20px; height: 20px; background: white; border-radius: 50%; top: 3px; right: ${{currentSettings.rtlEnabled ? '4px' : '22px'}}; transition: right .2s; box-shadow: 0 2px 4px rgba(0,0,0,0.3);"></div>
                    </div>
                </div>

                <!-- Font Family Selection -->
                <div style="margin-bottom: 14px;">
                    <label style="display: block; font-size: 13px; font-weight: 600; color: #e4e4e7; margin-bottom: 7px;">Font Family:</label>
                    <select id="ag-font-family-select" style="width: 100%; background: #27272a; color: #f4f4f5; border: 1px solid rgba(255,255,255,0.18); border-radius: 8px; padding: 7px 11px; font-size: 13px; font-weight: 500; outline: none; font-family: inherit; cursor: pointer; transition: border-color .15s;">
                        <option value="Vazirmatn" ${{currentSettings.fontFamily === 'Vazirmatn' ? 'selected' : ''}}>Vazirmatn (Default)</option>
                        <option value="Shabnam" ${{currentSettings.fontFamily === 'Shabnam' ? 'selected' : ''}}>Shabnam</option>
                        <option value="Sahel" ${{currentSettings.fontFamily === 'Sahel' ? 'selected' : ''}}>Sahel</option>
                        <option value="Samim" ${{currentSettings.fontFamily === 'Samim' ? 'selected' : ''}}>Samim</option>
                        <option value="Tahoma" ${{currentSettings.fontFamily === 'Tahoma' ? 'selected' : ''}}>Tahoma</option>
                        <option value="System" ${{currentSettings.fontFamily === 'System' ? 'selected' : ''}}>System Font</option>
                        <option value="Custom" ${{currentSettings.fontFamily === 'Custom' ? 'selected' : ''}}>Custom Font...</option>
                    </select>
                    <div id="ag-custom-font-container" style="display: ${{currentSettings.fontFamily === 'Custom' ? 'block' : 'none'}}; margin-top: 7px;">
                        <input type="text" id="ag-custom-font-input" placeholder="Font name (e.g. Dana, B Yekan)" value="${{currentSettings.customFont || ''}}" style="width: 100%; background: #1f1f23; color: #fff; border: 1px solid rgba(59,130,246,0.5); border-radius: 8px; padding: 7px 10px; font-size: 12.5px; outline: none; box-sizing: border-box;">
                    </div>
                </div>

                <!-- Font Size Stepper & Slider -->
                <div style="margin-bottom: 14px;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 7px;">
                        <span style="font-size: 13px; font-weight: 600; color: #e4e4e7;">Font Size:</span>
                        <span id="ag-font-size-badge" style="font-size: 12.5px; font-weight: 700; color: #60a5fa; background: rgba(59, 130, 246, 0.18); border: 1px solid rgba(59,130,246,0.3); padding: 2px 9px; border-radius: 5px; direction: ltr;">${{currentSettings.fontSize}}px</span>
                    </div>
                    <div style="display: flex; align-items: center; gap: 9px; direction: ltr;">
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
                knob.style.right = currentSettings.rtlEnabled ? '4px' : '22px';
                if (statusBadge) {{
                    statusBadge.style.background = currentSettings.rtlEnabled ? 'rgba(34, 197, 94, 0.2)' : 'rgba(161, 161, 170, 0.2)';
                    statusBadge.style.color = currentSettings.rtlEnabled ? '#4ade80' : '#a1a1aa';
                    statusBadge.textContent = currentSettings.rtlEnabled ? 'Enabled' : 'Disabled';
                }}
                applySettings(currentSettings);
                saveSettings(currentSettings);
            }};

            const fontSelect = popoverInstance.querySelector('#ag-font-family-select');
            const customContainer = popoverInstance.querySelector('#ag-custom-font-container');
            const customInput = popoverInstance.querySelector('#ag-custom-font-input');
            fontSelect.onchange = () => {{
                currentSettings.fontFamily = fontSelect.value;
                if (fontSelect.value === 'Custom') {{
                    customContainer.style.display = 'block';
                    customInput.focus();
                }} else {{
                    customContainer.style.display = 'none';
                }}
                applySettings(currentSettings);
                saveSettings(currentSettings);
            }};

            customInput.oninput = () => {{
                currentSettings.customFont = customInput.value.trim();
                applySettings(currentSettings);
                saveSettings(currentSettings);
            }};

            const sizeSlider = popoverInstance.querySelector('#ag-font-size-slider');
            const sizeBadge = popoverInstance.querySelector('#ag-font-size-badge');
            const decBtn = popoverInstance.querySelector('#ag-font-dec');
            const incBtn = popoverInstance.querySelector('#ag-font-inc');

            function updateFontSize(val) {{
                val = Math.max(12, Math.min(22, parseInt(val) || 15));
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
            lhButtons.forEach(b => {{
                b.onclick = () => {{
                    const lh = parseFloat(b.getAttribute('data-lh'));
                    currentSettings.lineHeight = lh;
                    lhButtons.forEach(btnEl => {{
                        const isMatch = parseFloat(btnEl.getAttribute('data-lh')) === lh;
                        btnEl.style.background = isMatch ? '#3b82f6' : '#27272a';
                        btnEl.style.borderColor = isMatch ? '#3b82f6' : 'rgba(255,255,255,0.12)';
                        btnEl.style.color = isMatch ? '#fff' : '#d4d4d8';
                    }});
                    applySettings(currentSettings);
                    saveSettings(currentSettings);
                }};
            }});

            popoverInstance.querySelector('#ag-close-popover').onclick = closePopover;
            popoverInstance.querySelector('#ag-reset-defaults').onclick = () => {{
                currentSettings = Object.assign({{}}, DEFAULT_SETTINGS);
                saveSettings(currentSettings);
                applySettings(currentSettings);
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
