import os
import subprocess


def init_subprocess_module():
    try:
        os.environ["COMPSEC"] = 'C:\\Windows\\System32\\cmd.exe'
    except:
        pass


def clear_screen():
    try:
        subprocess.call(['cls'])
    except:
        subprocess.call(['clear'])


def uninstall_lib(library):
    try:
        subprocess.check_output(["pip", "uninstall", library, "-y"])
    except:
        subprocess.check_output(["pip3", "uninstall", library, "-y"])


init_subprocess_module()