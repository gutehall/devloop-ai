"""Cross-platform clipboard and Cursor launch. Supports macOS, Linux, Windows."""
import os
import platform
import subprocess

_sys = platform.system()


def copy_to_clipboard(text: str) -> bool:
    """Copy text to clipboard. Returns True on success, False otherwise."""
    # Try pyperclip first
    try:
        import pyperclip
        pyperclip.copy(text)
        return True
    except ImportError:
        pass
    except Exception:
        pass

    # Fallback: platform-specific subprocess
    if _sys == "Darwin":
        try:
            p = subprocess.Popen(["pbcopy"], stdin=subprocess.PIPE)
            p.communicate(text.encode("utf-8"))
            return p.returncode == 0
        except FileNotFoundError:
            pass
    elif _sys == "Linux":
        for cmd in (
            ["xclip", "-selection", "clipboard"],
            ["xsel", "--clipboard", "--input"],
            ["wl-copy"],
        ):
            try:
                p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
                p.communicate(text.encode("utf-8"))
                return p.returncode == 0
            except FileNotFoundError:
                continue
    elif _sys == "Windows":
        try:
            p = subprocess.Popen(["clip"], stdin=subprocess.PIPE)
            p.communicate(text.encode("utf-16le"))
            return p.returncode == 0
        except FileNotFoundError:
            pass

    return False


def paste_from_clipboard() -> str:
    """Paste from clipboard. Returns empty string on failure."""
    # Try pyperclip first
    try:
        import pyperclip
        return pyperclip.paste()
    except ImportError:
        pass
    except Exception:
        pass

    # Fallback: platform-specific subprocess
    if _sys == "Darwin":
        try:
            return subprocess.check_output(["pbpaste"], text=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            pass
    elif _sys == "Linux":
        for cmd in (
            ["xclip", "-selection", "clipboard", "-o"],
            ["xsel", "--clipboard", "--output"],
            ["wl-paste"],
        ):
            try:
                return subprocess.check_output(cmd, text=True)
            except (subprocess.CalledProcessError, FileNotFoundError):
                continue
    elif _sys == "Windows":
        try:
            return subprocess.check_output(
                ["powershell", "-Command", "Get-Clipboard"],
                text=True,
            )
        except (subprocess.CalledProcessError, FileNotFoundError):
            pass

    return ""


def run_cursor_agent(prompt: str, cwd: str = ".") -> bool:
    """
    Run Cursor agent CLI with the given prompt in the project directory.
    Returns True if agent ran, False if agent not found (fallback to editor + clipboard).
    """
    path = os.path.abspath(cwd) if cwd else os.getcwd()
    try:
        subprocess.run(["agent", "--version"], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False
    subprocess.Popen(["agent", prompt], cwd=path)
    return True


def open_cursor(cwd: str = ".") -> None:
    """Open Cursor in the given directory. Works when 'cursor' shell command is installed."""
    path = os.path.abspath(cwd) if cwd else os.getcwd()

    # Prefer 'cursor .' - works on all platforms when Cursor's shell command is installed
    try:
        subprocess.Popen(["cursor", path])
        return
    except FileNotFoundError:
        pass

    # Fallback: platform-specific
    if _sys == "Darwin":
        try:
            subprocess.Popen(["open", "-a", "Cursor", path])
        except FileNotFoundError:
            subprocess.Popen(["cursor", path])
    elif _sys == "Windows":
        try:
            subprocess.Popen(["cursor", path], shell=True)
        except FileNotFoundError:
            subprocess.Popen(["start", "", "cursor", path], shell=True)
    else:
        # Linux: try cursor, then xdg-open
        try:
            subprocess.Popen(["cursor", path])
        except FileNotFoundError:
            try:
                subprocess.Popen(["xdg-open", path])
            except FileNotFoundError:
                pass
