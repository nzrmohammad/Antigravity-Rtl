# Antigravity RTL - Anti-Sanction & Proxy Shield Binaries

This directory contains verified native binaries and configuration templates used strictly for the **Anti-Sanction & Proxy Shield** capability.

## 📦 Binary Metadata & Cryptographic Identity

| Attribute | Specification |
|---|---|
| **Binary Filename** | `version.dll` |
| **Target Architecture** | Windows x86_64 (64-bit) |
| **Upstream Project** | [yuaotian/antigravity-proxy](https://github.com/yuaotian/antigravity-proxy) |
| **Upstream Release** | v2.4 (Official Release Build) |
| **Original Upstream Author** | yuaotian |
| **License** | [MIT License](https://github.com/yuaotian/antigravity-proxy/blob/main/LICENSE) |
| **SHA-256 Checksum** | `40f037232a180da8dff7611021270549fcc4e208580d8bf0f70bc9975f871b5f` |
| **File Size** | 632,320 bytes |

---

## 🛡️ Operating Mechanism (Windows DLL Proxying)

The Antigravity desktop client runs on Electron, launching several background child processes (such as `agy.exe`, `language_server.exe`, and worker Node.js instances). Because these child processes frequently do not inherit Electron Chromium network proxy flags or environment variables (`HTTP_PROXY`/`HTTPS_PROXY`), developers in sanctioned regions encounter `403 Forbidden` and `400 Bad Request` network connection failures from Google APIs.

`version.dll` utilizes standard Windows **DLL proxying / side-loading**:
1. When `Antigravity.exe` executes, the Windows PE loader searches the application folder for `version.dll`.
2. It forwards all official Windows Version API calls (`GetFileVersionInfoA`, `VerQueryValueW`, etc.) to the real system `C:\Windows\System32\version.dll`.
3. It hooks socket creation (`connect`, `send`, `recv`) within language server and worker processes to route external Google API requests through the user's configured local proxy (e.g. SOCKS5 on `127.0.0.1:10808`).
4. **Strict Opt-In**: This binary is **never** copied or installed during the standard RTL typography patch. It is deployed **only** when the user explicitly enables Proxy Shield via `--proxy`, the interactive menu Option 5, or the in-app Appearance menu.

---

## 🔒 Security & Verification

Before copying `version.dll` to the Antigravity application directory, `ProxyManager.install()` cryptographically validates the file against `PROXY_VERSION_DLL_SHA256`:

```python
import hashlib
from antigravity_rtl.constants import PROXY_VERSION_DLL_SHA256

def verify_dll(path: str) -> bool:
    with open(path, "rb") as f:
        digest = hashlib.sha256(f.read()).hexdigest()
    return digest == PROXY_VERSION_DLL_SHA256
```

If the checksum does not match, the installation is aborted immediately with a `SecurityError`.
