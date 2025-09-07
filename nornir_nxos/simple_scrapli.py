from nornir import InitNornir
from nornir_scrapli.tasks import send_command
from nornir_utils.plugins.functions import print_result
from rich import print as rprint

nr = InitNornir(config_file="config.yaml")

def show_version(task):
    response = task.run(task=send_command, command="show version")
    task.host['facts'] = response.scrapli_response.genie_parse_output()

output = nr.run(task=show_version)
print_result(output)

import ipdb
ipdb.set_trace()
