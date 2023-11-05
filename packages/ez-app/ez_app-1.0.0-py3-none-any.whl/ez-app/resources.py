import os

class Resource:
    """
    readonly file / folder
    easily create a directory tree
    """
    def __init__(self, where:str, type:str) -> None:
        self.where = where
        self.type = type
        self.name = ""
        self.postfix = ""
        self.children = {}
        self.file = None
    
    def read(self) -> None:
        """
        open the file the resource has
        you still need to read the property 'file'
        of the object by yourself
        """
        if self.type=="file": 
            self.close()
            self.file = open(self.where,"r",encoding="utf-8")
    
    def close(self) -> None:
        """
        close the file the resource has
        """
        if self.file:
            self.file.close()
            self.file = None

    def get(self, name:str) -> "Resource":
        """
        get the file with the specific name under the resource,
        only available for folder,
        return None if not found.
        """
        return self.children.get(name,None)

    @staticmethod
    def create(where:str) -> "Resource":
        """
        create a resource from the specific location,
        automatically create the children under it if
        it is a folder
        """
        r = Resource(where,"file" if os.path.isfile(where) else "folder")
        Resource.create_from_resource(r)
        return r
    
    def __repr__(self) -> str:
        """
        you can understand it, can't you?
        """
        return '<Resource where="{}" type="{}" name="{}" postfix="{}">'.format(self.where,self.type,self.name,self.postfix)

    @staticmethod
    def create_from_resource(where:"Resource") -> None:
        """
        work with a folder Resource
        create all the children under the folder
        """
        for filename in os.listdir(where.where):
            file_path = os.path.realpath( os.path.join(where.where,filename) )
            isfile = os.path.isfile(file_path)

            where.children[filename] = r = Resource(file_path,"file" if isfile else "folder")

            if isfile: 
                name, postfix = filename.split(".",1)
                r.name = name
                r.postfix=postfix  
            
            if not isfile: Resource.create_from_resource(r)
