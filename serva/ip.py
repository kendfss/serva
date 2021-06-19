import subprocess

import pyperclip

def get_ip(version:str='ipv4', copy:bool=False) -> str:
    """
    Returns the IP address of the device on which the function is called
    Dependencies: subprocess.check_result, pyperclip.copy
    Arguments: copy=False
    Output: ipAddress [str]
    """
    call = str(subprocess.check_output('ipconfig')).split('\\n')
    line = [l for l in call if version in l.lower()][0]
    address = line.strip().strip('. ').strip('\\r').split(': ')[1]
    if copy: pyperclip.copy(address)
    return address