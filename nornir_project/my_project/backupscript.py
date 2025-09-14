import pathlib
from datetime import date
from nornir import InitNornir
from nornir_scrapli.tasks import send_command
from nornir_utils.plugins.functions import print_result
from nornir_utils.plugins.tasks.files import write_file

nr = InitNornir(config_file="../config.yaml")

def backup_configurations(task):
    commands = ["show run", "show ip interface brief", "show interface"]
    for cmd in commands:
        config_dir = "./backup"
        date_dir = f"{config_dir}/{date.today()}"
        command_dir = f"{date_dir}/{cmd.replace(' ', '_')}"
        
        pathlib.Path(config_dir).mkdir(exist_ok=True)
        pathlib.Path(date_dir).mkdir(exist_ok=True)
        pathlib.Path(command_dir).mkdir(exist_ok=True)

        r = task.run(task=send_command, name=f"Run {cmd}", command=cmd)

        task.run(task=write_file, content=r.result, filename=f"{command_dir}/{task.host}.txt")

result = nr.run(task=backup_configurations)
print_result(result)

# import ipdb
# ipdb.set_trace()

