import yaml

class ConfigUtils:
    @classmethod
    def load_yaml_config(cls, config_file):
        """Read and parse config file
        """
        with open(config_file, "r") as f:
            config_txt = f.read()
            config = yaml.load(config_txt, Loader=yaml.FullLoader)
        return config, config_txt