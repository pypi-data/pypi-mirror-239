class FutureFields:
    """
    to use FutureField, you have to initialize a FutureFields
    to store the data of FutureField(s)
    """
    field_containers = {}
    def __init__(self, namespace:str="default") -> None:
        self.field_containers[namespace] = self
        self.fields = {}

class FutureField:
    """
    define a field that work across file
    """
    def __init__(self, name:str, namespace:str="default") -> None:
        self.name = name
        self.namespace = namespace
    
    def set(self, value) -> None:
        """
        set. nothing else
        """
        if not FutureFields.I: raise ValueError("Object 'FutureFields namespace={}' doesn't exists.".format(repr(self.namespace)))
        f = FutureFields.I.fields
        f[self.name] = value

    def get(self):
        """
        get. nothing else
        """
        if not FutureFields.I: raise ValueError("Object 'FutureFields namespace={}' doesn't exists.".format(repr(self.namespace)))
        f = FutureFields.I.fields
        return f.get(self.name, None)