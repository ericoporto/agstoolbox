import winreg
from pathlib import PureWindowsPath


def set_run_key(key, value):
    """
    Set/Remove Run Key in Windows registry.

    :param key: Run Key Name
    :param value: Program to Run
    :return: None
    """
    # This is for the system run variable
    reg_key = winreg.OpenKey(
        winreg.HKEY_CURRENT_USER,
        r'Software\Microsoft\Windows\CurrentVersion\Run',
        0, winreg.KEY_WRITE | winreg.KEY_READ)

    if value is not None:
        value = str(PureWindowsPath(value))

    with reg_key:
        if value is None:
            winreg.DeleteValue(reg_key, key)
        else:
            if '%' in value:
                var_type = winreg.REG_EXPAND_SZ
            else:
                var_type = winreg.REG_SZ
            winreg.SetValueEx(reg_key, key, 0, var_type, value)
        winreg.CloseKey(reg_key)


def get_run_key(key):
    reg_key = winreg.OpenKey(
        winreg.HKEY_CURRENT_USER,
        r'Software\Microsoft\Windows\CurrentVersion\Run',
        0, winreg.KEY_READ)

    with reg_key:
        ret_val = None
        try:
            ret_val = winreg.QueryValue(reg_key, key)
        except OSError:
            ret_val = None
        finally:
            winreg.CloseKey(reg_key)
            return ret_val
