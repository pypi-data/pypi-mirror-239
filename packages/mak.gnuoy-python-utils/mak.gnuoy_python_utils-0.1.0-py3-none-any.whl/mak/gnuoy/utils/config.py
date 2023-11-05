import configparser
import datetime
import os
import subprocess
import time

class Config:
    def __init__(self, filepath: str = "./config.ini"):
        self.filepath = filepath
        self.config = configparser.ConfigParser()
        try:
            self.last_modified = os.path.getmtime(self.filepath)
            self.config.read(self.filepath)
        except FileNotFoundError as e:
            self.last_modified = 0

    def _reload(self):
        if self.last_modified < os.path.getmtime(self.filepath):
            self.config.read(self.filepath)
            self.last_modified = os.path.getmtime(self.filepath)

    def get(self, section: str, key: str) -> str:
        self._reload()
        return self.config[section][key]

    def getBoolean(self, section: str, key: str) -> bool:
        self._reload()
        return self.config[section].getboolean(key)

    def getInt(self, section: str, key: str) -> int:
        self._reload()
        return self.config[section].getint(key)

    def getFloat(self, section: str, key: str) -> float:
        self._reload()
        return self.config[section].getfloat(key)

    def set(self, section: str, key: str, value: str):
        if not section in self.config:
            self.config[section] = {}
        self.config[section][key] = value

        with open(self.filepath, "w") as f:
            self.config.write(f)
    
    def fromDict(self, settings: dict):
        self.config.read_dict(settings)
        
        with open(self.filepath, "w") as f:
            self.config.write(f)

    def toDict(self) -> dict:
        return {s:dict(self.config.items(s)) for s in self.config.sections()}

    def clear(self):
        self.config.clear()

if __name__ == "__main__":
    config = Config()
    # TEST-1
    # config.set("Section1", "key1", "value1")
    # print(f"{config.get('Section1', 'key1')}")
    # config.set("Section1", "key2", "123")
    # print(f"{config.get('Section1', 'key1')}")
    # config.set("Section2", "key3", "True")
    # print(f"{config.get('Section2', 'key3')}")

    # config.clear()
    # settings = dict({
    #     "Section3": {
    #         "key4": 33
    #     }
    # })
    # config.fromDict(settings)
    # print(f"{config.toDict()}")

    # TEST-2
    print(f"{config.toDict()}")