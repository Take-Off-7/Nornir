from nornir import InitNornir
from nornir_netmiko.tasks import netmiko_send_command
from nornir_utils.plugins.functions import print_result

def main():
    nr = InitNornir(config_file="../config.yaml")
    result = nr.run(
        task=netmiko_send_command,
        command_string="show run"
    )
    print_result(result)

if __name__ == "__main__":
    main()
