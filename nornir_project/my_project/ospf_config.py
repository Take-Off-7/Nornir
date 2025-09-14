from nornir import InitNornir
from nornir_scrapli.tasks import send_configs
from nornir_utils.plugins.functions import print_result
from nornir_utils.plugins.tasks.data import load_yaml
from jinja2 import Environment, FileSystemLoader

nr = InitNornir(config_file="../config.yaml")
env = Environment(loader=FileSystemLoader("templates"))

def load_ospf_vars(task):
    data = task.run(task=load_yaml, file="./host_vars/ospf_vars.yaml")
    task.host["ospf_fact"] = data.result
    nr.run(task=render_ospf_config)

def render_ospf_config(task):
    template = env.get_template("ospf_template.j2")
    result = task.host["ospf_fact"]
    rendered = template.render(**result)
    task.host["ospf_config"] = rendered
    nr.run(task=print_ospf_config)

def print_ospf_config(task):
    print(f"=== Rendered OSPF config for {task.host} ===")
    print(task.host["ospf_config"])
    print("==========================================")
    nr.run(task=push_ospf_config)

def push_ospf_config(task):
    ospf_config = task.host["ospf_config"].splitlines()
    result = task.run(task=send_configs, configs=ospf_config)
    task.host["facts"] = result.result

result = nr.run(task=load_ospf_vars)
print_result(result)

# import ipdb
# ipdb.set_trace()