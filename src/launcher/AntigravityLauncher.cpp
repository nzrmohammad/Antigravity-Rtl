// Antigravity Auto-Shield Background Launcher
// Compiles with MSVC (cl /O2 AntigravityLauncher.cpp) or MinGW (g++ -O2 -mwindows AntigravityLauncher.cpp -o AntigravityLauncher.exe)

#define WIN32_LEAN_AND_MEAN
#include <windows.h>
#include <shellapi.h>
#include <string>
#include <vector>

bool FileExists(const std::wstring& path) {
    DWORD attr = GetFileAttributesW(path.c_str());
    return (attr != INVALID_FILE_ATTRIBUTES && !(attr & FILE_ATTRIBUTE_DIRECTORY));
}

bool DirExists(const std::wstring& path) {
    DWORD attr = GetFileAttributesW(path.c_str());
    return (attr != INVALID_FILE_ATTRIBUTES && (attr & FILE_ATTRIBUTE_DIRECTORY));
}

std::wstring GetExecutableDir() {
    wchar_t buffer[MAX_PATH];
    GetModuleFileNameW(NULL, buffer, MAX_PATH);
    std::wstring path(buffer);
    size_t pos = path.find_last_of(L"\\/");
    return (pos != std::string::npos) ? path.substr(0, pos) : L"";
}

void TriggerSilentPatch(const std::wstring& appDir) {
    // Look for persistent patcher in resources\rtl-patch or %APPDATA%\Antigravity\rtl-patch
    std::wstring patchBat = appDir + L"\\resources\\rtl-patch\\patch.bat";
    if (!FileExists(patchBat)) {
        wchar_t appData[MAX_PATH];
        if (GetEnvironmentVariableW(L"APPDATA", appData, MAX_PATH) > 0) {
            patchBat = std::wstring(appData) + L"\\Antigravity\\rtl-patch\\patch.bat";
        }
    }

    if (FileExists(patchBat)) {
        std::wstring cmd = L"\"" + patchBat + L"\" --no-kill";
        STARTUPINFOW si = { sizeof(STARTUPINFOW) };
        PROCESS_INFORMATION pi = {};
        si.dwFlags = STARTF_USESHOWWINDOW;
        si.wShowWindow = SW_HIDE;
        
        std::vector<wchar_t> cmdBuf(cmd.begin(), cmd.end());
        cmdBuf.push_back(0);

        if (CreateProcessW(NULL, cmdBuf.data(), NULL, NULL, FALSE, CREATE_NO_WINDOW, NULL, NULL, &si, &pi)) {
            CloseHandle(pi.hThread);
            CloseHandle(pi.hProcess);
        }
    }
}

int WINAPI WinMain(HINSTANCE hInstance, HINSTANCE hPrevInstance, LPSTR lpCmdLine, int nCmdShow) {
    std::wstring appDir = GetExecutableDir();
    std::wstring realExe = appDir + L"\\Antigravity.exe";

    if (!FileExists(realExe)) {
        MessageBoxW(NULL, 
            L"Could not locate original Antigravity.exe in the installation directory.",
            L"Antigravity Launcher Error", MB_ICONERROR | MB_OK);
        return 1;
    }

    // Trigger update-healing background check
    TriggerSilentPatch(appDir);

    // Forward command line arguments directly to Antigravity.exe
    LPWSTR fullCmdLine = GetCommandLineW();
    STARTUPINFOW si = { sizeof(STARTUPINFOW) };
    PROCESS_INFORMATION pi = {};
    GetStartupInfoW(&si);

    std::wstring targetCmd = L"\"" + realExe + L"\"";
    // Append arguments if present
    int argc = 0;
    LPWSTR* argv = CommandLineToArgvW(fullCmdLine, &argc);
    if (argv && argc > 1) {
        for (int i = 1; i < argc; ++i) {
            targetCmd += L" \"";
            targetCmd += argv[i];
            targetCmd += L"\"";
        }
        LocalFree(argv);
    }

    std::vector<wchar_t> cmdBuf(targetCmd.begin(), targetCmd.end());
    cmdBuf.push_back(0);

    if (CreateProcessW(realExe.c_str(), cmdBuf.data(), NULL, NULL, FALSE, 0, NULL, appDir.c_str(), &si, &pi)) {
        CloseHandle(pi.hThread);
        CloseHandle(pi.hProcess);
        return 0;
    } else {
        MessageBoxW(NULL, L"Failed to start Antigravity.exe.", L"Antigravity Launcher Error", MB_ICONERROR | MB_OK);
        return 1;
    }
}
