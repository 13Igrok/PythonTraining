import subprocess

playbook_path = '/path/to/playbook.yml'
inventory_path = '/path/to/inventory'

command = f'ansible-playbook {playbook_path} -i {inventory_path}'
subprocess.run(command, shell=True, check=True)
