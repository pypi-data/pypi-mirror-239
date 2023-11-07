import os
import subprocess
current_dir = os.path.dirname(__file__)
parent_dir = os.path.dirname(current_dir)

PARENT_DIR = f'{parent_dir}/tn5916_v3_0'
OVERWRITE_LIST = '\|'.join(['bridge'])

print(f'TESTFSM: inheritance the pattern from {PARENT_DIR}')

def get_command_output(command):
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    output = result.stdout.strip()
    return output
print('file_name:', OVERWRITE_LIST)
cmd_grep = f'ls {PARENT_DIR}| grep -v "{OVERWRITE_LIST}"'
cmd_xargs = f'xargs -I {{}} cp {PARENT_DIR}/{{}} {current_dir}/'
cmd = f'{cmd_grep} | {cmd_xargs}'
print('cmd:', cmd)
print(get_command_output(cmd))