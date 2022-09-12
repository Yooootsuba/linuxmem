import sys
import shutil
import subprocess


def print_error(message):
    print(message, file = sys.stderr)
    exit()


def pgrep_is_in_system_path():
    return shutil.which('pgrep') != None


def get_process_id_by_name(process_name):
    if pgrep_is_in_system_path() == False:
        print_error('pgrep is not in system path !')

    try:
        return int(subprocess.check_output(['pgrep', process_name]))
    except:
        print_error('process not found !')
