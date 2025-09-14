import json
from rich import print as rprint
from nornir import InitNornir
from nornir_scrapli.tasks import send_command, send_configs
from nornir_utils.plugins.functions import print_result

nr = InitNornir(config_file="../config.yaml")

def get_cdp(task):
    interfaces_list = []
    interfaces_result = task.run(task=send_command, command="show interface brief | json")
    task.host["interfaces_facts"] = json.loads(interfaces_result.result)
    interfaces = task.host["interfaces_facts"]["TABLE_interface"]["ROW_interface"]
    for interface in interfaces:
        intf = interface["interface"]
        if intf not in ("mgmt0", "loopback0"):
            interfaces_list.append(intf)
            print(interfaces_list)

    cdp_result = task.run(task=send_command, command="show cdp neighbor | json")
    task.host["cdp_facts"] = json.loads(cdp_result.result)
    ## Incomplete ##
    clean_interfaces(task, interfaces_list)

def clean_interfaces(task, interfaces_list):
    for interfaces in interfaces_list:
        task.run(task=send_configs, configs=[f"interface {interfaces}", "switchport", "shutdown", "description SHUTDOWN"])

results = nr.run(task=get_cdp)
print_result(results)

# import ipdb
# ipdb.set_trace()
