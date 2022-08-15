import yaml

def import_yaml(yaml_path):
    with open(yaml_path, "r") as stream:
        try:
            content = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
    return content