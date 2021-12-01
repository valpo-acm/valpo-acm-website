import yaml
from pathlib import Path

# Absolute path of the folder that contains this file.
PATH = str(Path(__file__).parent.parent.absolute()) + "/"

class Config:

    host = ""
    port = ""

    # load image and sound files from filepath strings, also load data
    def load_config(self):

        # Open and close the config file safely.
        with open(PATH + 'config.yaml', 'r') as file:
            config = yaml.safe_load(file)

            self.host = config['host']
            self.port = config['port']
