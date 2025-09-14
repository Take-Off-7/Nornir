from nornir import InitNornir
from nornir.core.task import Task, Result
from nornir_utils.plugins.functions import print_result
import time

def check_config(task: Task, feature: str) -> Result:
    """
    Simulate checking a feature on the host.
    Falls back to 'unknown' if the key is missing in inventory.
    """
    time.sleep(1)  # simulate processing delay
    data_value = task.host.get(f"{feature}_server", "unknown")
    message = f"{task.host.name} {feature} is {data_value}"
    return Result(host=task.host, result=message)

def main():
    # Initialize Nornir from config.yaml
    nr = InitNornir(config_file="../config.yaml")

    # Run the task on all hosts
    result = nr.run(task=check_config, feature="nxos")

    # Print results
    print_result(result)

if __name__ == "__main__":
    main()
