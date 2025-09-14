from nornir import InitNornir
from nornir_utils.plugins.functions import print_result
from nornir_napalm.plugins.tasks import napalm_get

def show_version(task):
    """
    Retrieves hostname and OS version using NAPALM.
    """
    result = task.run(
        task=napalm_get,
        getters=["facts"]  # gets hostname, OS version, serial number, etc.
    )
    facts = result[0].result["facts"]
    print(f"{task.host.name} - Hostname: {facts['hostname']}, OS Version: {facts['os_version']}")

def main():
    nr = InitNornir(config_file="../config.yaml")
    result = nr.run(task=show_version)
    print_result(result)

if __name__ == "__main__":
    main()
