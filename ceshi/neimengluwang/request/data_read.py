import yaml


class YamlData:
    def __init__(self, path):
        self.path = path

    def read_yaml(self):
        with open(self.path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
        return data 



if __name__ == '__main__':
    yaml_data = YamlData('D:/Program Files/Projects/pythonProject/ceshi/neimengluwang/request/data.yaml')
    print(yaml_data.read_yaml())