# Antigravity Auto-Shield Launcher Source

This directory contains the transparent C++ source code for `AntigravityLauncher.exe`.

## Purpose
`AntigravityLauncher.exe` is an optional helper executable placed in the Antigravity installation folder when `--install-shortcuts` is selected. It ensures that:
1. When Antigravity automatically updates, the launcher detects whether the new `app.asar` has been patched.
2. It silently triggers the background patcher to re-apply RTL and custom typography without interrupting the user.
3. It immediately forwards all CLI arguments and executes the real `Antigravity.exe`.

## Build Instructions

### With MinGW GCC:
```bash
g++ -O2 -mwindows AntigravityLauncher.cpp -o ../AntigravityLauncher.exe
```

### With MSVC (Visual Studio Developer Command Prompt):
```cmd
cl /O2 /Fe:..\AntigravityLauncher.exe AntigravityLauncher.cpp /link /SUBSYSTEM:WINDOWS
```
