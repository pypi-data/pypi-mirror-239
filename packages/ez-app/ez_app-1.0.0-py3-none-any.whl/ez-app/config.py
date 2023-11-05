import os
import json
from types import FunctionType

class Config:
    """
    config
    """
    def __init__(self, name:str, base_path:FunctionType) -> None:
        self.name = name
        self.keys = []
        self.data = {}
        self.base_path =base_path()

    def define_key(self, key:str, default: int) -> "Config":
        """
        define a key and set default value
        when the config file doesn't exist
        create a new file and fill it with 
        default values
        """
        self.keys.append(
            (key, default)
        )
        return self

    def get_path(self) -> str:
        """
        get the realpath of the config file
        """
        return os.path.realpath(
            os.path.join(
                self.base_path,
                "./{}.json".format(self.name)
            )
        )
    
    def get_default(self) -> dict:
        """
        get a default config dict
        """
        config = {}
        for key, default in self.keys:
            config[key] = default
        return config

    def read(self) -> bool:
        """
        read local config
        return True if file config exists
        """
        try:
            with open(self.get_path(), "r") as f:
                self.data = json.load(f)
            return True
        except FileNotFoundError:
            """
            create one instead
            """
            self.init()
            return False
    
    def init(self) -> None:
        """
        create a new config
        """
        self.data = self.get_default()
        with open(self.get_path(),"w+") as f:
            json.dump(
                self.data, 
                f, 
                ensure_ascii=False,
                sort_keys=True,
                indent=4
            )