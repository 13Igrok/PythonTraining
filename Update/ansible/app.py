import subprocess

# Run Ansible command
def run_ansible():
    command = "ansible-playbook example_variables.yml"
    subprocess.run(command, shell=True)

# Run Ansible
run_ansible()
