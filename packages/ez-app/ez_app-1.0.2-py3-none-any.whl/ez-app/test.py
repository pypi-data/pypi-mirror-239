import os
from config import Config
from resources import Resource
from future_fields import FutureField, FutureFields

def get_base_path():
    return os.path.realpath(os.path.dirname(__file__))

def get_test_path():
    return os.path.realpath(
        os.path.join(
            get_base_path(),
            "./test/"
        )
    )

def test_config():
    conf = Config("config", get_test_path)
    conf.define_key("field_1",1)
    conf.define_key("field_2","acc")
    print(conf.read(), conf.data)


def test():
    os.makedirs(get_test_path(), exist_ok=True)
    test_config()

if __name__ == "__main__":
    test()