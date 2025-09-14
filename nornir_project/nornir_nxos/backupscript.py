import pathlib
from nornir import InitNornir
from nornir_netmiko.tasks import netmiko_send_command
from nornir_utils.plugins.functions import print_result
from nornir_utils.plugins.tasks.files import write_file

nr = InitNornir(config_file="../config.yaml")

config_directory = "backups"

def backup_config(task):
    # Grab running config only (avoids startup-config lock)
    result = task.run(task=netmiko_send_command, command_string="show running-config")
    
    pathlib.Path(config_directory).mkdir(exist_ok=True)
    task.run(
        task=write_file,
        content=result.result,
        filename=f"{config_directory}/{task.host}.txt"
    )

results = nr.run(task=backup_config)
print_result(results)
